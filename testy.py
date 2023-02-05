import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.response import Response
import requests

parsed = urlparse("https://www.informatics.uci.edu/files/pdf/InformaticsBrochure-March2018")
parsed = urlparse("http://sli.ics.uci.edu/Classes/2015W-273a?action=download&upname=HW4")
print("This is the parsed1 query: ", parsed.query)
print("this is the parsed1path:\t", parsed.path)
#r = requests.get(parsed2)
#print(r.headers['Content-Type'])

print( not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()) and not re.search(
                r'(/css/|/js/|/bmp/|/gif/|/jpe?g/|/ico/|Calendar/'
                + r'|/png/|/tiff?/|/mid/|/mp2/|/mp3/|/mp4/'
                + r'|/wav/|/avi/|/mov/|/mpeg/|/ram/|/m4v/|/mkv/|/ogg/|/ogv/|/pdf/'
                + r'|/ps/|/eps/|/tex/|/ppt/|/pptx/|/ppsx/|/doc/|/docx/|/xls/|/xlsx/|/names/'
                + r'|/data/|/dat/|/exe/|/bz2/|/tar/|/msi/|/bin/|/7z/|/psd/|/dmg/|/iso/'
                + r'|/epub/|/dll/|/cnf/|/tgz/|/sha1/'
                + r'|/thmx/|/mso/|/arff/|/rtf/|/jar/|/csv/'
                + r'|/rm/|/smil/|/wmv/|/swf/|/wma/|/zip/|/rar/|/gz/)', parsed.path.lower()) and not re.match(
                    r".*\.(css|js|bmp|gif|jpe?g|ico"
                    + r"|png|tiff?|mid|mp2|mp3|mp4"
                    + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                    + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
                    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                    + r"|epub|dll|cnf|tgz|sha1"
                    + r"|thmx|mso|arff|rtf|jar|csv"
                    + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.query.lower()))

req = requests.get("http://sli.ics.uci.edu/")
print(req.status_code)