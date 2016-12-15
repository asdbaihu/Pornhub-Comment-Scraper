#!/usr/bin/python
import requests
import sys
import random
from bs4 import BeautifulSoup
import re

#Crawls through the pornhub database and amasses a set 
#
#returns the set of all comments, where each string in the set contains a comment
def crawl(initialURL, maxComments):
    #keep this so we don't get any cycles
	exploredPages = set()

	frontier = list()

	frontier.append(initialURL)

	allComments = set()

	#frontier is 'true' if it is non-empty
	while frontier and len(allComments) < maxComments:

		url = frontier.pop()

		if url in exploredPages:
			continue

		r = requests.get(url)
		print("Got page " + url)

		comments = getCommentsFromPageText(str(r.content))
		allComments = allComments.union(comments)
		
		print "Num comments: " + str(len(allComments))
		links = getLinksFromPageText(str(r.content))
		for link in links:
			frontier.append(link)

		exploredPages.add(url)
	return allComments

# Given a page's HTML content
# returns all of the comments from that page
def getCommentsFromPageText(content):
	#search for the correct divs
	commentMarker = "<div class=\"commentMessage\">"
	soup = BeautifulSoup(content, "html5lib")
	comments = set()
	for comment in soup.findAll("div", {"class" : "commentMessage"}):
		commentText = ''.join([v.extract() for v in comment])
		commentText = ' '.join(commentText.split())
		comments.add(commentText)
	print "Num comments on this page: " + str(len(comments))	
	return comments

# Given a page's text, provides a set containing all of the links
# outgoing from those pages.
# returns a set of links, strings
def getLinksFromPageText(pageText):

	linkMarker = "<a href=\"/view_video.php?"

	pageCopy = str(pageText)

	print(pageCopy.find(linkMarker))

	linkSet = set()

	while pageCopy.find(linkMarker) > 0:

		#skip to the thing
		pageCopy = pageCopy[pageCopy.find(linkMarker)+9:]

		#copy the link
		link = pageCopy[:pageCopy.find("\"")]

		link = "http://www.pornhub.com" + link

		linkSet.add(link)
	
	return linkSet


# Returns triples of words from the comments
def generateMarkovData(commentSet):
	triples = set()
	for comment in commentSet:
		words = comment.split()
		words = [x.lower() for x in words]
		#form triples
		for y in range(0, len(words)-2):
			current_triple = (words[y].lower(),words[y+1].lower(),words[y+2].lower())
			triples.add(current_triple)
	return triples

#markovData = Set of triples
def getRandomWord(markovData):
	return random.choice(random.choice((random.sample(markovData, 1))))


# Markov chain-type combination
def generateRandomSentence(markovData):
	currentWord = getRandomWord(markovData)
	nextWord = getRandomWord(markovData)
	sentence = currentWord + " " + nextWord + " "
	
	while ((not (nextWord==None and nextWord[len(nextWord)]=="." and nextWord==".")) and ((len(sentence.split())<180))):
		results = filter(lambda (a,b,c): (a==currentWord and b==nextWord), markovData)
		currentWord = nextWord
		if not results:
			c = getRandomWord(markovData)
			nextWord = c
			sentence = sentence + nextWord + " "
		else:
			(a,b,c) = random.choice(results)
			nextWord = c
			sentence = sentence + nextWord + " "
	return sentence

def writeCommentsToFile(commentSet, fileName):
	f = open(fileName, 'w') 
	for comment in commentSet:
		f.write(comment + "\n")
	f.close()

def loadCommentSetFromFile(fileName):
	f = open(fileName, 'r')
	content = list(f.readlines())
	f.close()
	return content

arguments_dict = dict()

if (("-url" in sys.argv) and ("-file" in sys.argv)) or ((not ("-url" in sys.argv)) and (not ("-file" in sys.argv))):
	print "Usage: python cream.py [-url <initial url> -numcomments <number of comments> -bible <path to bible> -outputfile <output file>] [-file filename]"
	print "-url: the initial url to start the search at."
	print "-numcomments: the maximum number of comments to pull from pornhub."
	print "-bible: the text to mix in with the comments. optional. " 
	exit()

current_argument = ""
for arg in sys.argv:
	if (arg[0] == "-"):
		current_argument = arg[1:]
	else:
		arguments_dict[current_argument] = arg

if ("url" in arguments_dict):
	initialURL = arguments_dict["url"]
	numberOfComments = int(arguments_dict["numcomments"])
	comments = crawl(initialURL, numberOfComments)
	if "bible" in arguments_dict:
		print("Loading bible...")
		bible_comments = loadCommentSetFromFile(arguments_dict["bible"])
		print("Merging...")
		comments = comments.union(bible_comments)
		print("Writing comments to file... " + arguments_dict["outputfile"])
		writeCommentsToFile(comments, arguments_dict["outputfile"])
		print("Loaded comments, training markov chain....")
		markovData = generateMarkovData(comments)
		print("Markov Data Loaded")
		print("Generating sentence...")
		sentence = generateRandomSentence(markovData)
		print("Sentence: " + sentence)
	else:
		print comments
else:
	fileName = arguments_dict["file"]
	comments = loadCommentSetFromFile(fileName)
	print("Loaded comments from file")
	markovData = generateMarkovData(comments)
	print("Markov Data Loaded")
	print("Generating sentence...")
	sentence = generateRandomSentence(markovData)
	print("Sentence: " + sentence)


