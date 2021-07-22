import boto3
from json import load, dumps
import os


event_connector_test_path = "test/resources/event-connector/active-event.json"

with open(event_connector_test_path) as f:
    messages = load(f)

kinesis_stream_name = os.environ.get("KINESIS_SOURCE_STREAM_NAME")
endpoint_url = os.environ.get("ENDPOINT_URL")
client = boto3.client("kinesis", endpoint_url=endpoint_url)
for message in messages:
    client.put_record(
        StreamName=kinesis_stream_name,
        Data=dumps(message),
        PartitionKey="1"
    )
