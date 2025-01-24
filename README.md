# README

## 概要 / Overview

このプログラムは、指定されたWikiページのダウンロードやアップロードを行うためのスクリプトです。ファイルの移動、Wikiページの編集、添付ファイルのアップロード機能を備えています。

This program is a script for downloading and uploading specified Wiki pages. It includes functions for moving files, editing Wiki pages, and uploading attachments.

---

## 必要要件 / Requirements

- Python 3.x
- 必須ライブラリ / Required Libraries:
  - `requests`
  - `requests_toolbelt`
  - `dotenv`
  - `beautifulsoup4`

以下のコマンドで必要なライブラリをインストールできます:
You can install the required libraries using the following command:
```bash
pip install requests requests_toolbelt python-dotenv beautifulsoup4
```

---

## 環境設定 / Environment Setup

1. `.env`ファイルを作成し、以下の内容を記載してください:
   Create a `.env` file and include the following content:
   ```plaintext
   WIKI_ENDPOINT=<Your Wiki Endpoint>
   WIKI_USER=<Your Wiki Username>
   WIKI_PASS=<Your Wiki Password>
   ```

---

## 使用方法 / Usage

### 基本コマンド / Basic Commands

このスクリプトはコマンドラインで動作します。以下のコマンドを使用してください:
This script works from the command line. Use the following commands:

### 1. アップロードモード / Upload Mode

指定されたファイルをWikiページにアップロードし、添付ファイルも処理します。
Uploads the specified file to a Wiki page and handles attachments.
```bash
python script.py u <file_path>
```

#### 引数 / Arguments
- `file_path`:
  アップロードするテキストファイルのパス。
  Path to the text file to be uploaded.

### 2. ダウンロードモード / Download Mode

指定されたWikiページの内容をダウンロードし、ローカルのテキストファイルに保存します。
Downloads the content of the specified Wiki page and saves it to a local text file.
```bash
python script.py d <page_name>
```

#### 引数 / Arguments
- `page_name` (オプション / Optional):
  ダウンロード対象のWikiページ名。指定しない場合、最新ページが取得されます。
  Name of the Wiki page to download. If omitted, the latest page will be retrieved.

---

## 主な機能 / Key Features

### ファイルアップロード / File Upload

- 指定されたWikiページに関連ファイルをアップロードします。
- アップロード進捗をリアルタイムで表示します。
- Moves specified files to an archival folder (`_old`) after uploading.

### ページダウンロード / Page Download

- Wikiページの内容を取得し、ローカルに保存します。
- Downloads Wiki page content and saves it locally.

### 最新ページ取得 / Get Latest Page

- 最新のWiki投稿ページを自動的に取得します。
- Automatically retrieves the latest Wiki post page.

---

## 注意点 / Notes

- Wikiのエンドポイント、ユーザー名、パスワードは環境変数で設定してください。
- 環境変数の設定が正しくない場合、エラーが発生します。
- Ensure the Wiki endpoint, username, and password are correctly set in the environment variables.
- Errors may occur if environment variables are not properly configured.

---

## サンプル出力 / Sample Output

### アップロード / Upload
```
ファイル 'example.txt' をアップロードします。
アップロード進捗: 1024/2048 bytes (50.0%)
ファイル 'example.txt' を正常にアップロードしました。
'example.txt' は '_old/example_20250101_120000.txt'へ移動されました。
```

### ダウンロード / Download
```
テキストエリアの内容がexample_page.txtに保存されました。
```

---

## 問題の報告 / Reporting Issues

バグや改善提案がある場合は、プロジェクト管理者に報告してください。
If you encounter any bugs or have suggestions for improvement, please report them to the project administrator.