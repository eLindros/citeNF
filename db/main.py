#%%
import pandas as pd

bookends = pd.read_json(r'NutritionFacts.json') 

videos = pd.read_json(r'videos.jsonl', lines=True)
videos["keywords"] = videos["keywords"].apply(lambda row: '\n'.join(row))
videos["url2"] = videos["url"].apply(lambda rw: rw[:-1])

joinvids = videos[["url2", "keywords"]]

newbookends = pd.merge(bookends, joinvids, how='left', left_on='user1', right_on='url2')

newbookends.drop("url2", axis=1)

newbookends.drop_duplicates()

newbookends.to_json("newbookends.bex", orient='records')

