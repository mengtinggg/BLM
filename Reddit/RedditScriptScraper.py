import requests
import praw
import time
import datetime as dt
import pandas as pd
import json

reddit = praw.Reddit(client_id='enter client_id', \
                     client_secret='enter client_secret key', \
                     user_agent='enter user agent', \
                     username='enter reddit username', \
                     password='enter reddit password')

subreddit = reddit.subreddit('BlackLivesMatter')

startDate = dt.datetime(2014, 1, 1) #change this to date and time you want format is YYYY, MM, DD
startDateUnix = time.mktime(startDate.timetuple())
endDate = dt.datetime(2015,10,15,8,5,57)
endDateUnix = time.mktime(endDate.timetuple())

def submissions_pushshift_praw(subreddit, start=None, end=None, limit=100, extra_query=""):
    """
    A simple function that returns a list of PRAW submission objects during a particular period from a defined sub.
    This function serves as a replacement for the now deprecated PRAW `submissions()` method.
    
    :param subreddit: A subreddit name to fetch submissions from.
    :param start: A Unix time integer. Posts fetched will be AFTER this time. (default: None)
    :param end: A Unix time integer. Posts fetched will be BEFORE this time. (default: None)
    :param limit: There needs to be a defined limit of results (default: 100), or Pushshift will return only 25.
    :param extra_query: A query string is optional. If an extra_query string is not supplied, 
                        the function will just grab everything from the defined time period. (default: empty string)
    
    Submissions are yielded newest first.
    
    For more information on PRAW, see: https://github.com/praw-dev/praw 
    For more information on Pushshift, see: https://github.com/pushshift/api
    """
    matching_praw_submissions = []
    
    # Default time values if none are defined (credit to u/bboe's PRAW `submissions()` for this section)
    utc_offset = 28800
    now = int(time.time())
    start = max(int(start) + utc_offset if start else 0, 0)
    end = min(int(end) if end else now, now) + utc_offset
    
    if limit > 1000:
        link_limit = 1000
    else:
        link_limit = limit

    count = 0
    check_count = 0
    check_once = False

    while count < limit:
        try:
            # Format our search link properly.
            search_link = ('https://api.pushshift.io/reddit/submission/search/'
                        '?subreddit={}&before={}&sort_type=created_utc&sort=desc&limit={}&q={}')
            search_link = search_link.format(subreddit, end, link_limit, extra_query)
            
            # Get the data from Pushshift as JSON.
            retrieved_data = requests.get(search_link)
            returned_submissions = json.loads(retrieved_data.text)['data']

            end = returned_submissions[-1]["created_utc"]

            # Iterate over the returned submissions to convert them to PRAW submission objects.
            for submission in returned_submissions:
                # Take the ID, fetch the PRAW submission object, and append to our list
                praw_submission = reddit.submission(id=submission['id'])

                if praw_submission not in matching_praw_submissions:
                    matching_praw_submissions.append(praw_submission)
                count += 1
            
            # last_id = matching_praw_submissions[-1].id
            print("Pushshift Crawled",len(matching_praw_submissions))


            # start = returned_submissions[-1]["created_utc"]

            if start > end:
                print("No more Submissions")
                break
            
            if check_once:
                check_count += 1
                
                if check_count == 5:
                    check_once = False
                    check_count = 0

        except:
            if check_once:
                print("Exception Caught again saving ...")
                break
            else:
                check_once = True
                print("Exception Caught retrying ...")

     
    # Return all PRAW submissions that were obtained.
    return matching_praw_submissions

topics_dict = { "author": [],
                "title":[],
                "score":[],
                "id":[], "url":[],
                "comms_num": [],
                "created": [],
                "body":[],
                "comments": []}

submission_count = 0

matching_submissions = submissions_pushshift_praw("", start = startDateUnix, end = endDateUnix, limit=100000, extra_query="blacklivesmatter")

for submission in matching_submissions:
    try:
        topics_dict["author"].append(submission.author)
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score) #number of upvotes
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments) #number of comments
        # topics_dict["created"].append(submission.created)
        topics_dict["created"].append(dt.datetime.fromtimestamp(submission.created)) #date time created in normal time format
        topics_dict["body"].append(submission.selftext)
        comment_string = ""
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            comment_string += (comment.body)+"\n\n"
        topics_dict["comments"].append(comment_string)
        submission_count += 1
        print("{} Submission Scraped".format(submission_count))
    except:
        submission_count+= 1
        print("Submission Failed:",submission_count)
        pass

    if submission_count == len(matching_submissions) or submission_count % 1000 == 0:
        topics_data = pd.DataFrame(topics_dict)
        print("Writing to file")
        topics_data.to_csv('Reddit2015andBefore.csv')



# topics_data = pd.DataFrame(topics_dict)
# print(topics_data)
# topics_data.to_csv('RedditTrial.csv')