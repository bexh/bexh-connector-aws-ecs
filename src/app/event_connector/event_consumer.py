from src.consumer import Consumer
from src.domain_model import Event
import os
from src.db import ES
from src.utils import iso_to_mysql_format
from pymysql import IntegrityError


class EventConsumer(Consumer):
    def __init__(self):
        es_host = os.environ.get("ES_HOST")
        es_port = os.environ.get("ES_PORT")
        self._es = ES(host=es_host, port=es_port)

        super(EventConsumer, self).__init__()

    def process(self, message):
        self._logger.debug(f"Processing message: {message}")
        event = Event(**message["value"])
        action = message["action"]

        if action == "ACTIVE_EVENT":
            self._handle_active_event(event=event)
        elif action == "INACTIVE_EVENT":
            self._handle_inactive_event(event=event)
        else:
            self._logger.error(f"{action} is not a valid event type")

    def _handle_active_event(self, event: Event):
        dtm = iso_to_mysql_format(iso=event.date)
        try:
            self._mysql.execute("""
                INSERT INTO EVENT(EVENT_ID, HOME, AWAY, HOME_ABBREV, AWAY_ABBREV, SPORT, DTM)
                VALUES
                    ('%s', '%s', '%s', '%s', '%s', '%s', '%s');
            """ % (event.event_id, event.home_team_name, event.away_team_name, event.home_team_abbrev,
                   event.away_team_abbrev, event.sport, dtm))
        except IntegrityError as e:
            error_code, error_message = e.args
            # duplicate entry code
            if error_code != 1062:
                raise e

        inputs = self._create_suggest_input(home_team=event.home_team_name, away_team=event.away_team_name)
        title = f"{event.home_team_name} vs {event.away_team_name}"
        record = {
          "name": {
            "input": inputs
          },
          "title": title,
          "id": event.event_id,
          "sport": event.sport
        }
        self._es.store_record(index_name="bexh", record=record, doc_type="events")
        self._logger.debug("New event to ES:", record)

    @staticmethod
    def _create_suggest_input(home_team: str, away_team: str):
        inputs = []
        title = f"{home_team.lower()} vs {away_team.lower()}"
        reverse_title = f"{away_team.lower()} vs {home_team.lower()}"
        for title in [title, reverse_title]:
            split_title = title.split(" ")
            for i in range(len(split_title) - 1):
                inputs.append(" ".join(split_title[i:]))
        return inputs

    def _handle_inactive_event(self, event: Event):
        # set status inactive
        self._mysql.execute("""
            UPDATE EVENT
            SET STATUS = 'INACTIVE', CURRENT_ODDS = NULL
            WHERE EVENT_ID = '%s';
        """ % event.event_id)

        # remove from ES
        self._es.delete_record(index_name="bexh", doc_type="events", query={"id": event.event_id})

        # set won
        self._mysql.execute("""
            UPDATE BETS
            SET WON = 1
            WHERE EVENT_ID = '%s'
            AND ON_TEAM = '%s';
        """ % (event.event_id, event.winning_team_abbrev))

        # set lost
        self._mysql.execute("""
            UPDATE BETS
            SET WON = 0
            WHERE EVENT_ID = '%s'
            AND ON_TEAM = '%s';
        """ % (event.event_id, event.losing_team_abbrev))

        # settle exchange bets
        self._mysql.execute("""
            UPDATE USERS u
            JOIN 
                (SELECT USER_ID, SUM(AMOUNT_WON) AS USER_AMOUNT_WON FROM
                (
                    SELECT USER_ID,
                    CASE
                        WHEN EXECUTED_ODDS > 0 THEN ROUND(EXECUTED_AMOUNT * (EXECUTED_ODDS / 100.00), 2)
                        ELSE ROUND(EXECUTED_AMOUNT / (ABS(EXECUTED_ODDS)/100.00), 2)
                    END AS AMOUNT_WON
                    FROM BETS
                    WHERE EVENT_ID = '%s'
                    AND ON_TEAM = '%s'
                    AND EXECUTED_ODDS IS NOT NULL
                ) t
                GROUP BY USER_ID
            ) b
            ON (u.USER_ID = b.USER_ID)
            SET u.BALANCE = u.BALANCE + b.USER_AMOUNT_WON;
        """ % (event.event_id, event.winning_team_abbrev))
