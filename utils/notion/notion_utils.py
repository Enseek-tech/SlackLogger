from notion_client import Client
import os
from dotenv import load_dotenv
import datetime
from const.user_mapper import USER_MAPPER

# 環境変数をロードします
load_dotenv()

# Notionクライアントを初期化します
notion = Client(auth=os.getenv("NOTION_API_TOKEN"))

def get_user_name(user_id):
    """
    SlackのユーザーIDからユーザー名を取得します。
    """
    return USER_MAPPER.get(user_id, user_id)

def fetch_existing_messages(page_id):
    """
    Notionページから既存のメッセージを取得し、メッセージ本文をセットとして返します。(差分検出のため)
    """
    try:
        blocks = notion.blocks.children.list(block_id=page_id)["results"]
        return {
            block["paragraph"]["rich_text"][0]["text"]["content"]
            for block in blocks
            if block["type"] == "paragraph" and block["paragraph"]["rich_text"]
        }
    except Exception as e:
        print(f"Error fetching existing messages from Notion: {e}")
        return set()

def format_message_content(message):
    """
    Slackメッセージをフォーマットして返します。
    ユーザー名はuser_mapperからローカルに取得して、タイムスタンプの形式を直す。
    """
    ts = message.get('ts', '')
    user_id = message.get('user', 'Unknown User')
    text = message.get('text', '')

    user_name = get_user_name(user_id)
    timestamp = datetime.datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M:%S')

    return f"{timestamp} - {user_name}: {text}"

def create_notion_block(message_content):
    """
    Notion用のブロックを作成して返します。
    """
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {"type": "text", "text": {"content": message_content}}
            ]
        }
    }

def add_messages_to_notion(messages, page_id, channel_name):
    """
    SlackメッセージをNotionページに差分追加します。
    """
    existing_messages = fetch_existing_messages(page_id)
    print(f"Found {len(existing_messages)} existing messages in Notion.")

    new_messages = [
        create_notion_block(format_message_content(message))
        for message in messages
        if format_message_content(message) not in existing_messages
    ]

    if new_messages:
        try:
            notion.blocks.children.append(block_id=page_id, children=new_messages)
            print(f"Added {len(new_messages)} new messages to Notion page {channel_name}.")
        except Exception as e:
            print(f"Error adding messages to Notion: {e}")
    else:
        print(f"No new messages to add for channel {channel_name}.")

def add_to_notion(channel_name, logs):
    """
    指定されたチャンネルのSlackメッセージを取得し、Notionのページに差分追加します。
    """
    notion_page_id = os.getenv(f"NOTION_PAGE_ID_{channel_name.upper()}")
    if not notion_page_id:
        print(f"Page ID not found for channel: {channel_name}")
        return

    existing_messages = fetch_existing_messages(notion_page_id)
    print(f"Found {len(existing_messages)} existing messages in Notion for channel: {channel_name}.")

    new_messages = [
        message for message in logs
        if format_message_content(message) not in existing_messages
    ]

    if new_messages:
        print(f"Adding {len(new_messages)} new messages to Notion for channel: {channel_name}")
        add_messages_to_notion(new_messages, notion_page_id, channel_name)
    else:
        print(f"No new messages to add for channel: {channel_name}")
