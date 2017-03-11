import re, io
from html import unescape


with io.open('dp.html', 'r', encoding='utf-8') as f:
 html = f.read()



# *?は*と同様だが、なるべく短い文字列にマッチすることを表すメタ文字
for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
  # 書籍のURLはitemprop="url"という属性を持つa要素のhref属性から取得する
  url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
  url = 'https://gihyo.jp' + url # /で始まっているのでドメイン名などを取得する

  # 書籍のタイトルはitemprop="name"という属性を持つp要素から取得する
  title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
  title = title.replace('<br/>', ' ') # <br/>タグをスペースに置き換える。str.replace()は文字列を置換する
  title = re.sub(r'<.*?>', '', title) # タグを取り除く
  title = unescape(title) # 文字参照を元に戻す

  print(url, title)

