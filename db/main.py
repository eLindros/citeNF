import pandas as pd

# Importiere Daten
videos = pd.read_json(r'videos.jsonl', lines=True) # Videos
citations = pd.read_json(r'citations.jsonl', lines=True) # Referenzen
video_citation = pd.read_json(r'video_citation.jsonl', lines=True) # Many2Many Videos Referenzen

# Spiele Referenzen an Videos ran
# Es genügt der Text der Referenz und die URL als Markdown-Link und Liste
for index, row in videos.iterrows():
    citations_of_video = citations.query(video_url == row['url'])
    citation_of_video = ''
    for index, cit in citations_of_video:
        citation_of_video += f"[{cit['citation']}]({cit['url']})\n"


# Lösche Duplikate in Referenzen


# Spiele Video-Urls an Referenzen ran


# Erstelle Markdown-Dateien für Videos


# Erstelle Import-Datei für Bookends

def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"
    return "".join(safe_char(c) for c in s).rstrip("_")

def link_to_keyword_md(s):
    return f"[{s}](https://nutritionfacts.org/topics/{s.replace(' ', '-')}/)"

for index, row in videos.iterrows():
        title = row["title"].split('|')[0]
        safe_title = make_safe_filename(title)
        url = row["url"]
        video = row["video"]
        youtube_id = video.split('/')[-1]
        transcript = row["transcript"]
        youtube = f"[![Youtube Video](http://img.youtube.com/vi/{youtube_id}/0.jpg)](http://www.youtube.com/watch?v={youtube_id})"
        keywords = row["keywords"]
        date = row["date"].split('T')[0].split('-')
        date_locale = ".".join(date.reverse())

        keys = ''

        for keyword in keywords:
            keys += link_to_keyword_md(keyword) + ' + '

        keys = keys[0:-3]


        file = open(f"md/{safe_title}.md", "w", encoding='utf-8')
        
        line = f"# {title}\n[_NutritionFacts.org_]({url})\n\n>{date_locale}\n\n{youtube}\n\n{transcript}\n---\n{keys}"

        file.write(line)
        file.close()


def append_keywords_bex(videos):
    videos["keywords"] = videos["keywords"].apply(lambda row: '\n'.join(row))
    videos["url2"] = videos["url"].apply(lambda rw: rw[:-1])

    joinvids = videos[["url2", "keywords"]]

    bookends = pd.read_json(r'NutritionFacts.json') 
    newbookends = pd.merge(bookends, joinvids, how='left', left_on='user1', right_on='url2')

    newbookends.drop("url2", axis=1)

    newbookends.drop_duplicates()

    newbookends.to_json("newbookends.bex", orient='records')

# append_keywords_bex(videos)