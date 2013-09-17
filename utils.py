from requests import get,ConnectionError
from bs4 import BeautifulSoup
import numpy as np
from fractions import Fraction
import pandas as pd
from time import sleep

import pdb

def find_measures(bsoup, id):
  measures = bsoup.find_all('div', class_="recipeMeasure")
  return list( set( filter(None, [ parse_measures(m, id)for m in measures ]) ) )

def find_directions(bsoup, id):
  directions = bsoup.find_all('div', class_="recipeDirection")
  return list( set( filter(None, [ parse_directions(m, id) for m in directions ]) ) )

def find_name(bsoup,id):
  try:
    name = bsoup.find_all('div', id ='wellTitle')[0].find_all('h2')[0].text
  except:
    name = "unknown"
  return name      

def parse_measures(measure_info, id ):
  """return (id, volume, ingredient, 'measure')"""
  contents = measure_info.contents
  if "Flame" in contents[0]:
    return None 
  elif "Place" in contents[0]:
    return ( id, "1", "pieces of " + contents[1].text, "measure"  )
  elif "Fill" in contents[0]:
    return ( id, "1", "pieces of " + contents[1].text, "measure"  )
  return ( id, contents[0], contents[1].text, "measure"  )

def parse_directions(direction_info, id):
  contents = direction_info.contents
  if contents[0] in ("Build", "Serve in a ", "Muddle/shake"):
    return None
  elif contents[0] == "Fill with":
    return (id,1, "Fill with ice", "direction")
  elif contents[0] == "Top with ": #need to investigate this one further.
    return (id, 1, "Top with "+ contents[1].text , "direction")
  elif contents[0] == "Shake in ":
    return (id, 1, "Shake in iced cocktail shaker & strain" , "direction")
  elif contents[0] == "Stir in ":
    return (id, 1, "Stir in mixing glass with ice & strain" , "direction")
  elif contents[0] == "Add ":
    return (id, 1, contents[1].text, "direction")
  else:
    return None

def parse_volumes(measures):
  """This takes in measures, and replaces the volumes with floats"""
  return [ (m[0], ounce_to_float(m[1]), m[2].lower(), m[3]) for m in measures ]

def ounce_to_float(oz_string):
  """converts something like '1 1/2 oz ' to 1.5"""
  oz_string = oz_string.strip()
  oz_split = oz_string.split(" ")
  if "dash" in oz_split[-1]:
    return 0.1 #?? what the hell is a dash
  else:
    s=0.0
    i=0
    while 1:
      try:
        s += Fraction(oz_split[i])
        i+=1
        if i%10==0:
          print "Broke! %d"%i
      except ValueError:
        return s
      except IndexError:
        return s

def measures_to_df(all_measures, columns):
  df = pd.DataFrame.from_records( all_measures,
                                  columns=columns
                                  )
  return clean_data(df_to_pivot(df,columns))

def df_to_pivot(df,columns):
  return pd.pivot_table(df, values = columns[1], rows=columns[0], cols=columns[2], aggfunc=np.sum, fill_value = 0).astype(float)


def clean_data(df):
  return df[ df.columns[ df.sum(0)!=0 ]]

def merge_columns(df, same_columns):
    df_ = df.copy()
    for columns in same_columns:
      c_keep = columns[0]
      for c in columns[1:]:
         try:
            df_[c_keep] += df_[c]
            del df_[c]
         except Exception: 
             pass 
    return df_ 

def run(upper, lower):
  drink_ids = range(upper,lower)
  recipes = {}
  for drink_id in drink_ids:
      URL = "http://www.cocktaildb.com/recipe_detail?id=%d"%drink_id
      try:
        bs = BeautifulSoup(get(URL).text)
      except ConnectionError as e:
        print e 
        sleep(3)
        bs = BeautifulSoup(get(URL).text)      
      recipes[drink_id] = {
              "measures":find_measures(bs,drink_id),
              "directions": find_directions(bs,drink_id),
              "name": find_name(bs,drink_id)
      } 
      print recipes[drink_id]["name"] 
      sleep(0.2)

  return recipes

EQUAL_DIRECTIONS = [
      ["orange slice", "orange slices"],
      ["lime slice", "lime shell", "lime wedge", "lime wheel"],
      ["lemon slice", "lemon shell", "lemon wedge", "lemon wheel"],
      ["mint sprigs", "mint sprig", "mint leaves", "mint leaf"],
      ["pineapple slices", "pineapple slice", "piece of pineapple"],
      ["pineapple chunks", "pineapple chunk"],
      ["cloves", "clove"],
      ["black cherries", "black cherry"],
      ["almonds", "almond"],
      ["Top with whipped cream", "whipped cream"],
      ["cocktail onion", "onion"]
    ]

EQUAL_INGREDIENTS = [ 
     ['gold rum', 'golden rum'],
     ['yolk of egg', 'yolk of fresh egg', 'egg yolk'],
     ['canadian club', 'canadian club whisky', 'canadian whiskey', 'canadian whisky'],
     ['egg white', 'white of an egg'],
     ['worcester sauce', 'worcestershire', 'worcestershire sauce'],
     ['johnnie walker', 'johnny walker'],
     ['creme de vanilla', 'creme de vanille'],
     ['passion fruit juice', 'passion fruit nectar', 'passion fruit syrup'],
     ['vanilla', 'vanilla extract'],
     ['mint sprig', 'mint sprigs', 'sprigs of mint', 'mint leaf', 'fresh mint'],
     ['lime (or lemon) juice', 'lemon (or lime) juice'],
     ['lime juice', 'fresh lime juice'],
     ['lemon juice', 'fresh lemon juice'],
     ['orgeat', 'orgeat syrup'],
     ['calisay', 'calisaya'],
     ['clove', 'cloves'],
     ['frais','fraise'],
     ['ice','iced'],
     ['jamaica ginger', 'jamaican ginger', 'jamaican ginger extract'],
     ['kirsch','kirschwasser'],
     ['lillet','lillet blanc'],
     ['shaved ice', 'pieces of shaved ice'],
     ['dry vermouth', 'vermouth, dry'],
     ['vieille cure', 'vielle cure'],
     ['egg', 'eggs','whole egg', 'whole eggs'],
     ['blackberry brandy', 'blackberry flavored brandy'],
     ['mandarette', 'mandarinette'],
     ["myers's", "myers's rum"],
     ['port', 'port wine'],
     ['gomme', 'gomme syrup'],
     ['apricot brandy','apricot flavored brandy'],
     ["pimm's", "pimm's cup"],
     ["rose's", "rose's lime juice"],
     ['sambuca', 'sambucca'],
     ['sauterne', 'sauterne wine'],
     ['scotch', 'scotch whisky'],
     ['tabasco', 'tabasco sauce'],
     ['angostura', 'angostura bitters'],
     ['mint leaf', 'mint leaves'],
     ['limes', 'lime'],
     ['geneva gin', 'genever gin'],
     ['jamaica rum', 'jamaican rum'],
     ['prunella', 'prunelle', 'prunelle liqueur'],
     ["creme d'yvette",'creme de yvette','creme yvette'],
     ['creme de noyau', 'creme de noyeau', 'creme de noyeaux'],
     ['creme de banana', 'creme de banane'],
     ['ginger brandy', 'ginger flavored brandy'],
     ['orange flavored gin', 'orange gin'],
     ['catsup', 'tomato catsup'],
     ['bourbon', 'bourbon whisky'],
     ['campari', 'campari bitters'],
     ['caloric', 'caloric punch'],
     ['maraschino', 'maraschino liquer'],
     ['orange juice', 'fresh orange juice'],
     ['creme of coconut', 'cream of coconut'],
     ['coffee liqueur', 'coffee liquor'],
     ['cherry flavored brandy', 'cherry brandy'],
     ['bacardi light rum', 'bacardi rum'],
     ['aurum', 'aurum liqueur'],
     ['151 proof rum', '151 rum'],
     ['raspberries', 'raspberry'],
     ['coffee liqueur', 'coffee liquor'],
     ['cordial', 'cordial medoc'],
     ['muscatel', 'muscatel wine'],
     ['peach brandy', 'peach flavored brandy'],
     ['peychaud', 'peychaud bitters'],
     ['liqueur', 'liquor'],
     ['guava juice', 'guava nectar', 'guava syrup']
  ]


if __name__=="__main__":
  bounds = range(1, 4300,100)
  recipes = {}
  for lower in bounds:
    recipes.update(run(lower, lower+100))
    sleep(2)
    print
    print len(recipes)
  all_measures = sum( [ v["measures"] for k,v in recipes.iteritems()], [] )
  all_directions = sum( [v["directions"] for k,v in recipes.iteritems()], [] )

  directions_df = measures_to_df( all_directions, ['id', 'action', 'direction', 'directions'])
  directions_df = merge_columns( directions_df, EQUAL_DIRECTIONS)

  all_measures = parse_volumes( all_measures )
  measures_df = measures_to_df( all_measures, ['id', 'volume', 'ingredient', 'measure'] )
  measures_df = merge_columns( measures_df, EQUAL_INGREDIENTS)
  print "done"

