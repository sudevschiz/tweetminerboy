import twitter_scrape as ts
import os


os.chdir("/home/schirappat/tweet_miner_boy/company_handles/")
searchList = ["journey mapping software","customer experience","journey mapping","#CX","#customerjourneymapping","#CustomerJourney", "#CustomerExperience",'"customer experience" AND "journey mapping"',"@forrester","@IDC","@HfSResearch","@Mapovate","@SuiteCX","@TandemSeven","@dtnpf","@symantec","@NortonOnline","@PCGPPL"]
    
for item in searchList:
    ts.fetch_tweets(item)    
