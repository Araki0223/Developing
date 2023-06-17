# --1--
import requests
import json
from pprint import pprint

res = requests.get('https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId=1009993429057254143')

json_data = json.loads(res.text)
pprint(json_data)

import pandas as pd


# mediumカテゴリの親カテゴリの辞書
parent_dict = {}

df = pd.DataFrame(columns=['category1', 'category2', 'category3', 'categoryId', 'categoryName'])

# 大カテゴリ
for category in json_data['result']['large']:
    df = df.append({'category1':category['categoryId'],'category2':"",'category3':"",'categoryId':category['categoryId'],'categoryName':category['categoryName']}, ignore_index=True)

# 中カテゴリ
for category in json_data['result']['medium']:
    df = df.append({'category1':category['parentCategoryId'],'category2':category['categoryId'],'category3':"",'categoryId':str(category['parentCategoryId'])+"-"+str(category['categoryId']),'categoryName':category['categoryName']}, ignore_index=True)
    parent_dict[str(category['categoryId'])] = category['parentCategoryId']

# --2--
# キーワードを含む行を抽出
df_keyword = df.query('categoryName.str.contains("魚")', engine='python')

# --3--
# 「煮魚」カテゴリの人気レシピを取得
res = requests.get('https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1009993429057254143&categoryId=32-339')

json_data = json.loads(res.text)
pprint(json_data)

import time

# 取得したレシピはDataFrameに格納する
df_recipe = pd.DataFrame(columns=['recipeId', 'recipeTitle', 'foodImageUrl', 'recipeMaterial', 'recipeCost', 'recipeIndication', 'categoryId', 'categoryName'])

for index, row in df_keyword.iterrows():
    time.sleep(3) # 連続でアクセスすると先方のサーバに負荷がかかるので少し待つのがマナー

    url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1009993429057254143&categoryId='+row['categoryId']
    res = requests.get(url)

    json_data = json.loads(res.text)
    recipes = json_data['result']

    for recipe in recipes:
        df_recipe = df_recipe.append({'recipeId':recipe['recipeId'],'recipeTitle':recipe['recipeTitle'],'foodImageUrl':recipe['foodImageUrl'],'recipeMaterial':recipe['recipeMaterial'],'recipeCost':recipe['recipeCost'],'recipeIndication':recipe['recipeIndication'],'categoryId':row['categoryId'],'categoryName':row['categoryName']}, ignore_index=True)

