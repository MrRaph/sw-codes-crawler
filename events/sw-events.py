from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import re
import requests
import bs4 as BeautifulSoup

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


for link in soup.find_all('a'):
	if '/help/notice_view/' in link.get('href') and 'Event' in str(link):
		if 'ummoner' in str(link):
                    urls = re.findall('/(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url)
                    r = requests.get('https://www.withhive.com' + link['href'])
                    soupEvent = BeautifulSoup.BeautifulSoup(r.content, 'lxml')
                    embeded += str(soupEvent.find_all('div', class_='notice_view')[0])


embeded += '</div></center></body></html>'
with open("/tmp/events.html", 'w') as f:
            f.write(embeded)
