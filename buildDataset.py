





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
        dataset.append(drink)
    return dataset


if __name__=='__main__':
    drinklist = buildListOfDict()
    print drinklist[0]
