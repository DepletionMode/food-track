import food
import sqlite3 as lite
import datetime

def _create_tables(c):
	try:
		c.execute('DROP TABLE Food')
	except:
		pass
	c.execute('CREATE TABLE Food (id INTEGER PRIMARY KEY, meal TEXT, name TEXT, amount TEXT, calories INT, carbs INT, fat INT, protein INT, fibre INT, sugar INT, date TEXT)')

def _populate(c, food, date):
	i = 1
	for k,v in food.meals.items():
		for f in v:
			c.execute("INSERT INTO Food(meal,name,amount,calories,carbs,fat,protein,fibre,sugar,date) VALUES('{}','{}','{}',{},{},{},{},{},{},'{}')".format(k,f.name,f.amount,f.calories,f.carbs,f.fat,f.protein,f.fibre,f.sugar,date))
			i += 1

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days+1)):
        yield start_date + datetime.timedelta(n)

FIRST = True
def _get_food_range(start_date, end_date):
	global FIRST
	foods = []
	
	for date in daterange(start_date, end_date):
		d = date.strftime("%Y-%m-%d")
		print('Pulling {} from server...'.format(d))
		foods.append((d, food.Food(d, FIRST)))
		FIRST = False
	return foods

DAYS = 1
def fill_db(incl_today=True):
	with lite.connect('food.db') as con:
		c = con.cursor()
		_create_tables(c)

		for d,f in _get_food_range(datetime.datetime.now()-datetime.timedelta(days=DAYS), datetime.datetime.now()):
			_populate(c, f, d)
