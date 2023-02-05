import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.response import Response
import re
import helpers

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

#reponse = servers reponse to the HTTP request.
def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    #parse webpage and find all links and text
    if resp.status == 200:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        links = soup.find_all("a", href=True)
        text = soup.getText()
    else:
        return []

    #create a prev_urls to read in stored links from previous searches.
    prev_urls = {}
    with open("urls.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line is not None:
                prev_urls[line] = 1

    # We will use the is_valid url function in this loop to make sure
    # we do not add bad urls or previously visited urls. 
    # we create a new_urls to store
    new_urls = {}
    for link in links:
        str_link = link.get('href')
        str_link = str_link.split('#')[0]
        if str_link not in prev_urls and str_link not in new_urls:
            if is_valid(str_link):
                new_urls[str_link] = 1
    
    # Open file again and denote to append to the urls.txt file
    with open('urls.txt', 'a') as f:
        for line in new_urls:
            f.write(line)
            f.write('\n')
    f.close()

    # returns most top 50 most common words thus far.
    top50 = helpers.mostCommon(text)

    # Returns the url with the most words
    url_with_most_words = helpers.longestPage(resp.raw_response.url, text)

    # Store total unique pages
    totalUniquePages = len(prev_urls) + len(new_urls) + 3

    with open("uniquePages.txt", 'w') as f:
        f.write(str(totalUniquePages))

    return new_urls

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if parsed.hostname == None:
            return False
        if not parsed.hostname.endswith(('ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu')):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|wp-json|odc"
            + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()) and not re.search(
                r'(/css/|/js/|/bmp/|/gif/|/jpe?g/|/ico/'
                + r'|/png/|/tiff?/|/mid/|/mp2/|/mp3/|/mp4/'
                + r'|/wav/|/avi/|/mov/|/mpeg/|/ram/|/m4v/|/mkv/|/ogg/|/ogv/|/pdf/|/wp-content/'
                + r'|/ps/|/eps/|/tex/|/ppt/|/pptx/|/ppsx/|/doc/|/docx/|/xls/|/xlsx/|/names/|/wp-login'
                + r'|/data/|/dat/|/exe/|/bz2/|/tar/|/msi/|/bin/|/7z/|/psd/|/dmg/|/iso/|/wp-json/'
                + r'|/epub/|/dll/|/cnf/|/tgz/|/sha1/'
                + r'|/thmx/|/mso/|/arff/|/rtf/|/jar/|/csv/'
                + r'|/rm/|/smil/|/wmv/|/swf/|/wma/|/zip/|/rar/|/gz/)', parsed.path.lower()) and not re.match(
                    r".*\.(css|js|bmp|gif|jpe?g|ico"
                    + r"|png|tiff?|mid|mp2|mp3|mp4"
                    + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|ical|share=|odc"
                    + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
                    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                    + r"|epub|dll|cnf|tgz|sha1"
                    + r"|thmx|mso|arff|rtf|jar|csv"
                    + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.query.lower()) and not re.search(
                        r'(ical=|share=|action=)', parsed.query.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise