from src.consumer import Consumer
from src.domain_model import AggregatedBets


class AggregatedBetInfoConsumer(Consumer):
    def __init__(self):
        super(AggregatedBetInfoConsumer, self).__init__()

    def process(self, message):
        aggregated_bets = AggregatedBets(**message)
        self._mysql.execute("""
            INSERT INTO AGG_BETS (EVENT_ID, ODDS, DTM, WINDOW_INTERVAL)
            VALUES ('%s', %s, %s, %s)
        """ % (
            aggregated_bets.event_id,
            int(aggregated_bets.odds),
            aggregated_bets.row_time.strftime("%Y-%m-%d %H:%M:%S"),
            5
        ))
