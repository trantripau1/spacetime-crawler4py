import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.response import Response
import requests
import helpers

#parsed = urlparse("https://www.informatics.uci.edu/files/pdf/InformaticsBrochure-March2018")
parsed = urlparse("http://computableplant.ics.uci.edu/papers/2006/plcb-02-12-12_Wold.pdf ")
print("This is the parsed1 query: ", parsed.query)
print("this is the parsed1 path:\t", parsed.path)
#r = requests.get(parsed2)
#print(r.headers['Content-Type'])

print( not re.match(
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
                + r'|/wav/|/avi/|/mov/|/mpeg/|/ram/|/m4v/|/mkv/|/ogg/|/ogv/|pdf|/wp-content/'
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
                        r'(ical=|share=|action=|jpg)', parsed.query.lower()))

resp = requests.get("https://wics.ics.uci.edu/4")
print(len(resp.text))
#soup = BeautifulSoup(resp.content, "html.parser")
#t = soup.getText()
#print(len(t))
#print(t)
helpers.report()