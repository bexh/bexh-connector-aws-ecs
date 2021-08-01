import json
import boto3
from src.app.aggregated_bet_info_connector.aggregated_bet_info_consumer import AggregatedBetInfoConsumer


# TODO: redefine how to test this
# Scratch testing method
# def test_agg_bet_connector():
#     path = "resources/aggregated-bet-info-connector/five-min-agg.json"
#     with open(path) as f:
#         event = json.load(f)
#
#     consumer = AggregatedBetInfoConsumer()
#     consumer.process(event)
