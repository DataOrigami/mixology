Mixology
========

###Every proper club needs a proper club cocktail.

Can we algorithmically find our club cocktail using a large database of cocktail drinks? Yes.

Here are our goals to accomplish:

- Determine the ingredients (and perhaps the directions to make the cocktail, too)
  - This may require an objective function. 
  - Using the database to weed out **bad** combinations is good too!
  - Should have some flair to it.
  - More data is better. We should look at popularity too.
- Determine a name for the cocktail (this should be data determined too)
  - Naively, gather all names of cocktails, split on whitespace, and randomly pick.
  - Better: considering the ingredients we have chosen, look for a pair or triplet
   of existing cocktails that can be "summed up" to produce our cocktail. This is like a regression task.
  - using Google Trends to find "hot names", i.e. "One Chevron Direction" would be hilarious. 
- Look for interesting relationships in the dataset. "orange juice => vodka"? Some tools that might help: association rules, network analysis
- Create a cool postcard-sized graphic about our cocktail (with recipe). We'll use this to create actual postcards to promote our club: "Dear P.M. Harper, I've noticed you could use a drink...". "Dear Ottawa Citizen, we have provided for you a result you might finding interesting-- the url is at ...."
- Can we get a local drinking establishment to serve it? Maybe exclusively to our members/meetings?
- Can we light it on fire? Why not?
- Actually drink it. Our next meeting will be supplied with our new Data Origami cocktail.


### Results?
