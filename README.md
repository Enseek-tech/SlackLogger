# Slackログ保存BOT改

サークルで運用されていたものに比べ
- 省コード化(70%削減)
- 超高速化
- 安定化

[ここに保存されます](https://www.notion.so/148712765bdc804f93edc264dc5898f1?v=7009b6cb45da4e54870df40381b3dd94)

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
