#Curlを定期実行でもできなくはない気がするので要相談
#もしくは1ファイルに纏める
import urllib.request as urlreq

#販売品取得
url = "https://so2-api.mutoys.com/json/sale/all.json"
urlreq.urlretrieve(url, 'data/sale.json')

#注文品取得
url = "https://so2-api.mutoys.com/json/request/all.json"
urlreq.urlretrieve(url, 'data/req.json')