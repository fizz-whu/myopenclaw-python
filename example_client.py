import requests
import sys


def send_message(message: str, channel: str = "cli", account_id: str = None):
    url = "http://localhost:8000/message"

    payload = {
        "message": message,
        "channel": channel,
        "account_id": account_id,
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        print(f"\nAgent: {data['agent_id']}")
        print(f"Session: {data['session_key']}")
        print(f"\n{data['response']}\n")

        if not data['success']:
            print(f"Error: {data['error']}")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to gateway: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python example_client.py 'your message here'")
        sys.exit(1)

    message = " ".join(sys.argv[1:])
    send_message(message)
