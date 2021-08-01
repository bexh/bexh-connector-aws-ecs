import json
import boto3
from src.app.bet_connector.bet_consumer import BetConsumer

# TODO: redefine how to test this

# Scratch testing method
# def test_bet_connector():
#     path = "resources/bet-connector/executed-bet.json"
#     with open(path) as f:
#         event = json.load(f)
#
#     consumer = BetConsumer()
#     consumer.process(event)

# Scratch testing method
# def test_add_message_to_kinesis():
#     path = "resources/bet-connector/executed-bet.json"
#     with open(path) as f:
#         event = json.load(f)
#     kinesis = boto3.client('kinesis')
#     kinesis.put_record(
#         StreamName="bexh-exch-bets-out-dev-189266647936",
#         Data=json.dumps(event).encode('utf-8'),
#         PartitionKey='1',
#     )
