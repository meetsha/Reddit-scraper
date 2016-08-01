from newspaper import Article
import requests
import json
import csv

def scrapeReddit(subreddit):
    reddit_url = "http://www.reddit.com/r/%s.json?sort=top&t=day/"%subreddit
    headers = {'User-Agent' : 'short_description_of_yourself user:uiandgame'}
    reddit_json = json.loads(requests.get(reddit_url,headers=headers).text) 

    news_arr = []

    for i in reddit_json["data"]["children"][:40]:
        if i['data']['is_self'] == True: continue
        if i['data']['over_18'] == True: continue
        title = i["data"]["title"]
        title = title.encode('ascii',errors='ignore').strip()
        url = i["data"]["url"]
        article_content = nlp(url)
        if not article_content:
            continue
        else:
            news_arr.append(article_content)
    
    # with open

    myfile = open('data.csv','wb')
    writer = csv.writer(myfile, delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)

    for row in news_arr:
        writer.writerow(row)

def nlp(link):
    print link
    try:
        article = Article(link)
        article.download()
        article.parse()
        article.nlp()
        if not article.has_top_image():
            print "Does not have a top image, skipping this article"
            return None

        source = article.source_url
        source = source.replace("www.","")
        source = source.replace("http://","")

        image_url = article.top_image
        title = article.title
        title = title.encode('ascii',errors='ignore').strip()
        summary = article.summary
        summary = summary.encode('ascii',errors='ignore').strip()

        news_data = [title,link,image_url,summary]
    
    except:
        print "Exception occured: ignoring this link"
        news_data = None

    return news_data

def get_dict(**kwargs): #takes as many arguments and makes a dictionary of them with same key value pairs
    d = {}
    for k,v in kwargs.iteritems():
        d[k] = v
    return d

def spreadsheet_query():
    url = "https://spreadsheets.google.com/feeds/list/1ieAk09bpe2u5ET1dmjbdwNLxwU3gOwXNTUpDq17DaEk/od6/public/values?alt=json"
    json_ob = requests.get(url).json()
    arr = []
    for i in json_ob["feed"]["entry"]:
        d = {}
        title = i["gsx$title"]["$t"]
        image_url = i["gsx$imageurl"]["$t"]
        link = i["gsx$link"]["$t"]
        summary = i["gsx$summary"]["$t"]
        d = get_dict(link=link,image_url=image_url,summary=summary,title=title)
        arr.append(d)
    return arr
            

if __name__ == '__main__':
    #scrapeReddit(subreddit='worldnews')
    print spreadsheet_query()

     
