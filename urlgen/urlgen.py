from . import adjectives
from . import animals
from secrets import choice

'''
Securely generates a url suffix in the adj-adj-animal pattern
'''
def generate():
	adj1 = choice(adjectives.adj_list).capitalize()
	adj2 = choice(adjectives.adj_list).capitalize()
	animal = choice(animals.animal_list).capitalize()
	return "{}{}{}".format(adj1, adj2, animal)