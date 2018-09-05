import os

import twitter_scrape as ts

newpath = './mined_tweets'
if not os.path.exists(newpath):
    os.makedirs(newpath)

# searchList = ["journey mapping software", "customer experience", "journey mapping", "#CX", "#customerjourneymapping",
#               "#CustomerJourney", "#CustomerExperience", "@forrester", "@IDC", "@HfSResearch", "@Mapovate", "@SuiteCX",
#               "@TandemSeven", "@dtnpf", "@symantec", "@NortonOnline", "@PCGPPL"]
searchList = ["@CMOKerala"]
for item in searchList:
    ts.fetch_tweets(item)
