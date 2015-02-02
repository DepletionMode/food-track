import scrape_food
import string

class FoodItem():
	def __init__(self, raw):
		self.__deserialize(raw)

	def __deserialize(self, raw):
		self.name, self.amount = [ x.strip() for x in raw[0].rsplit(',', 1) ]
		self.calories, self.carbs, self.fat, self.protein, self.fibre, self.sugar = raw[1]
		self.name = filter(lambda x: x in string.printable, self.name)

		print(self.amount)

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
