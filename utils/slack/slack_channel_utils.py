from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()
slack_token = os.getenv("SLACK_API_TOKEN")
client = WebClient(token=slack_token)

def get_channel_list():
    """
    Slack APIを使用して全てのパブリックチャンネルのIDと名前を取得します。
    戻り値: {<channel_id>: <channel_name>} の形式の辞書
    """
    try:
        response = client.conversations_list()
        channels = response['channels']
        # チャンネルIDと名前のペアを辞書で返す
        return {channel['id']: channel['name'] for channel in channels if not channel.get('is_archived', False)}
    except SlackApiError as e:
        print(f"Error fetching channel list: {e.response['error']}")
        return {}

def get_channel_name(channel_id):
    """
    指定されたチャンネルIDからチャンネル名を取得します。
    """
    try:
        response = client.conversations_info(channel=channel_id)
        channel_name = response['channel']['name']
        return channel_name
    except SlackApiError as e:
        print(f"Error fetching channel name: {e.response['error']}")
        return None
