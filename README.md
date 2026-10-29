# Rules Left Behind — 自動公開システム

毎日 18:00（日本時間）に GitHub Actions が動き、次の流れをすべて自動で行います。費用は ¥0 です。

1. **AIが話を考える**（Gemini無料枠）：オリジナルのサバイバルミステリーを台本＋場面指定の形式で執筆 → AI編集者が矛盾・安全性・他チャンネルとの類似をチェックして修正 → 形式チェック（語数・場面数・Shortsの範囲など）に通るまで最大4回やり直し
2. **動画にする**：場面パーツから絵を描画 → ナレーション → 長尺（字幕付き）→ その内容のShorts → サムネイル
3. **品質チェック**（長さ・黒画面）→ 合格したら長尺とShortsを公開

予定表（queue.json）に今日の回がすでにあればそれを使い、なければAIが新しく書きます。

## 仕組み
- `engine/write_story.py` …… AIが毎日の話を書く（ルールは `engine/story_spec.md`。ここを編集すると作風を変えられます）
- `engine/kit.py` …… 場面パーツ（屋外・室内・小物・人物・ルール帳・図解）から絵を描く
- `episodes/<名前>/` …… 1話分の台本（story.py）・絵（scenes.py）・タイトル等（meta.json）。AIが書いた回も自動でここに保存されます
- `queue.json` …… 公開の予定表。日付が来た話から自動で公開（止めたい話だけ `"approved": false` にする）
- `build.sh` …… 1話を組み立て（長尺 + Shorts + 英語字幕）。長さ・黒画面チェックに落ちたら投稿しない
- `publish.py` …… YouTube へアップロード（長尺 → 字幕 → サムネ → Shorts。Shortsの説明欄に長尺へのリンクを自動記載）
- 公開範囲は GitHub の変数 `PUBLISH_PRIVACY` で切替。**初期値は public（自動公開）**。止めたいときは private にする

## 初期設定（田村さんの作業・約30分）
APIキーやトークンは、**チャットに貼らず** GitHub の Secrets に直接入力してください。

### 1. GitHub
1. GitHub で新しいリポジトリ `rules-left-behind` を作成（**Public推奨**：Actionsの実行時間が無料で無制限。Privateだと月2,000分の上限があり毎日投稿だと足りなくなる可能性があります。秘密情報はSecretsに入るのでコードが公開されても問題ありません）
2. このフォルダの中身を「Add file → Upload files」でアップロード
   - Macでは `.github` フォルダが隠れています。Finderで **Cmd + Shift + .（ピリオド）** を押すと表示されます

### 2. Google Cloud（Shunto519 や Tiny Twist とは別の新しいプロジェクト）
1. 新規プロジェクト `rules-left-behind` を作成
2. 「YouTube Data API v3」を有効化
3. 「OAuth同意画面」：外部 → 自分をテストユーザーに追加 → **公開ステータスを「本番環境」にする**
   （「テスト」のままだと、認証が7日で切れて自動投稿が止まります）
4. 「認証情報」→ OAuthクライアントID →「デスクトップアプリ」→ JSONをダウンロード（client_secret.json）

### 3. 更新トークンの取得（自分のパソコンで1回だけ）
```
pip install google-auth-oauthlib
python get_refresh_token.py client_secret.json
```
ブラウザで shunto.sid@gmail.com を選び、**チャンネル「Rules Left Behind」を選択**してください（ここを間違えると別チャンネルに投稿されます）。

### 4. GitHub に登録（Settings → Secrets and variables → Actions）
- Secrets：`YT_CLIENT_ID` / `YT_CLIENT_SECRET`（client_secret.json内の値）、`YT_REFRESH_TOKEN`（手順3で表示された値）、`GEMINI_API_KEY`（下記）
- **Gemini APIキー**：Google AI Studio（aistudio.google.com）→「Get API key」→ 新しいプロジェクトで作成。**課金（請求先アカウント）は設定しないでください**（無料枠のまま使います。無料枠では入力内容がGoogleの改善に使われる場合があります）
- Variables：設定不要（自動で公開）。一時停止したいときだけ `PUBLISH_PRIVACY` = `private` を追加

### 5. 動作確認
第1話は **2026-10-30 の18:00 に自動公開**される設定になっています。すぐ試したいときは Actions → daily-publish →「Run workflow」。
約1〜1.5時間後に長尺とShortsがチャンネルに出ていれば成功です。生成した動画は Actions の「Artifacts」からも7日間ダウンロードできます。

## 公開について（重要）
- Googleの審査（API監査）を通していないプロジェクトからアップした動画は、YouTube側で**非公開に固定**されることがあります。
  自動で「公開」まで行うには、YouTube API Services の監査申請（無料）が必要になる場合があります。それまでは
  「非公開でアップ → 田村さんが Studio で公開に切り替え」で運用できます。
- 新しい回を追加するときは `episodes/` にフォルダを置き、`queue.json` に公開日を書くだけで自動公開されます。

## 既知の制限
- **AIの話はまだ実地テストしていません。** この環境からGeminiに接続できなかったため、話を書く部分は形式チェックと絵の描画までを確認済みで、実際にGeminiが書いた回での通しテストは初回実行時になります。最初の数日は、公開された回を見て気になる点を教えてください。`story_spec.md` を直して改善します。
- 絵は場面パーツの組み合わせなので、第1話（1話専用に描いた絵）ほど作り込まれていません。
- AIが話を書けなかった日（形式チェックに4回落ちた日など）は、その日は投稿されません（Actionsが失敗として通知されます）。
- YouTubeの収益化審査では、似た作りの動画を大量に出すチャンネルは不利になることがあります。数字を見ながら作風ルールを調整していきましょう。
