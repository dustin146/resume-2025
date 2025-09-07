import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
os.environ["TABLE_NAME"] = "visitor_counter"

import json
import app

def test_get_handler_returns_zero(monkeypatch):
    # Fake DynamoDB client
    class FakeDDB:
        def get_item(self, TableName, Key, ConsistentRead):
            return {"Item": {"pk": {"S": "resume"}, "count": {"N": "0"}}}

    monkeypatch.setattr(app, "ddb", FakeDDB())

    event = {"requestContext": {"http": {"method": "GET"}}, "headers": {}}
    resp = app.handler(event, None)
    body = json.loads(resp["body"])
    assert body["count"] == 0
    assert resp["statusCode"] == 200
