from apscheduler.schedulers.blocking import BlockingScheduler
from utils.slack.slack_channel_utils import get_channel_list
from utils.slack.slack_client import get_slack_logs
from utils.notion.notion_utils import add_to_notion
import datetime

def export_logs(export_function, description):
    """
    指定されたエクスポート関数を使用してSlackログをNotionにエクスポートします。
    """
    print(f"Starting {description} export...")
    channel_list = get_channel_list()
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)

    for channel_id, channel_name in channel_list.items():
        print(f"Fetching messages for channel: {channel_name}")
        logs = get_slack_logs(channel_id, start_date, end_date)
        if logs:
            print(f"Writing {len(logs)} messages to Notion for channel: {channel_name}")
            export_function(channel_name, logs)
        else:
            print(f"No new messages for channel: {channel_name}")

    print(f"{description.capitalize()} export completed.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "manual":
        export_logs(add_to_notion, "manual")
    else:
        scheduler = BlockingScheduler()
        scheduler.add_job(export_logs(add_to_notion, "weekly"), 'cron', day_of_week='sun', hour=0, minute=0)
        print("Scheduler started.")
        scheduler.start()
