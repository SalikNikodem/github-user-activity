import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def github_activity(user, timeout=5):
    url = f"https://api.github.com/users/{user}/events"
    headers = {'User-Agent': 'MonitorApp/1.0'}

    try:
        request = Request(url, headers=headers)
        with urlopen(request, timeout=timeout) as answer:
            events = json.loads(answer.read())
            for event in events:
                event_type = event.get("type")
                repository_name = event.get("repo", {}).get("name")

                match event_type:
                    case "PushEvent":
                        print("asdas")



    except HTTPError as e:
        code = e.code
        if code == 404:
            return f'Resource not found, {code}'
        return f'Error code : {code}'
    except URLError as e:
        return f'URLError {e.reason}'
    except Exception as e:
        return f'Error: {e}'

