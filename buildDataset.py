"""
buildDataset

Implements a function ``buildListOfDict`` to parse the drink recipe dataset 
(./datasets/6K.csv) and turn it into a list of drink recipe dictionaries.


"""


def buildListOfDict():
    dataset = []
    f = open("./datasets/6K.csv",'r').readlines()
    for line in f:
        recipe = line.strip('\n').split(',')
        drink = {}
        drink['id'] = recipe[0]
        drink['name'] = recipe[1]
        drink['rating'] = recipe[2]
        drink['votes'] = recipe[3]
        recipe = recipe[4:]
        drink['ingredients'] = []
        for i in xrange(len(recipe)):
            drink['ingredients'].append(recipe[i])
            #quantity, ing = parseIngredient(recipe[i])
            #drink['ingredients'].append({'quantity':quantity, 'type':ing})
        dataset.append(drink)
    return dataset

def parseIngredient(ing):
    #   was going to split each ingredient string into 'quantity' and 'type'..
    #   e.g. quantity = 2 oz, type = Vodka
    pass

if __name__=='__main__':
    drinklist = buildListOfDict()
    print drinklist[0]
