import json


def parse_response_content(response):
    """Try to load json response
    If fail just return string response
    """
    try:
        return json.loads(response.content.decode())
    except json.JSONDecodeError:
        return response.content.decode()
