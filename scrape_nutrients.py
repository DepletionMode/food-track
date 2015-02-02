import mechanize
def pull(itemno):
	br = mechanize.Browser()
	#br.set_all_readonly(False)
	br.set_handle_robots(False)
	br.set_handle_refresh(False)
	br.addheaders = [('User-agent','Firefox')]

	resp = br.open('http://ndb.nal.usda.gov/ndb/foods/show/{}?fg=&man=&lfacet=&count=&max=&sort=&qlookup=&offset=&format=Full&new=&measureby='.format(itemno))
	#print resp.read()

	from bs4 import BeautifulSoup
	soup = BeautifulSoup(resp.read())

#	trs = soup.find_all('tr', id='Lipids-0')
	trs = soup.find_all('tr', class_='odd')
	for tr in trs:
#		print(tr.text)
		tds = tr.find_all('td')
		if tds[0].text.lower().find('polyunsat') > 0:
#		for td in tds:
			print(tds[0].text)
pull(4660)

#	table = soup.find_all('table', class_='table0')[0]
#	trs = table.find_all('tr')
#	meal = ''
#	food = {}
#	for tr in trs:
#		classes = tr.attrs.get('class',[])
#		if 'bottom' in classes: continue
#		if 'total' in classes: continue
#		if 'meal_header' in classes:
#			td = tr.find_all('td', class_='first')[0]
#			meal = td.text
#			food[meal] = []
#			continue
#		tds = tr.find_all('td')
#		if tds[0].a == None: break
#		item = tds[0].a.text
#		info = []
#		for td in tds[1:-1]:
#			info.append(td.text)
#		food[meal].append((item,info))
#
#	return food
