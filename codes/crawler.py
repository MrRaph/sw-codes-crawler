import praw
import os
import re
import time
import boto3
from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={"ACL": "public-read", 'ContentType': "text/html"})
    except ClientError:
        return False
    return True

def crawl(event, context):
    reddit = praw.Reddit(client_id=os.environ['reddit_client_id'],
                        client_secret=os.environ['reddit_client_secret'],
                        user_agent='Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0')

    subreddit = reddit.subreddit('summonerswar')

    embededList = []

    for submission in subreddit.search("withhive.me", sort='recent', time_filter='month', limit=20):
        if 'withhive.me/313/' in submission.selftext:

            embededList.append('<blockquote class="reddit-card" data-card-created="'+ str(time.time()).split(':')[0] +'">'\
            '<a href="' + submission.url + '?ref=share&ref_source=embed">' + submission.title + '</a>'\
            'from <a href="http://www.reddit.com/r/summonerswar">Summoners War</a></blockquote>'\
            '<script async src="https://embed.redditmedia.com/widgets/platform.js" charset="UTF-8"></script><br /><br />')

        for comment in submission.comments:
            if 'withhive.me/313/' in comment.body:
                embededList.append('<a class="embedly-card" href="https://www.reddit.com' + comment.permalink + '">Card</a>'\
                '<script async src="//embed.redditmedia.com/widgets/platform.js" charset="UTF-8"></script>')


    embeded = '<html><head><title>Code Tendanci.eu</title></head><body>'
    for post in embededList[::-1]:
        embeded += post
    embeded += '</body></html>'

    with open("/tmp/index.html", 'w') as f:
        f.write(embeded)

    upload_file("/tmp/index.html", os.environ['bucket'], "index.html")
    # client = boto3.client('cloudfront')
    # response = client.create_invalidation(
    #     DistributionId=os.environ['distribution_id'],
    #     InvalidationBatch={
    #         'Paths': {
    #             'Quantity': 1,
    #             'Items': [
    #                 '/',
    #             ]
    #         },
    #         'CallerReference': str(time.time())
    #     }
    # )

