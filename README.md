Cream.py
========

A markov chain combining the book of genesis and pornhub comments -- all in python!

What is it?:

A markov chain uses transitory probability to generate sentences. My algorithm for generating sentences is (at this moment) pretty shitty, because most pornhub comments don't have the greatest grammar. So, after like 40 words, the algorithm spits out your sentence.

In short: You use this generate sentences that are partially pornhub comment, partially (insert media here). I used the book of genesis as my second source in my tests, but feel free to use whatever you want.


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






