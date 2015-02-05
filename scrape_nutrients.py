import mechanize

def __contains(s, m):
	if s.find(m) > -1: return True
	return False

def pull_pufas(itemno):
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
	poly = False
	poly_fats = {}
	for tr in trs:
#		print(tr.text)
		tds = tr.find_all('td')
		if tds[0].text.lower().find('polyunsat') > 0:
			poly = True
			continue
		if poly:
			if not tds[0].text.strip()[0].isdigit():
				break
			poly_fats[tds[0].text.splitlines()[0].strip()] = tds[2].text.strip()

#			for td in tds:
#				print(td.text)
	
	return poly_fats

def __is_n6(pufa_name):
	n6_list = [
			'n-6',
			'18:2',
			'20:2',
			'22:2',
			'22:4',
			'24:4',
	]

#	n6_list = [
#			'n-6',
#			'18:2',
#			'18:3',
#			'20:2',
#			'20:3',
#			'20:4',
#			'22:2',
#			'22:4',
#			'22:5',
#			'24:4',
#			'24:5'
#	]

	for p in n6_list:
		if __contains(pufa_name, p) and not __contains(pufa_name, 'undiff'):
			return True

	return False

def __is_n3(pufa_name):
	n3_list = [
			'n-3',
			'16:3',
			'ALA', # 18:3
			'18:4',
			'20:5',
			'21:5',
			'22:6',
			'24:6'
	]

#	n3_list = [
#			'n-3',
#			'16:3',
#			'ALA', # 18:3
#			'18:3',
#			'18:4',
#			'20:3',
#			'20:4',
#			'20:5',
#			'21:5',
#			'22:5',
#			'22:6',
#			'24:5',
#			'24:6'
#	]

	for p in n3_list:
		if __contains(pufa_name, p) and not __contains(pufa_name, 'undiff'):
			return True

	return False

def get_omega_ratio(pufas):
	n3 = 0
	n6 = 0
	undiff = 0
	undiff_list = {}
	n6_list = {}
	n3_list = {}
	for k,v in pufas.items():
		if __is_n3(k):
			n3 += float(v)
			n3_list[k.split()[0]] = float(v)
			#n3_list.append((k.split()[0], float(v)))
		if __is_n6(k):
			n6 += float(v)
			n6_list[k.split()[0]] = float(v)
			#n6_list.append((k.split()[0], float(v)))
		if __contains(k, 'undiff'):
			undiff += float(v)
			undiff_list[k.split()[0]] = float(v)
			#undiff_list.append((k.split()[0], float(v)))

	for k,v in undiff_list.items():
		n3_ = n3_list.get(k, 0)
		n6_ = n6_list.get(k, 0)
		#print(n6_, n3_, v)
		if n3_ == 0 and n6_ == 0:	# assume n6 :(
			if __is_n6(k):
				n6 += v
		elif n3_ == 0:
			if __is_n3(k):
				n3 += v - n6_
		elif n6_ == 0:
			if __is_n6(k):
				n6 += v - n3_

	#print('Undiff: ', undiff)
	#print(n6_list, n3_list, undiff_list)
	return n6, n3

if __name__ == '__main__':
	pufas = pull_pufas(1125)
	print(pufas)
	print(get_omega_ratio(pufas))
	pufas = pull_pufas(1116)
	print(pufas)
	print(get_omega_ratio(pufas))
	pufas = pull_pufas(4660)
	print(pufas)
	print(get_omega_ratio(pufas))
