from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import boto3
from botocore.exceptions import ClientError

import re
import os
import requests
import bs4 as BeautifulSoup

import mmap
import sys
import http.client

session = boto3.Session(profile_name='sw')

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
    s3_client = session.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={"ACL": "public-read", 'ContentType': "text/html"})
    except ClientError:
        return False
    return True


def sendDiscord( message, webhook ):
 
    # compile the form data (BOUNDARY can be anything)
    formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------:::BOUNDARY:::--"
  
    # get the connection and make the request
    connection = http.client.HTTPSConnection("discordapp.com")

    try:
        connection.request("POST", webhook, formdata, {
            'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
            'cache-control': "no-cache",
            })
    except:
        pass
  
    # get the response
    response = connection.getresponse()
    result = response.read()
  
    # return back to the calling function with the result
    return result.decode("utf-8")

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome(chrome_options=chrome_options) #replace with .Firefox(), or with the browser of your choice
url = "https://www.withhive.com/help"
browser.get(url) #navigate to the page
innerHTML = browser.execute_script("return document.body.innerHTML")

soup = BeautifulSoup.BeautifulSoup(innerHTML, 'lxml')

embeded = '<html>'
embeded += '<head><style type="text/css">@charset "UTF-8";[ng\:cloak],[ng-cloak],[data-ng-cloak],[x-ng-cloak],.ng-cloak,.x-ng-cloak,.ng-hide{display:none !important;}ng\:form{display:block;}</style>'\
        '    <!--[if lte IE 7]>'\
        '     <script src="http://cdnjs.cloudflare.com/ajax/libs/json2/20130526/json2.js"></script>'\
        '    <![endif]-->'\
        '   <!--[if lte IE 8]>'\
        '     <script src="http://bestiejs.github.io/json3/lib/json3.js"></script>'\
        '    <![endif]-->'\
        '    <!-- Le HTML5 shim, for IE6-8 support of HTML elements -->'\
        '    <!--[if lt IE 9]>'\
        '           <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>'\
        '   <![endif]-->'\
        '    <!-- Le styles -->'\
        '   <meta charset="utf-8">'\
        '   <meta http-equiv="X-UA-Compatible" content="IE=edge">'\
        ''\
        '   <!-- for Facebook && googleplus-->'\
        '   <meta property="og:title" content="HIVE: Mobile Gaming\'s Home Sweet Home!">'\
        '   <meta property="og:type" content="article">'\
        '   <meta property="og:image" content="//image-glb.qpyou.cn/hubweb/contents/hive_logo_256.png">'\
        '   <meta property="og:url" content="http://www.withhive.com/help/notice_view/33807">'\
        '   <meta property="og:description" content="">'\
        ''\
        '   <!-- for Twitter -->'\
        '   <meta name="twitter:card" content="summary">'\
        '   <meta name="twitter:title" content="HIVE: Mobile Gaming\'s Home Sweet Home!">'\
        '   <meta name="twitter:description" content="">'\
        '   <meta name="twitter:image" content="//image-glb.qpyou.cn/hubweb/contents/hive_logo_256.png">'\
        ''\
        '    <!-- for weibo -->'\
        '    <meta property="wb:webmaster" content="004a156e336d778e">'\
        ''\
        '   <title>Event Tendanci.eu</title>'\
        '<!--<script type="text/javascript" src="//image-glb.qpyou.cn/hubweb/pcweb/20190620000000/js/external/jquery-1.7.2.min.js?31"></script>-->'\
        '   <script type="text/javascript" async="" src="https://www.google-analytics.com/analytics.js"></script><script type="text/javascript" src="//image-glb.qpyou.cn/hubweb/pcweb/20190620000000/js/external/jquery-1.7.2.min.js?1443170166"></script>'\
        '   '\
        ' <!--  <link rel="stylesheet" href="/resource/current/css/font.css?31" type="text/css" /> -->'\
        '   <link rel="stylesheet" href="//image-glb.qpyou.cn/hubweb/font/font.css" type="text/css">'\
        '   '\
        '       '\
        '   '\
        '       <link rel="stylesheet" href="//image-glb.qpyou.cn/hubweb/pcweb/20190620000000/css/ui_v1.css?31" type="text/css">'\
        '       '\
        '   <link rel="stylesheet" href="//image-glb.qpyou.cn/hubweb/pcweb/20190620000000/css/toastr.css?31" type="text/css">'\
        '   '\
        '   '\
        '   <script type="text/javascript" src="//image-glb.qpyou.cn/hubweb/pcweb/20190620000000/js/external/angular.min.js?31"></script>'\
        '   <script type="text/javascript" src="//image-glb.qpyou.cn/hubweb/pcweb/20190620000000/js/external/toastr.js?31"></script>'\
        '   <script type="text/javascript" src="//image-glb.qpyou.cn/hubweb/pcweb/20190620000000/js/hub/hive_plugin.js"></script>'\
        ''\
        '   <!--<script type="text/javascript" src="http://wcs.naver.net/wcslog.js"></script>-->'\
        '   <script type="text/javascript" src="//wcs.naver.net/wcslog.js"></script>'\
        '   <script type="text/javascript">'\
        '   if(!wcs_add) var wcs_add = {};'\
        '   wcs_add["wa"] = "a3ed84e4af75bc";'\
        '   wcs_do();'\
        '   </script>'\
        ''\
        '            <!-- Global Site Tag (gtag.js) - Google Analytics -->'\
        '        <script async="" src="https://www.googletagmanager.com/gtag/js?id=UA-106958063-1"></script>'\
        '        <script>'\
        '            window.dataLayer = window.dataLayer || [];'\
        '            function gtag(){dataLayer.push(arguments)};'\
        '            gtag(\'js\', new Date());'\
        ''\
        '            gtag(\'config\', \'UA-106958063-1\');'\
        '        </script>'\
        '    '\
        '</head><body><br /><br /><center><div style="width: 75%;">'\

eventLinks = []

for link in soup.find_all('a'):
    if '/help/notice_view/' in link.get('href') and 'Event' in str(link):
            if 'ummoner' in str(link):
                # urls = re.findall('https://www.withhive.com(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url)
                r = requests.get('https://www.withhive.com' + link['href'])

                print(link['href'])

                soupEvent = BeautifulSoup.BeautifulSoup(r.content, 'lxml')
                embeded += str(soupEvent.find_all('div', class_='notice_view')[0])

                eventLinks.append({"title": str(soupEvent.find_all('h3', class_='title')[0]), "link": 'https://www.withhive.com' + link['href']})

                # sendDiscord('Nouvel event : https://wwww.withhive.com' + str(link['href']), os.environ["discord_aldanet_webhook"])
                # sendDiscord('Nouvel event : ' + str(link), os.environ["discord_unicorn_webhook"])


# eventCount = 0

try:
    session.client('s3').download_file(os.environ['bucket'], 'history_events__23456765432.txt', '/tmp/history_events__23456765432.txt')
except:
    f = open('/tmp/history_events__23456765432.txt', 'w') # to clear the file
    f.write('NEW')
    f.close()


f = open('/tmp/history_events__23456765432.txt', "a+")

messageCount = 0
with open('/tmp/history_events__23456765432.txt', 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
    for event in eventLinks:
        if s.find(bytes(event['link'], encoding='utf-8')) != -1:
            print('true ' + event['link'])
        else:
            print('false ' + event['link'])

            sendDiscord('Nouvel event : ' + str(event['title']) + ' \\r\\n ' + str(event['link']), os.environ["discord_aldanet_webhook"])
            # sendDiscord('Nouveau code : ' + str(link) + ' // Code OldSchool : ' + str(link).replace('https://withhive.me/313/', '').replace('http://withhive.me/313/', '').replace(')', '').replace('(', ''), os.environ["discord_unicorn_webhook"])
            messageCount += 1

            # File append
            f.write("%s\r\n" % event['link'])


if messageCount > 0:
    sendDiscord('@everyone v\'la des events tout neufs ! :-)', os.environ["discord_aldanet_webhook"])
    # sendDiscord('@here v\'la des codes tout neufs ! :-)', os.environ["discord_unicorn_webhook"])

f.close
f = open('/tmp/history_events__23456765432.txt', "r")
tailed = tail(f, lines=50)
f.close()
f = open('/tmp/history_events__23456765432.txt', 'w') # to clear the file
f.write(tailed)
f.close()
upload_file("/tmp/history_events__23456765432.txt", os.environ['bucket'], "history_events__23456765432.txt")



embeded += '</div></center></body></html>'
with open("/tmp/events.html", 'w') as f:
            f.write(embeded)
