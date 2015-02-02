import mechanize
import config

def pull(date=None, login=True):
	br = mechanize.Browser()
	#br.set_all_readonly(False)
	br.set_handle_robots(False)
	br.set_handle_refresh(False)
	br.addheaders = [('User-agent','Firefox')]

	login = True	# always login for now
	if login:
		url = 'http://www.myfitnesspal.com/account/logout'
		resp = br.open(url)

		br.form = list(br.forms())[0]
		br["username"] = config.USERNAME
		br["password"] = config.PASSWORD
		resp = br.submit()

	if date == None: date = ''
	else: date = '?date='+date
	resp = br.open('http://www.myfitnesspal.com/food/diary/davkaplan' + date)
	#print resp.read()

	from bs4 import BeautifulSoup
	soup = BeautifulSoup(resp.read())
	table = soup.find_all('table', class_='table0')[0]
	trs = table.find_all('tr')
	meal = ''
	food = {}
	for tr in trs:
		classes = tr.attrs.get('class',[])
		if 'bottom' in classes: continue
		if 'total' in classes: continue
		if 'meal_header' in classes:
			td = tr.find_all('td', class_='first')[0]
			meal = td.text
			food[meal] = []
			continue
		tds = tr.find_all('td')
		if tds[0].a == None: break
		item = tds[0].a.text
		info = []
		for td in tds[1:-1]:
			info.append(td.text)
		food[meal].append((item,info))

	return food
