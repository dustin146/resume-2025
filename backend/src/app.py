import json, os, boto3

ddb = boto3.client("dynamodb")
TABLE = os.environ["TABLE_NAME"]
PK = {"pk": {"S": "resume"}}

def _headers(origin: str):
    allow = origin if origin.startswith("https://") else os.environ.get("ALLOW_ORIGIN", "https://dustinumphress.com")
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": allow,
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Cache-Control": "no-store"
    }

def handler(event, _ctx):
    # Works for HTTP API "Lambda proxy" events
    method = (event.get("requestContext", {}).get("http", {}) or {}).get("method", "GET")
    origin = (event.get("headers") or {}).get("origin", "")

    if method == "OPTIONS":
        return {"statusCode": 204, "headers": _headers(origin), "body": ""}

    if method == "POST":
        r = ddb.update_item(
            TableName=TABLE,
            Key=PK,
            UpdateExpression="ADD #c :one",
            ExpressionAttributeNames={"#c": "count"},
            ExpressionAttributeValues={":one": {"N": "1"}},
            ReturnValues="UPDATED_NEW"
        )
        count = int(r["Attributes"]["count"]["N"])
        return {"statusCode": 200, "headers": _headers(origin), "body": json.dumps({"count": count})}

    if method == "GET":
        r = ddb.get_item(TableName=TABLE, Key=PK, ConsistentRead=True)
        count = int(r.get("Item", {}).get("count", {}).get("N", "0"))
        return {"statusCode": 200, "headers": _headers(origin), "body": json.dumps({"count": count})}

    return {"statusCode": 405, "headers": _headers(origin), "body": json.dumps({"message": "Method not allowed"})}
