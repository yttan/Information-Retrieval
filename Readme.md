## UCI Web Search Engine

## Text Processing

1. There's a function that reads in a text file and returns a list of the tokens in that file. A function that counts the number of occurrences of each word in the token list. And a method that prints out the word frequency counts ordered by decreasing frequency.  

2. It takes two text files as arguments and outputs the number of
tokens they have in common.

3. It takes two word-frequency maps (given in two separate input text files) and creates an output word-frequency count file where the counts are added. The input and output files are of the form “word, count”, one of these per line.

## SpaceTime Crawler
Use SpaceTime Crawler to download pages.  

Define function extract_next_links (applications/search/crawler_frame.py)   
This function extracts links from the content of a downloaded webpage.  
The output is a list of URLs in string form. Each URL should be in absolute form. It is not required to remove duplicates that have already been downloaded. The frontier takes care of ignoring duplicates.  

Define function is_valid (applications/search/crawler_frame.py)  
This function returns True or False based on whether a URL is valid and must be downloaded or
not. Robot rules and duplication rules are checked separately and should not be checked here.  
This is a place to
1. filter out crawler traps (e.g. the ICS calendar)  
2. double check that the URL is valid and in absolute form.  

Modify function update (applications/search/crawler_frame.py)  
Store all subdomains, the page having maximum number of outgoing links, the total number of invalid urls in a text file.  

## Search Engine
Using the pages that stored by crawling the ics.uci.edu domain, construct an index that maps words to documents (pages). As pay load add the TF-IDF and the position of the words in each document.  

Develop an interface to search the index that retrieves documents according to a relevance score. The user types a query and a list of relevant hits is shown, showing the URL.  

Improve the ranking performance of your search engine

The Oracle (i.e. ground truth) for the ranking of the results is Google. Write a program that sends the queries to Google appended with “site:ics.uci.edu” and returns Google’s search results. For each query, the ordering of the Google results should be considered the “right order” (i.e. the Oracle)

Compute NDCG@5 for tf-idf scoring and improve the search engine’s NDCG@5 by using cosine similarity.

## Usage  
### test processing
files are named as 1.py, 2.py and 3.py. Using Python 2.7. Test files are given.(E.G. test1.txt)  
### Crawler  
The crawler is run on a UCI server. Example extracted files are in folder /WEBPAGES_TEST which has 100 web pages.  
### Search  
Using TF-IDF scoring
```
$ python search.py [your query]
```
NDCG@5 for TF-IDF
```
$ python before.py
```
NDCG@5 for cosine similarity
```
$ python after.py
```
