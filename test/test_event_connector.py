from src.db import ES
import pytest


def test_es():
    try:
        es = ES(host="localhost", port=9200)
        record = {
          "name": {
            "input": [
              "Detroit Pistons vs Chicago Bulls",
              "Pistons vs Chicago Bulls",
              "Chicago Bulls",
              "Bulls",
              "Chicago Bulls vs Detroit Pistons",
              "Bulls vs Detroit Pistons",
              "Detroit Pistons",
              "Pistons"
              ]
          },
          "title": "Detroit Pistons vs Chicago Bulls",
          "id": 1,
          "sport": "basketball"
        }
        es.store_record(index_name="bexh", record=record, doc_type="events")
    except Exception as e:
        print(str(e))
