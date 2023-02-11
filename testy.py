import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.response import Response
import requests
import helpers

#parsed = urlparse("https://www.informatics.uci.edu/files/pdf/InformaticsBrochure-March2018")
parsed = urlparse("http://computableplant.ics.uci.edu/papers/2006/plcb-02-12-12_Wold.pdf")

print("This is the parsed1 query: ", parsed.query)
print("this is the parsed1 path:\t", parsed.path)

if parsed.scheme not in set(["http", "https"]):
    print("f")
elif parsed.hostname == None:
    print("fa")
elif not parsed.hostname.endswith(('ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu')):
    print("fal")
elif re.match( 
    r".*\.(css|js|bmp|gif|jpe?g|ico"
    + r"|png|tiff?|mid|mp2|mp3|mp4"
    + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|wp-json|odc"
    + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
    + r"|epub|dll|cnf|tgz|sha1"
    + r"|thmx|mso|arff|rtf|jar|csv"
    + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
        print("fals")
elif re.search( 
    r'(/css/|/js/|/bmp/|/gif/|/jpe?g/|/ico/'
    + r'|/png/|/tiff?/|/mid/|/mp2/|/mp3/|/mp4/'
    + r'|/wav/|/avi/|/mov/|/mpeg/|/ram/|/m4v/|/mkv/|/ogg/|/ogv/|pdf'
    + r'|/ps/|/eps/|/tex/|/ppt/|/pptx/|/ppsx/|/doc/|/docx/|/xls/|/xlsx/|/names/|/wp-'
    + r'|/data/|/dat/|/exe/|/bz2/|/tar/|/msi/|/bin/|/7z/|/psd/|/dmg/|/iso/'
    + r'|/epub/|/dll/|/cnf/|/tgz/|/sha1/'
    + r'|/thmx/|/mso/|/arff/|/rtf/|/jar/|/csv/'
    + r'|/rm/|/smil/|/wmv/|/swf/|/wma/|/zip/|/rar/|/gz/)', parsed.path.lower()):
        print("false")
elif re.match( 
    r".*\.(css|js|bmp|gif|jpe?g|ico"
    + r"|png|tiff?|mid|mp2|mp3|mp4"
    + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|ical|share=|odc"
    + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
    + r"|epub|dll|cnf|tgz|sha1"
    + r"|thmx|mso|arff|rtf|jar|csv"
    + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.query.lower()):
        print("false1")
elif re.search(
    r'(ical=|share=|action=)', parsed.query.lower()):
        print("fgalse2")
elif parsed.hostname.endswith(('wics.ics.uci.edu')):
    if re.search(r'(/events/|/wics-hosts|/letter-of)', parsed.path.lower()):
        print("fgalse3")
print("True")
#resp = requests.get("https://wics.ics.uci.edu/4")
#print(len(resp.text))
#soup = BeautifulSoup(resp.content, "html.parser")
#t = soup.getText()
#print(len(t))
#print(t)
helpers.report()