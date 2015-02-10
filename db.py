import food
import sqlite3 as lite
import datetime

def _drop_table(c, t):
	try:
		c.execute('DROP TABLE {}'.format(t))
	except:
		pass

def _create_tables(c):
	_drop_table(c, 'Food')
	_drop_table(c, 'Pufas')

	c.execute('CREATE TABLE Food (id INTEGER PRIMARY KEY, meal TEXT, name TEXT, amount TEXT, calories INT, carbs INT, fat INT, protein INT, fibre INT, sugar INT, date TEXT)')
	c.execute('CREATE TABLE Pufas (id INTEGER PRIMARY KEY, foodid, n6 INT, n3 INT)')

def _populate(c, food, date):
	for k,v in food.meals.items():
		for f in v:
			c.execute("INSERT INTO Food(meal,name,amount,calories,carbs,fat,protein,fibre,sugar,date) VALUES('{}','{}','{}',{},{},{},{},{},{},'{}')".format(k,f.name,f.amount,f.calories,f.carbs,f.fat,f.protein,f.fibre,f.sugar,date))
			if f.pufas_raw != None:
				c.execute("SELECT max(id) from Food")
				foodid = c.fetchone()[0]
				c.execute("INSERT INTO Pufas(foodid, n6, n3) VALUES({},{},{})".format(foodid,f.n6,f.n3))

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

DAYS_OFFSET = 1
DAYS = 1
def fill_db(incl_today=True):
	with lite.connect('food.db') as con:
		c = con.cursor()
		_create_tables(c)

		for d,f in _get_food_range(datetime.datetime.now()-datetime.timedelta(days=DAYS), datetime.datetime.now()-datetime.timedelta(days=DAYS_OFFSET)):
			_populate(c, f, d)
