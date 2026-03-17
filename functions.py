import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def github_activity(user, key = None,timeout=5):
    url = f"https://api.github.com/users/{user}/events"
    headers = {'User-Agent': 'MonitorApp/1.0'}
    found = False
    try:
        request = Request(url, headers=headers)
        with urlopen(request, timeout=timeout) as answer:
            events = json.loads(answer.read())

            if not events:
                print(f"No activity from user {user}")

            for event in events:
                event_type = event.get("type")
                repository_name = event.get("repo", {}).get("name")
                if key and key != event_type:
                    continue
                match event_type:
                    case "PushEvent":
                        print(f"Pushed changes to {repository_name}")
                        found = True
                    case "IssuesEvent":
                        issue = event.get("payload", {}).get("action")
                        print(f"{issue} a new issue in {repository_name}")
                        found = True

                    case "WatchEvent":
                        print(f"Starred {repository_name}")
                        found = True

                    case "CreateEvent":
                        ref_type = event.get("payload", {}).get("ref_type")
                        print(f"Created a new {ref_type} in {repository_name}")
                        found = True
            if not found:
                print(f"No activities found for type {key}")
        return ''

    except HTTPError as e:
        code = e.code
        if code == 404:
            return f'Resource not found, {code}'
        return f'Error code : {code}'
    except URLError as e:
        return f'URLError {e.reason}'
    except Exception as e:
        return f'Error: {e}'
