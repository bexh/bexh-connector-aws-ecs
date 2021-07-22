from src.consumer import Consumer
from src.domain_model import ExecutedBets, Bet


class BetConsumer(Consumer):
    def __init__(self):
        super(BetConsumer, self).__init__()

    def process(self, message):
        self._logger.debug(f"Processing message: {message}")
        executed_bets = ExecutedBets(**message)
        bets: [Bet] = executed_bets.to_bets()
        for bet in bets:
            if bet.status == "EXECUTED":
                self._handle_executed(bet=bet)
            elif bet.status == "PARTIALLY_EXECUTED":
                self._handle_partially_executed(bet=bet)
            elif bet.status == "CANCELLED":
                self._handle_cancelled(bet=bet)
            elif bet.status == "EXPIRED_EVENT":
                self._handle_expired_event(bet=bet)
            elif bet.status == "INSUFFICIENT_VOLUME":
                self._handle_insufficient_volume(bet=bet)
            else:
                self._logger.error(
                    f"Bet status {bet.status} does not match acceptable statuses "
                    "EXECUTED, PARTIALLY_EXECUTED, CANCELLED, EXPIRED_EVENT, INSUFFICIENT_VOLUME"
                )

    def _handle_executed(self, bet: Bet):
        self._mysql.execute("""
            UPDATE BETS
            SET STATUS = 'executed',
                EXECUTED_AMOUNT = CASE
                    WHEN EXECUTED_AMOUNT IS NOT NULL THEN EXECUTED_AMOUNT + %s
                    ELSE %s
                END,
                EXECUTED_ODDS = CASE
                    WHEN EXECUTED_ODDS IS NOT NULL THEN (EXECUTED_ODDS * (EXECUTED_AMOUNT/(EXECUTED_AMOUNT + %s))) + (%s * (%s/(EXECUTED_AMOUNT + %s)))
                    ELSE %s
                END
            WHERE BET_ID = %s;
        """ % (
            bet.amount,
            bet.amount,
            bet.amount, bet.odds, bet.amount, bet.amount,
            bet.odds,
            bet.bet_id
        ))

    def _handle_partially_executed(self, bet: Bet):
        self._mysql.execute("""
            UPDATE BETS
            SET STATUS = 'partially executed',
                EXECUTED_AMOUNT = CASE
                    WHEN EXECUTED_AMOUNT IS NOT NULL THEN EXECUTED_AMOUNT + %s
                    ELSE %s
                END,
                EXECUTED_ODDS = CASE
                    WHEN EXECUTED_ODDS IS NOT NULL THEN (EXECUTED_ODDS * (EXECUTED_AMOUNT/(EXECUTED_AMOUNT + %s))) + (%s * (%s/(EXECUTED_AMOUNT + %s)))
                    ELSE %s
                END
            WHERE BET_ID = %s;
        """ % (
            bet.amount,
            bet.amount,
            bet.amount, bet.odds, bet.amount, bet.amount,
            bet.odds,
            bet.bet_id
        ))

    def _handle_cancelled(self, bet: Bet):
        self._mysql.execute("""
            UPDATE BETS
            SET STATUS = 'cancelled',
            WHERE BET_ID = %s;
        """ % bet.bet_id)

        self._mysql.execute("""
            UPDATE USERS
            SET BALANCE = BALANCE + %s
            WHERE USER_ID = %s;
        """ % (bet.amount, bet.user_id))

    def _handle_expired_event(self, bet: Bet):
        # set won
        self._mysql.execute("""
            UPDATE BETS
            SET WON = 1,
                STATUS = 'completed'
            WHERE EVENT_ID = '%s'
            AND ON_TEAM = '%s';
        """ % (bet.event_id, bet.winning_team_abbrev))

        # set lost
        self._mysql.execute("""
            UPDATE BETS
            SET WON = 0,
                STATUS = 'completed'
            WHERE EVENT_ID = '%s'
            AND ON_TEAM != '%s';
        """ % (bet.event_id, bet.winning_team_abbrev))

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
        """ % (bet.event_id, bet.winning_team_abbrev))

    def _handle_insufficient_volume(self, bet: Bet):
        self._mysql.execute("""
            UPDATE BETS
            SET STATUS = 'cancelled',
            WHERE BET_ID = %s;
        """ % bet.bet_id)

        self._mysql.execute("""
            UPDATE USERS
            SET BALANCE = BALANCE + %s
            WHERE USER_ID = %s;
        """ % (bet.amount, bet.user_id))
