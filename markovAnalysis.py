"""

Using Markov chains calculate relative ratings for all ingredients
then generate new recipes using these rankings.

Warning: every so often this produces absolutely disgusting sounding
drinks which should be considered monstrosities and never be craeted.

"""

import re
import csv

import os
import random
from collections import Counter

# import numpy as np 	# used for experimental rating systems

from scipy import stats

# Massive regex to clean clean ingredient data
filter = r'^(((\s?[\.0-9\/\-,](?!-up))|qt[s]?|\s|oz[s]?\s|cl[s]?\s|part[s]?|shot[s]?|cup[s]?|l\s|tsp[s]?|tb[s]?[l]?(sp[s]?)?|ml[s]?|fill\s|with\s|fill\swith\s|fifth[s]?|splash(es)?|lb[s]?|drop[s]?|jigger[s]?|count[s]?|measure[s]?|dash(es)?|pint[s]?|bottle[s]?|gal[s]?|(add|top)\s|glass\s|handful[s]?\s|or\s|about\s|in\s|gr\s|aprox\s|a\sdash\s(of\s)?|kg\s)\s?)*'

datasetFolder = './datasets/'

dataFile = '6K.csv'
recipeOutputFile = 'MarkovRecipes.csv'
ingredientOutputFile = 'MarkovIngredients.csv'

# csv quote char
qchar = '"'

minVoteCount = 10

# create proper paths
dataFile = os.path.join(datasetFolder, dataFile)
recipeOutputFile = os.path.join(datasetFolder, recipeOutputFile)
ingredientOutputFile = os.path.join(datasetFolder,ingredientOutputFile)



dataset = csv.reader(file(dataFile,'r'), delimiter=',', quotechar=qchar)



"""
Read file and create ingredient list with related ingredients, ratings, and vote counts
Ingredient data returned as :

{ingredient}{count, related list, rating, votes}

"""
def createIngredientData(  ):
	
	# Dict of ingredients and their relations
	ingredients = {}

	# Read data
	with open(dataFile, 'r') as csvfile:

		dialect = csv.Sniffer().sniff(csvfile.read())
		csvfile.seek(0)
		reader = csv.reader(csvfile, dialect)

		# generate markov chain for drinks
		for row in reader:
			
			ingredients_list = row[4:]

			votes = int(row[3])

			# remove votes under threshold
			if votes > minVoteCount:

				ingredients_sublist = [] 

				if row[2] != '': # if rated
					rating = float(row[2])

				# iterate through ingredients in drink
				for i in ingredients_list:

					# normalize ingredient data
					i = i.lower()
					i = re.sub(filter, '', i) # apply regex ingredient filter
					
					# create new value in ingredient list
					if i not in ingredients.keys():

						ingredients[i] = {
							'count':1, 
							'related':{},	# list of related ingredients 
							'rating':rating,
							'votes':votes	# total votes
							}
					
					# update ingredient data
					else:

						ingredients[i]['count'] += 1
						ingredients[i]['rating'] += rating
						ingredients[i]['votes'] += votes

					# add ingredient to this drink's list
					ingredients_sublist.append(i)
				

				# ingredients_sublist = list(ingredients_sublist)
				
				# iterate through each ingredient and it's related ingredients
				# increment their counts and rating values
				for x in ingredients_sublist:
					for y in ingredients_sublist:
						if y != x:

							if y in ingredients[x]['related'].keys():

								ingredients[x]['related'][y]['count']+=1
								ingredients[x]['related'][y]['rating']+=rating
							
							else:
								ingredients[x]['related'][y] = {}
								ingredients[x]['related'][y]['count'] = 1
								ingredients[x]['related'][y]['rating'] = rating

	# Iterate through ingredient list and calculate average ratings
	for x in ingredients.keys():

		ingredients[x]['rating'] = ingredients[x]['rating']/ingredients[x]['count']

		# update related ingredient ratings to get an idea of what goes well together
		for k in ingredients[x]['related'].keys():
			ingredients[x]['related'][k]['rating'] =  ingredients[x]['related'][k]['rating']/ingredients[x]['related'][k]['count']



	# write ingredients to file
	fout = csv.writer( file(ingredientOutputFile,'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	for k in ingredients:
		fout.writerow( [k, ingredients[k]['rating']]+ ingredients[k]['related'].keys() )

	# return rated data
	return ingredients

"""
Generate one recipe for every ingredient
"""
def generateRecipes():


	ingredients = createIngredientData()

	mean = 0 	# mean rating
	var = 0 	# variance of ratings

	for k in ingredients.keys():
		mean += ingredients[k]['rating']	
		var += ingredients[k]['rating']**2	

	mean = mean/len(ingredients)
	var = var/len(ingredients)-mean**2

	# Use normal distribution to normalize our ratings
	norm = stats.norm(loc=mean,scale=var**(0.5))

	# list of recipes from ingredients
	recipes = []

	# create a recipe for each ingredient sorted by rating
	for k in [ ingredients.keys().index(x[0]) for x in sorted( ingredients.items(), key=lambda t:t[1]['rating'] ) ]:
		
		choiceLength = 5 	# number of ingredients in drink

		# id of starting ingredient
		r=k 	

		# list of ingredients and their indices for this recipe
		recipe = [ [ingredients.keys()[r],r ] ]


		emptyIngredientList = False
		for i in range(0,random.randint(1,choiceLength)):
			
			if not emptyIngredientList:
				try:

					# name of this ingredient
					name = recipe[i][0]

					# Sort by best rated in sublist
					rel = sorted( ingredients[name]['related'], key= lambda x: ingredients[x]['rating'],reverse=True)

					# choose an ingredient from list of related ingredients
					for j in range(0,min(len(rel)-1,choiceLength)):

						# select random ingredient
						r = random.randint(j,min(len(rel)-1,choiceLength))
						
						# add to drink if not already in drink
						if 	r not in [x[0] for x in recipe]:
							recipe.append( [rel[r], r] )
							break
				
				# list was empty
				except Exception as e:

					emptyIngredientList=True
					break

		# rank recipes
		if recipe != [] and len(recipe)>1:

			drinkRating = 0

			# remove duplicate ingredients
			recipe = list(set([x[0] for x in recipe]))


			previous = ''
			for i in recipe:
				if i!=recipe[0]:	
					try:
						rating = ingredients[previous]['related'][i]['rating']
					except:
						pass
				else:
					rating = ingredients[i]['rating']

				# print i,',', rating
				drinkRating += rating

				previous=i

			drinkRating/=len(recipe)

			# Some experimental rantings
			# drinkRating = drinkRating*drinkRating
			# drinkRating = norm.cdf(drinkRating)

			recipes.append([recipe,drinkRating])

	return recipes


# get recipe list
recipes = generateRecipes()

# Sort recipes by ranking
recipes = sorted(recipes, key=lambda x: x[1],reverse=False)

# print all recipes
for recipe in recipes:
	print recipe[1]
	for ingredient in recipe[0]:
		print '\t',ingredient

# output data to csv file
fout = csv.writer( file(recipeOutputFile,'w'),delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
for x in recipes:
	fout.writerow( [x[1]]+x[0] )

