import re
import sqlite3
from urllib.request import urlopen
from html import unescape

def main():
  html = fetch('http://gihyo.jp/dp')
  books = scrape(html)
  save('books.dp', books)

def fetch(url):
  f = urlopen(url)
  # HTTPヘッダーからエンコーディングを取得する
  encoding = f.info().get_content_charset(failobj="utf-8")
  html = f.read().decode(encoding) # 得られたエンコーディングを指定して文字列にデコードする
  return html

def scrape(html):
  books = []
  for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
    # 書籍のURLはitemprop="url"という属性を持つa要素のhref属性から取得する
    url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
    url = 'https://gihyo.jp' + url # /で始まっているのでドメイン名などを追加する

    # 書籍のタイトルはitemprop="name"という属性を持つp要素から取得する
    title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
    title = re.sub(r'<.*?>', '', title) # タグを取り除く
    title = unescape(title) # 文字参照を元に戻す

    books.append({'url': url, 'title': title})
    return books

def save(dp_path, books):
  conn = sqlite3.connect(dp_path) # データベースを開き、コネクションを取得する
  c = conn.cursor() # カーソルを取得する
  # execute()メソッドでSQL文を実行する
  # このスクリプトを何回実行しても同じ結果になるようにするために、booksテーブルが存在する場合は削除する
  c.execute('''
    CREATE TABLE books (
      title text,
      url text
      )
  ''')

  # executemany()メソッドでは複数のパラメーターをリストで指定できる
  c.executemany('INSERT INTO books VALUES (:title, :url)', books)
  conn.commit() # 変更をコミット(保存)する
  conn.close() # コネクションを閉じる

# pythonコマンドで実行された場合にmain()関数を呼び出す。これはモジュールとして他のファイルから
# インポートされたときに、main()関数が実行されないようにするための、Pythonにおける一般的なイディオム
if __name__ == '__main__':
  main()
