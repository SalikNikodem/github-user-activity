import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime
import time
from pathlib import Path

events = ["PushEvent", "IssuesEvent", "WatchEvent", "CreateEvent", "DeleteEvent", "ForkEvent", "PublicEvent","DiscussionEvent"]


def github_activity(user, key = None,timeout=5):
    cache_f = Path(f"{user}_cache.json")
    found = False
    if cache_f.exists() and (time.time() - cache_f.stat().st_mtime < 1200):
        with open(cache_f, "r") as ff:
            events = json.load(ff)
            match(events, key=key, found=found, user=user)
            return ''

    url = f"https://api.github.com/users/{user}/events"
    headers = {'User-Agent': 'MonitorApp/1.0'}
    try:
        request = Request(url, headers=headers)
        with urlopen(request, timeout=timeout) as answer:
            events = json.loads(answer.read())
        with open(cache_f, "w") as ff:
            json.dump(events, ff)
        match(events,key=key, found=found,user=user)

    except HTTPError as e:
        code = e.code
        if code == 404:
            return f'Resource not found, {code}'
        elif code == 403:
            return f"Forbidden, {code}"
        return f'Error code: {code}'
    except URLError as e:
        return f'URLError {e.reason}'
    except Exception as e:
        return f'Error: {e}'

def match(events, key, found, user):
    if not events:
        print(f"No activity from user {user}")

    for event in events:
        event_type = event.get("type")
        repository_name = event.get("repo", {}).get("name")
        raw_date = event.get("created_at").replace("Z", "")

        # ISO 8601 type convert
        date = datetime.fromisoformat(raw_date)

        if key and key != event_type:
            continue
        match event_type:
            case "DiscussionEvent":
                action = event.get("payload", {}).get("action")
                print(f"{date}: {action} Discussion in {repository_name}")
            case "PublicEvent":
                print(f"{date}: {repository_name} is now public")
            case "ForkEvent":
                action = event.get("payload", {}).get("action")
                print(f"{date}: {action} in {repository_name}")
            case "DeleteEvent":
                ref_type = event.get("payload", {}).get("ref_type")
                print(f"{date}: Deleted {ref_type} in {repository_name} ")
                found = True
            case "PushEvent":
                print(f"{date}: Pushed changes to {repository_name}")
                found = True
            case "IssuesEvent":
                issue = event.get("payload", {}).get("action")
                print(f"{date}: {issue} a new issue in {repository_name}")
                found = True
            case "WatchEvent":
                print(f"{date}: Starred {repository_name}")
                found = True

            case "CreateEvent":
                ref_type = event.get("payload", {}).get("ref_type")
                print(f"{date}: Created a new {ref_type} in {repository_name}")
                found = True
    if not found and key:
        print(f"No activities found for type {key}")
    return ''