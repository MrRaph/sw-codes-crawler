import praw
import os
import time
import boto3
import re
import mmap
from botocore.exceptions import ClientError

def tail( f, lines=20 ):
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])

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
    links = []

    for submission in subreddit.search("withhive.me", sort='recent', time_filter='week', limit=20):
        if 'withhive.me/313/' in submission.selftext:

            embededList.append('<blockquote class="reddit-card" data-card-created="'+ str(time.time()).split(':')[0] +'">'\
            '<a href="' + submission.url + '?ref=share&ref_source=embed">' + submission.title + '</a>'\
            'from <a href="http://www.reddit.com/r/summonerswar">Summoners War</a></blockquote>'\
            '<script async src="https://embed.redditmedia.com/widgets/platform.js" charset="UTF-8"></script><br /><br />')

            print(re.findall('http[s]?://withhive.me/313/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', submission.selftext))
            for url in re.findall('http[s]?://withhive.me/313/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', submission.selftext):
                if 'withhive.me/313/' in url:
                    links.append(url)

        for comment in submission.comments:
            if 'withhive.me/313/' in comment.body:
                embededList.append('<a class="embedly-card" href="https://www.reddit.com' + comment.permalink + '">Card</a>'\
                '<script async src="//embed.redditmedia.com/widgets/platform.js" charset="UTF-8"></script>')

                print(re.findall('http[s]?://withhive.me/313/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', comment.body))
                for url in re.findall('http[s]?://withhive.me/313/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', comment.body):
                    if 'withhive.me/313/' in url:
                        links.append(url)


    embeded = '<html><head><title>Code Tendanci.eu</title>'\
   ' <!-- Global site tag (gtag.js) - Google Analytics -->'\
    '<script async src="https://www.googletagmanager.com/gtag/js?id=UA-145085111-1"></script>'\
    '<script>'\
    'window.dataLayer = window.dataLayer || [];'\
    'function gtag(){dataLayer.push(arguments);}'\
    'gtag(\'js\', new Date());'\
    'gtag(\'config\', \'UA-145085111-1\');'\
    '</script>'\
    '</head><body>'
    
    for post in embededList[::-1]:
        embeded += post
    embeded += '</body></html>'

    with open("/tmp/index.html", 'w') as f:
        f.write(embeded)

    embeded = ''

    upload_file("/tmp/index.html", os.environ['bucket'], "index.html")
    
    try:
        boto3.client('s3').download_file(os.environ['bucket'], 'history__23456765432.txt', '/tmp/history__23456765432.txt')
    except:
        pass

    f = open('/tmp/history__23456765432.txt', "a+")

    with open('/tmp/history__23456765432.txt', 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
        for link in links:
            if s.find(bytes(link, encoding='utf-8')) != -1:
                print('true ' + link)
            else:
                print('false ' + link)
                 # SNS Notify
                sns = boto3.client('sns', region_name='eu-west-1')
                sns.publish(PhoneNumber=os.environ['target_arn'], Message=str(link), Subject='New SW Code')
                # File append
                f.write("%s\r\n" % link)
    f.close
    f = open('/tmp/history__23456765432.txt', "r")
    tailed = tail(f, lines=50)
    f.close()
    f = open('/tmp/history__23456765432.txt', 'w') # to clear the file
    f.write(tailed)
    f.close()
    upload_file("/tmp/history__23456765432.txt", os.environ['bucket'], "history__23456765432.txt")


