from adjectives import adj_list
from animals import animal_list
from secrets import choice

'''
Securely generates a url suffix in the adj-adj-animal pattern
'''
def generate():
	adj1 = choice(adj_list).capitalize()
	adj2 = choice(adj_list).capitalize()
	animal = choice(animal_list).capitalize()
	return "{}{}{}".format(adj1, adj2, animal)