import os

import twitter_scrape as ts

newpath = './mined_tweets'
if not os.path.exists(newpath):
    os.makedirs(newpath)

# searchList = ["journey mapping software", "customer experience", "journey mapping", "#CX", "#customerjourneymapping",
#               "#CustomerJourney", "#CustomerExperience", "@forrester", "@IDC", "@HfSResearch", "@Mapovate", "@SuiteCX",
#               "@TandemSeven", "@dtnpf", "@symantec", "@NortonOnline", "@PCGPPL"]
searchList = ["@TryCatchExcept"]


def option_one():
    list_string = "\n".join(searchList)
    print("Current fetch list is : \n" + list_string)
    print("Starting fetch...\n")
    for item in searchList:
        ts.fetch_tweets(item)


def option_two():
    handles = input("Input the handle to be fetched. [Input multiple handles using , ]")
    handle_list = handles.split(",")
    print("Starting fetch...")

    # TODO : Different fetching practise for tweets MADE BY a twitter handle
    for item in handle_list:
        print("In progress")
        # ts.fetch_tweets(item)


def option_three():
    handles = input("Input the handle or hashtag to be streamed. [Input multiple handles using , ]")
    handle_list = handles.split(",")
    print("Starting fetch...")

    # TODO : Twitter streaming
    for item in handle_list:
        print("In progress")
        # ts.fetch_tweets(item)


def option_four():
    print("Exiting...")
    return


title = "\n\n=+=+ TWEET MINER +=+=\n\nChoose from options below : \n"

print(title)

print("[1] Fetch all mentions of a hashtag or a handle")
print("[2] Fetch all tweets made by a handle")
print("[3] Stream a hashtag")
print("[4] Exit")

choice = input('Enter your choice [1-4] : ')
print(choice)
choice = int(choice)

print("Option " + str(choice) + " selected.")
if choice == 1:
    option_one()
if choice == 2:
    option_two()
if choice == 3:
    option_three()
if choice == 4:
    option_four()
