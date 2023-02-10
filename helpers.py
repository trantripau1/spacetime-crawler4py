import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.response import Response

# ************* Function longestPage **********************************
# Counts the number of words on the current webpage and writes to 
# longestPage.txt IFF the current webpage has more words based off the 
# tolkiens function
# *********************************************************************
def longestPage(url, text):
    tokens = tolkiens(text)
    prev_largest = []
    largest = []
    with open("longestPage.txt", "r") as f:
        lines = f.readlines()
        if len(lines) > 0:
            for line in lines:
                line = line.strip()
                if line is not None:
                    prev_largest.append(line)
    f.close()

    if len(prev_largest) < 1:
        largest = [url, str(len(tokens))]
    else:
        largest = prev_largest
        if len(tokens) > int(prev_largest[1]):
            largest = [url, str(len(tokens))]
 
    with open("longestPage.txt", "w") as f:
        f.write(largest[0])
        f.write("\n")
        f.write(str(largest[1]))
    f.close()

# ************* Function tolkiens *************************************
# takes in a single parameter a string of txt. Tolkiens tokenizes
# alphanumeric characters strictly whilst ignoring any words featured
# in the stopwords list.
# *********************************************************************
def tolkiens(text):
    # Retrieve stopwords list
    stopwords = set()
    with open("stopwords.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line is not None:
                stopwords.add(line)
    f.close()

    # tokenize and add to list text_words
    text_words = []
    text = re.split("[\W_À-ÖØ-öø-ÿ]+", text) #Split on nonalphanumerics to create list of words in line.
    for word in text: 
        token = word.lower() #Make lowercase so the capitalization does not matter.
        if token != '' and token.isascii() == True and token not in stopwords:
            text_words.append(token) #Adds to list
    return text_words

# ************* Function mostCommon ***********************************
# Takes in a single parameter a string of text. Reads a preformatted
# txt file known as words.txt that contains a record of the previous
# words and their associated frequencies and then updates/adds to that
# txt file.
# *********************************************************************
def mostCommon(text):
    #create a map and read file containing past word frequencies.
    words = {}
    with open("words.txt", "r") as f:
        lines = f.readlines()
        # If words.txt is not empty, read and add the words saved.
        if len(lines) > 0:
            for line in lines:
                line = line.strip()
                if line is not None:
                    word_count = re.split("[\W_À-ÖØ-öø-ÿ]+", line)
                    # File words.txt format is word <space> num
                    words[word_count[0]] = int(word_count[1])
    f.close()

    # Generate a list of words scraped from text and add/update
    # to words dict.
    tokenList = tolkiens(text)
    for token in tokenList:
        if token not in words:
            words[token] = 0
        words[token] += 1
    
    # Sort the dictionary by value. if there is a tie, by alphabetical
    words = dict(sorted(words.items(), key = lambda key: key[0], 
        reverse=True))
    words = dict(sorted(words.items(), key = lambda item: item[1], 
        reverse=True))

    # Overwrite to the file starting with words with highest freq
    with open("words.txt", 'w') as f:
        for line in words:
            f.write(line)
            f.write(" ")
            f.write(str(words[line]))
            f.write("\n")
    f.close()

# ************* Function getSubdomains ********************************
# reads from status.txt. Adds to a dict that records the unique 
# subdomain and the number of times they appear.
# returns the dictionary
# *********************************************************************
def getSubdomains():

    # read from that status.txt all the urls that match the domain
    # and then add them to subdomains
    subdomains = {}
    with open('status.txt', 'r') as f:
        for line in f:
            url = urlparse(line)
            subdomain = url.hostname.split('.')[0]
            if not 'https://' + subdomain + '.ics.uci.edu' in subdomains:
                subdomains['https://' + subdomain + '.ics.uci.edu'] = 1;
            elif 'https://' + subdomain + '.ics.uci.edu' in subdomains:
                subdomains['https://' + subdomain + '.ics.uci.edu'] += 1
    f.close()
    
    #sort subdomains alphabetically and then by frequency
    subdomains = dict(sorted(subdomains.items(), key = lambda key: key[0]))
    subdomains = dict(sorted(subdomains.items(), key = lambda item: item[1], reverse=True))  
        
    return subdomains

# ************* Function report ***************************************
# Summarizes all statistics by reading from each respective file and 
# writing to report.txt the total pages that are unique and valid,
# the page with the largest numbers of recorded words, the 50 most
# common words and the unique subdomains in under the ics.uci.edu
# domain (with their respective frequencies)
# *********************************************************************
def report():

    #get total number of pages
    totalpages = 0
    with open('status.txt', 'r') as f:
        for line in f:
            totalpages += 1
    f.close()

    # read from longestPage.txt to get larget page in terms of words
    largest = []
    with open("longestPage.txt", "r") as f:
        lines = f.readlines()
        if len(lines) > 0:
            for line in lines:
                line = line.strip()
                if line is not None:
                    largest.append(line)
    f.close()

    # write to the report.txt all the statistics 
    with open('report.txt', 'w') as f:
        f.write("Total Unique Pages Found: " + str(totalpages) + "\n")
        f.write("Longest page in terms of words: " + largest[0])
        f.write("\tWords: " + largest[1] + "\n")
        f.write("\nList of the 50 most common words:\n")
        with open("words.txt", 'r') as f2:
            count = 0
            lines = f2.readlines()
            if len(lines) > 0:
                for line in lines:
                    line = line.strip()
                    if count == 50:
                        break
                    if line is not None:
                        word = re.split("[\W_À-ÖØ-öø-ÿ]+", line)
                        f.write(word[0] + ", " + word[1] + "\n")
                    count += 1
        f2.close()
        subdomains = getSubdomains()
        f.write("\nUnique subdomains found under ics.uci.edu:\n")
        for sub in subdomains:
            f.write(sub + ", " + str(subdomains[sub]) + "\n")
    f.close()

        
        
