import os
import sys
import shutil
import re
import argparse
import requests
from dotenv import load_dotenv
from datetime import datetime
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

# 環境変数取得
load_dotenv()
wiki_endpoint = os.getenv("WIKI_ENDPOINT")
wiki_pass = os.getenv("WIKI_PASS")
wiki_user = os.getenv("WIKI_USER")


def upload_files(page_name, files):
    # アップロードURL
    upload_url = f"{wiki_endpoint}"

    for file_path in files:
        total_size = os.path.getsize(file_path)  # ファイルサイズ取得
        current_size = 0

        def callback(monitor):
            """送信進捗のコールバック関数"""
            nonlocal current_size
            current_size = monitor.bytes_read
            percentage = (current_size / total_size) * 100
            sys.stdout.write(f"\rアップロード進捗: {current_size}/{total_size} bytes ({percentage:.1f}%)")
            sys.stdout.flush()

        # ファイルデータ
        with open(file_path, "rb") as file:
            files_data = MultipartEncoder(
                fields={
                    "plugin": "attach",
                    "pcmd": "post",
                    "refer": page_name,
                    "pass": wiki_pass,
                    "encode_hint": "ぷ",
                    "attach_file": (os.path.basename(file_path), file, "application/octet-stream"),
                }
            )

            # 進捗を監視するためのMonitor
            monitor = MultipartEncoderMonitor(files_data, callback)

            print(f"\nファイル '{os.path.basename(file_path)}' をアップロードします。")

            # POSTリクエストでファイルをアップロード
            response = requests.post(upload_url, data=monitor, headers={'Content-Type': monitor.content_type})


            if response.status_code == 200:
                print(f"\nファイル '{os.path.basename(file_path)}' を正常にアップロードしました。")
            else:
                print(f"ファイル '{os.path.basename(file_path)}' のアップロードに失敗しました。ステータスコード: {response.status_code}")



def move_file(source_file, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    base_name = os.path.basename(source_file)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    name, ext = os.path.splitext(base_name) 
    new_file_name = f"{name}_{timestamp}{ext}"

    destination_file = os.path.join(destination_folder, new_file_name)

    shutil.move(source_file, destination_file)
    print(f"'{source_file}' は '{destination_file}'へ移動されました。")


### 上：ファイル処理関連 / 下：wiki処理関連 ###


def download_page(args):
    page_name = args.page_name
    # 対象のURL
    url = f"{wiki_endpoint}?cmd=edit&page={page_name}"

    # リクエストを送信してページを取得
    response = requests.get(url)
    response.raise_for_status()  # リクエストが成功したか確認

    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(response.content, "html.parser")

    # テキストエリアを適切なセレクタで取得
    textarea = soup.find("textarea", {"name": "msg"})

    if textarea is not None:
        # テキストエリアの内容を取得
        text_content = textarea.get_text()

        # テキストをファイルに保存
        with open(f"{page_name}.txt", "w", encoding="utf-8") as file:
            file.write(text_content)

        print(f"テキストエリアの内容が{page_name}.txtに保存されました。")
    else:
        print("テキストエリアが見つかりませんでした。")


def upload_page(args):
    # セッションを作成
    session = requests.Session()

    # パスからファイルを取得
    file_path = args.file_path
    page_name = os.path.splitext(os.path.basename(file_path))[0]
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except IOError:
        print(f"ファイル '{file_path}' を読み込むことができませんでした。")
        sys.exit(1)

    pattern = r"#ref\((\./[^,]+),[^)]+\);"
    upload_files_name = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                image_path = match.group(1)
                # マッチした文字列全体を確認し、`;` の後に `-` があればスキップ
                if re.search(r";-", line):
                    continue
                upload_files_name.append(image_path)


    # 編集ページのURL
    edit_page_url = f"{wiki_endpoint}?cmd=edit&page={page_name}"

    # 編集ページを開いてdigest値を取得
    response = session.get(edit_page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # digest値の取得
    digest_input = soup.find("input", {"name": "digest"})
    if not digest_input:
        print("digest値の取得に失敗しました。")
        sys.exit(1)
    digest_value = digest_input["value"]

    # ページ更新用データの準備
    edit_data = {
        "encode_hint": "ぷ",
        "cmd": "edit",
        "page": page_name,
        "digest": digest_value,
        "msg": content,
        "write": "ページの更新",
        "notimestamp": "true",
    }

    # フォームをPOSTリクエストで送信
    response = session.post(f"{wiki_endpoint}", data=edit_data)

    # ステータスコードを確認
    if response.status_code == 200:
        print(f"ページ '{page_name}' を更新しました。")
        upload_files(page_name, upload_files_name)
        move_file(file_path, "_old")
    else:
        print(f"ページの更新に失敗しました。ステータスコード: {response.status_code}")
        sys.exit(1)


# 最新投稿をサーチ
def getLatestPage():
    # URLのHTMLを取得
    response = requests.get(f"{wiki_endpoint}?{wiki_user}")
    response.raise_for_status()  # ステータスコードが200以外の場合にエラーを発生させる

    soup = BeautifulSoup(response.content, "html.parser")
    element_id = "list_9" # 最新の投稿のID
    element = soup.find("a", id=element_id)
    if element:
        print(f"最新データの{element.get_text(strip=True)}を取得します。")
        return element.get_text(strip=True)
    else:
        print(f"ID '{element_id}' の要素が見つかりませんでした。")
        sys.exit()


def main():
    parser = argparse.ArgumentParser(description="モードに応じた処理を行います。")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # アップロード用のサブパーサーを作成
    parser_a = subparsers.add_parser("u", help="アップロード用関数")
    parser_a.add_argument("file_path", type=str, help="ファイル名")
    parser_a.set_defaults(func=upload_page)

    # ダウンロード用のサブパーサーを作成
    parser_b = subparsers.add_parser("d", help="ダウンロード用関数")
    parser_b.add_argument(
        "page_name", type=str, help="ページ名", default=getLatestPage(), nargs="?"
    )
    parser_b.set_defaults(func=download_page)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
