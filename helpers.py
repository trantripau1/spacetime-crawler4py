import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.response import Response

# Counts the number of words on the current webpage and writes to longestPage.txt
# IFF the current webpage has more words based off the tolkiens function
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

    return largest

# Tokenizes alphanumeric characters, ignoring non-english words 
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

    text_words = []
    text = re.split("[\W_À-ÖØ-öø-ÿ]+", text) #Split on nonalphanumerics to create list of words in line.
    for word in text: 
        token = word.lower() #Make lowercase so the capitalization does not matter.
        if token != '' and token.isascii() == True and token not in stopwords:
            text_words.append(token) #Adds to list
    return text_words

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
    
    # Creates a list of the top 50 most common words
    top50 = []
    i = 0
    for key in words:
        if i == 50:
            break
        top50.append(key)
        i += 1
    return top50