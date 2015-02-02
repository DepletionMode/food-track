#import scrape_food

#today = scrape_food.pull()
#print(today['Breakfast'])
#another = scrape_food.pull('2015-01-29')
#print(another)

import db

db.fill_db()
