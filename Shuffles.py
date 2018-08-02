from random import randint

OVERHAND_VARIATION = 0.2
RIFFLE_VARIATION = 0.04
RIFFLE_MAX_FALLING_CARDS = 4
CORGI_MAX_JUMP = 7

def overhand(deck, generator = False):

	start, end = len(deck), len(deck)
	shuffled_deck = []

	while end > len(deck)/10:

		variation = int(start * OVERHAND_VARIATION)
		start, end = start // 2 + randint(0, variation), start
		shuffled_deck += deck[start:end]

		if generator:
			yield shuffled_deck + deck[:start]

	return shuffled_deck + deck[:start]

# def overhand(deck, generator = False):

# 	start, end = len(deck), len(deck)
# 	start, end = start // 2 + randint(0, variation), start


def riffle(deck, generator = False):

	variation = int(len(deck) * RIFFLE_VARIATION/2)
	shuffled_deck = []

	cut = len(deck) // 2 + randint(-variation, variation)
	pile1, pile2 = deck[:cut], deck[cut:]

	#swapper(1,2) #=> (2,) 1,2,1,2,1,2,1,2 ...
	def swapper(one, two):
		if randint(0, 1) == 0: yield two
		while one or two:
			yield one
			yield two

	for pile in swapper(pile1,pile2):

		split = randint(1, RIFFLE_MAX_FALLING_CARDS)
		shuffled_deck += pile[0:split]
		del pile[0:split]

		if generator:
			yield shuffled_deck + pile1 + pile2

	return shuffled_deck

#aka smooshing
def corgi(deck, generator = False):
	source, target = 0, 0
	while target < 52:
		deck[source], deck[target] = deck[target], deck[source]
		source, target = target, target + randint(1, CORGI_MAX_JUMP)

		if generator:
			yield deck

	return deck
