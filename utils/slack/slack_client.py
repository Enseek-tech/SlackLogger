from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from dotenv import load_dotenv

load_dotenv()
slack_token = os.getenv("SLACK_API_TOKEN")
client = WebClient(token=slack_token)

def get_slack_logs(channel_id, start_date, end_date):
    """
    指定されたチャンネルのSlackメッセージを取得します。
    """
    try:
        response = client.conversations_history(
            channel=channel_id,
            oldest=start_date.timestamp(),
            latest=end_date.timestamp(),
            inclusive=True
        )
        return response.get('messages', [])
    except SlackApiError as e:
        print(f"Error fetching Slack logs: {e.response['error']}")
        return []
