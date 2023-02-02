import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from utils.response import Response
import re

def countWords(text):
    #create a map and read file containing past word frequencies
    wordFreq = {}
    with open("words.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            word_count = re.findall("\w+", line)
            # File words.txt format is word <space> num
            wordFreq[word_count[0]] = int(word_count[1])
    f.close()

    # After file is read proceed to add/update words and their counts
    tokens = re.findall('\w+', text)
    for token in tokens:
        token = token.lower()
        if token not in words:
            words[token] = 0
        words[token] += 1
    
    # Sort the dictionary by value. if there is a tie, by alphabetical
    words = dict(sorted(words.items(), key = lambda key: key[0], 
    reverse=True))
    words = dict(sorted(words.items(), key = lambda item: item[1], 
    reverse=True))

    # Overwrite to the file starting with words with highest freq
    with open("words.txt", "w") as f:
        for line in words:
            f.write(line)
            f.write(" ")
            f.write(words[line])
            f.write("\n")
    f.close()
    
    # Creates a list of the top 50 most common words
    top50 = []
    i = 0
    for key in words:
        if i == 50:
            break
        top50.append(key)
        i += 1
    return top50

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

    #create a prev_urls to read in stored links from previous searches.
    prev_urls = {}
    with open("urls.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        prev_urls[line.strip()] = 1
    f.close()

    #parse webpage and find all links and text
    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    links = soup.find_all("a", href=True)
    text = soup.getText()

    # Count the number of words and their freqs 
    countWords(text)

    # We will use the is_valid url function in this loop to make sure
    # we do not add bad urls or previously visited urls. 
    # we create a new_urls to store
    new_urls = {}
    for link in links:
        str_link = link.get('href')
        if str_link not in urls and str_link not in new_urls:
            new_urls[str_link] = 1
    
    # Open file again and denote to append to the urls.txt file
    with open('urls.txt', 'a') as f:
        for line in new_urls:
            f.write(line)
            f.write('\n')
    f.close()
    return new_urls

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

if __name__ == '__main__':
    url = 'https://www.ics.uci.edu'
    resp = requests.get(url)
    #print(type(resp.content))
    print(resp.content["url"])
    #new_resp = Response(resp.content)
    #print(scraper(url, resp))