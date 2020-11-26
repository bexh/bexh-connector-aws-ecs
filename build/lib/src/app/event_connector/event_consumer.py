from src.consumer import Consumer
from src.domain_model import Event
import os
from src.db import ES


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
            self._logger.error("Not a valid event type")

    def _handle_active_event(self, event: Event):
        self._mysql.execute("""
            INSERT INTO EVENT(EVENT_ID, HOME, AWAY, HOME_ABBREV, AWAY_ABBREV, SPORT, DTM)
            VALUES
                ('%s', '%s', '%s', '%s', '%s', '%s', '%s');
        """ % (event.event_id, event.home_team_name, event.away_team_name, event.home_team_abbrev,
               event.away_team_abbrev, event.sport, event.date))



    def _handle_inactive_event(self, event: Event):
        pass
