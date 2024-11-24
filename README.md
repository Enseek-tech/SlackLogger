# Slackログ保存BOT改


- 省コード化
- 超高速
- 安定

# 利用
- 現在はマニュアルでの実行のみを想定しています。.envファイルを作成して以下を作成
- 定期実行にも一応対応している CloudFlareとかにデプロイしてcronでスケジューリングとか

```
SLACK_API_TOKEN=
NOTION_API_TOKEN=
NOTION_DATABASE_ID=148712765bdc804f93edc264dc5898f1
# Notionの保存する先のページID
NOTION_PAGE_ID_0_GENERAL=148712765bdc81a19f8dd59e733a7a11
```
# 注意事項
- 事前に取得したいチャンネルに対応するNotionページを追加してそのIDを環境変数に入れる必要あり
