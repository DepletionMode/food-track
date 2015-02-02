import scrape_food
import string

def __contains(s, m):
	if s.find(m) > -1: return True
	return False

def __hack_typos(r):
	r = r.replace('tbps', 'tbsp')
	r = r.replace('tablespoon', 'tbsp')
	r = r.replace(' grams', ' g')
	r = r.replace(' gram', ' g')
	r = r.replace(' gr', ' g')
	r = r.replace('milliliters', 'ml')
	r = r.replace(' fl oz', ' fl_oz')
	return r

def __hack_lindt_excellence_85(r):
	if __contains(r, 'lindt excellence') and __contains(r, 'block'):
		toks = r.split()
		g = float(toks[-3]) * 10
		r = '{}, {} g'.format(r.split(',')[0], g)
	return r

def __hack_peppers_chopped(r):
	if __contains(r, 'peppers - sweet') and __contains(r, 'chopped'):
		toks = r.split(',')
		toks[-2], toks[-1] = toks[-1], toks[-2]
		r = ','.join(toks)
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

def __hack_pumpkin_mashed(r):
	if __contains(r, 'pumpkin - cooked') and __contains(r, 'mashed'):
		toks = r.split(',')
		toks[-2], toks[-1] = toks[-1], toks[-2]
		r = ','.join(toks)
	return r

def __hack_tomato_cherry(r):
	if __contains(r, 'tomato') and __contains(r, 'cherry'):
		toks = r.split()
		g = float(toks[-2]) * 17
		r = '{}, {} g'.format(r.rsplit(',', 1)[0], g)
	return r

def __hack_hellmans_mayo(r):
	if __contains(r, 'hellman'):
		r = r.replace('table spoon 15 g', 'tbsp')
	return r

def __hack_goulash_soup(r):
	if __contains(r, 'goulash soup'):
		toks = r.split()
		print(toks)
		g = float(toks[-2]) * 500
		r = '{}, {} g'.format(r.rsplit(',', 1)[0], g)
	return r

def __hack_challa(r):
	# ???
	if __contains(r, 'challa'):
		toks = r.split()
		print(toks)
		g = float(toks[-2]) * 50
		r = '{}, {} g'.format(r.rsplit(',', 1)[0], g)
	return r

hacks = [
		__hack_typos,
		__hack_cabbage_savoy_shredded,
		__hack_tomatoes_chopped,
		__hack_lindt_excellence_85,
		__hack_pumpkin_mashed,
		__hack_tomato_cherry,
		__hack_peppers_chopped,
		__hack_hellmans_mayo,
		__hack_challa,
		__hack_goulash_soup
		]

def hack(raw):
	print(raw)
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
		elif __contains(amount, 'fl_oz'): g = 30
		elif __contains(amount, 'lb'): g = 455

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
