from functions import github_activity, events
import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Run: python user_activity.py [user] [event](optional)")
        sys.exit(1)
    user = sys.argv[1]

    key = sys.argv[2] if len(sys.argv) > 2 else None

    if key and key not in events:
        print(f"Filter events use from list: {events}")
        sys.exit(1)

    github_activity(user, key=key)