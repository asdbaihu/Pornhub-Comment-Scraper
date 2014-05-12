#pornhub
import requests
import sys


#Crawls through the pornhub database and amasses a set 
#
#
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

		print("Got page " + initialURL)

		comments = getCommentsFromPageText(str(r.content))
		allComments = allComments.union(comments)

		links = getLinksFromPageText(str(r.content))

		for link in links:
			#print("Adding link: " + link)
			frontier.append(link)

		exploredPages.add(url)
	return allComments


def getCommentsFromPageText(content):
	#search for the correct divs
	commentMarker = "<div class=\"commentMsg\">"

	#total comments
	allComments = set()

	while content.find(commentMarker) > 0:
		
		#jump to the place where you found the div, and cut out the rest of the string
		content = content[(content.find(commentMarker) + len(commentMarker)):]
		
		#search for the first div
		content = content[(content.find("<div>") + 5):]

		#get the comment
		comment = content[:content.find("</div>")]

		#add the comment to the database
		allComments.add(comment)

	return allComments


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


if (len(sys.argv) != 2):
	print "Usage: python cream.py <initial url> <number of comments>"

initialURL = sys.argv[0]
numberOfComments = int(sys.argv[1])

comments = crawl(initialURL, numberOfComments)

x = 0
for y in comments:
	x = x + 1
	print(str(x) + ": " + y)


