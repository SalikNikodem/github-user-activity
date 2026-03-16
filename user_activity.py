from functions import github_activity
import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Run: python user_activity.py [user]")
        sys.exit(1)

    print(github_activity(sys.argv[1]))