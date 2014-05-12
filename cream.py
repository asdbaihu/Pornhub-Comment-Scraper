#pornhub
import requests



#Crawls through the pornhub database and amasses a set 
#
#
def crawl(initialURL):

	r = requests.get(initialURL)

	print("Got page " + initialURL)

	comments = getCommentsFromPageText(r.content)
	
	links = getLinksFromPageText(r.content)

	return (comments, links)


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

	linkMarker = "<a href=\"/view_video.php?\""

	pageCopy = str(pageText)

	linkSet = set()

	while pageCopy.find(linkMarker) > 0:

		#skip to the thing
		pageCopy = pageCopy[pageCopy.find(linkMarker)+9:]

		#copy the link
		link = pageCopy[:pageCopy.find("\"")]

		linkSet.add(link)
	
	return linkSet


comments,links = crawl("http://www.pornhub.com/view_video.php?viewkey=1193961895")

x = 0
for y in comments:
	x = x + 1
	print(str(x) + ": " + y)


