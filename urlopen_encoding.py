import sys, io
from urllib.request import urlopen

f = urlopen('https://gihyo.jp/dp')
# HTTPヘッダーからエンコーディングを取得する
encoding = f.info().get_content_charset(failobj="utf-8")
print('encoding:', encoding, file=sys.stderr) # エンコーディングを標準出力エラーにする
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Here
text = f.read().decode(encoding) # 得られたエンコーディングを指定して文字列にデコードする
print(text)




