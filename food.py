import scrape_food
import string

def __contains(s, m):
	if s.find(m) > -1: return True
	return False

def __hack_lindt_excellence_85(r):
	if __contains(r, 'lindt excellence') and __contains(r, 'block'):
		toks = r.split()
		g = float(toks[-3]) * 10
		r = '{}, {} g'.format(r.split(',')[0], g)
	return r

def __hack_tomatoes_chopped(r):
	if __contains(r, 'tomatoes - red, ripe') and __contains(r, 'chopped or sliced'):
		toks = r.split(',')
		toks[-2], toks[-1] = toks[-1], toks[-2]
		r = ','.join(toks)
	return r

def __hack_cabbage_savoy_shredded(r):
	if __contains(r, 'cabbage - savoy'):
		toks = r.split(',')
		toks[-2], toks[-1] = toks[-1], toks[-2]
		r = ','.join(toks)
	return r

hacks = [
		__hack_cabbage_savoy_shredded,
		__hack_tomatoes_chopped,
		__hack_lindt_excellence_85
		]

def hack(raw):
	for h in hacks:
		raw = h(raw.lower())
	return raw

def convert_to_grams(amount):
	amount = amount.strip().lower()
	toks = amount.split()

	num = float(toks[0])
	if toks[-1] != 'g' or len(toks) > 2:

		if __contains(amount, 'tbsp'): g = 15
		elif __contains(amount, 'tsp'): g = 5
		elif __contains(amount, 'cup'): g = 250
		elif __contains(amount, 'ml'): g = 1

	else:
		g = 1

	return num * g

class FoodItem():
	def __init__(self, raw):
		self.__deserialize(raw)

	def __deserialize(self, raw):
		name_amount = hack(raw[0])
		self.name, amount = [ x.strip() for x in name_amount.rsplit(',', 1) ]
		self.amount = convert_to_grams(amount)
		self.calories, self.carbs, self.fat, self.protein, self.fibre, self.sugar = raw[1]
		self.name = filter(lambda x: x in string.printable, self.name)
		print(self.name, self.amount)

class Food():
	def __init__(self, date=None, login=True):
		self.meals = {}
		self.__scrape(date, login)

	def __scrape(self, date, login):
		raw = scrape_food.pull(date, login)
		for k,v in raw.items():
			foods = []
			for raw_food in v:
				foods.append(FoodItem(raw_food))
			self.meals[k.lower()] = foods

# test
#f = Food()
#print(f.meals)
#for f in f.meals['breakfast']:
#	print('{} of {}'.format(f.amount, f.name))
