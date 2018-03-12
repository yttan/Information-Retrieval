import logging
from datamodel.search.Ytan5_datamodel import Ytan5Link, OneYtan5UnProcessedLink, add_server_copy, get_downloaded_content
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter, ServerTriggers
from lxml import html,etree
import re, os
from time import time
from uuid import uuid4

from urlparse import urlparse, parse_qs, urljoin
from uuid import uuid4
subdomains = {}
invalidcount = 0
maxpage = None
maxoutcount = 0
logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"
#TRAP_POOL = {"calendar.ics.uci.edu"}
TRAP_POOL = {"calendar.ics.uci.edu","tippersweb.ics.uci.edu/research","vision.ics.uci.edu/datasets/db.all.sift","www.ics.uci.edu/informatics/news/news_2007.php","www.ics.uci.edu/~franz","www.ics.uci.edu/~rickl","www.ics.uci.edu/~irishabh","www.ics.uci.edu/facebook","www.ics.uci.edu/computerscience/sitemap.php","seal.ics.uci.edu/projects/covert/GooglePlay_ICC_allSols.txt","seal.ics.uci.edu/projects/covert/Covert-Web-1.0.war","www.ics.uci.edu/computerscience/news/news_2006.php","www.ics.uci.edu/ugrad/policies/Computer_Acct_Backup.php","vision.ics.uci.edu/people/34.html"}
@Producer(Ytan5Link)
@GetterSetter(OneYtan5UnProcessedLink)
@ServerTriggers(add_server_copy, get_downloaded_content)
class CrawlerFrame(IApplication):

    def __init__(self, frame):
        self.starttime = time()
        self.app_id = "Ytan5"
        self.frame = frame


    def initialize(self):
        self.count = 0
        l = Ytan5Link("http://www.ics.uci.edu/")
        print l.full_url
        self.frame.add(l)

    def update(self):
        global subdomains
        global invalidcount
        global maxpage
        global maxoutcount
        unprocessed_links = self.frame.get_new(OneYtan5UnProcessedLink)
        if unprocessed_links:
            link = unprocessed_links[0]
            print "Got a link to download:", link.full_url
            downloaded = link.download()
            myurl = urlparse(link.full_url)
            subdomain = myurl.hostname.split('.uci.edu')[0]
            links = extract_next_links(downloaded)
            if len(links) > maxoutcount:
                maxoutcount = len(links)
                maxpage = link.full_url
            if subdomain not in subdomains:
                subdomains[subdomain] = 1
            else:
                subdomains[subdomain] += 1
            f = open("result.txt","w")
            fcontent = ["subdomains: ","\n",str(subdomains),"\n","max out links page:","\n",str(maxpage),"\n","invalid urls","\n",str(invalidcount)]
            f.writelines(fcontent)
            f.close()
            for l in links:
                if is_valid(l):
                    self.frame.add(Ytan5Link(l))
                    
            
             
            
    def shutdown(self):
        print (
            "Time time spent this session: ",
            time() - self.starttime, " seconds.")

def extract_next_links(rawDataObj):
    outputLinks = []
    '''
    rawDataObj is an object of type UrlResponse declared at L20-30
    datamodel/search/server_datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded.
    The frontier takes care of that.

    Suggested library: lxml
    '''
    global invalidcount
    if rawDataObj.http_code != 200 or (rawDataObj.error_message != None and rawDataObj.error_message != '') or rawDataObj.is_redirected:
        return outputLinks
    # Credit: https://github.com/gjwGithub/search-engine/blob/master/generateGraph.py
    webpage = etree.HTML(rawDataObj.content)
    hrefs = webpage.xpath(u"//a")
    for href in hrefs:
        rawHref = href.get("href")
        absHref = urljoin(rawDataObj.url, rawHref)
        if is_valid(absHref):
            if absHref[-1] != "/":
                absHref += "/"
            outputLinks.append(absHref)
        else:
            invalidcount += 1
    return outputLinks

def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be
    downloaded or not.
    Robot rules and duplication rules are checked separately.
    This is a great place to filter out crawler traps.
    '''
    # Credit: https://github.com/jma19/WebCrawler/blob/master/python/applications/search/crawler_frame.py
    if url == None or url == '':
        return False
    for trap in TRAP_POOL:
        if url.__contains__(trap):
            return False
    if url.__contains__('?'):
        return False
    if url.__contains__("../"):
        return False
    #if not (url.endswith(".html") or url.endswith(".xml") or url.endswith(".php")):
    #    return False
    parsed = urlparse(url)
    if parsed.scheme not in set(["http", "https"]):
        return False
    try:
        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False
