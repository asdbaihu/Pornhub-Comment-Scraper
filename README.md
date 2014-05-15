Cream.py
========

A markov chain combining the book of genesis and pornhub comments -- all in python!


Usage:

First, obtain a link to a pornhub video. Then, pick some large number of comments to obtain. The larger the number, the better. Typically the algorithm does best at around 5000 comments (before it hits enough cycles to terminate).

Run the [preprocessing] program:
>>> python cream.py -url <link> -numcomments <5000> -bible /Users/Steve/Desktop/genesis.txt -outputfile /Users/Steve/Desktop/comments.txt

I have conveniently included the entire text of genesis in this project! :)

Now, to run the program and generate a sentence:
>>> python cream.py -file /Users/Steve/Desktop/comments.txt

That will output your sentence.



Also -- feel free to use this with something besides genesis. You know, the entire text of 50 shades of gray or maybe Catcher in the Rye. Who knows!


Made whilst procrastinating during finals week.






