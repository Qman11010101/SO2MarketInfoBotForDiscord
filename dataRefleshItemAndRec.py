#Curlを定期実行でもできなくはない気がするので要相談
#もしくは1ファイルに纏める
import urllib.request as urlreq

#商品定義取得
url = "https://so2-api.mutoys.com/master/item.json"
urlreq.urlretrieve(url, 'data/item.json')

#レシピ品取得
url = "https://so2-api.mutoys.com/json/master/recipe_item.json"
urlreq.urlretrieve(url, 'data/rec.json')