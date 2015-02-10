from scrape_nutrients import *
import re

def __contains(s, m):
	if s.find(m) > -1: return True
	return False

def __degredient(name):
	names = []
	if __contains(name, "lindt excellence 85%"):
		names.append("cocoa butter");
	else:
		names.append(name)
	return names

def __lookup_usda(name):
	names = __degredient(name)

	code_list = [
			# regex, code
			('^.*(butter|ghee)+.*$', 132),
			('^.*(salmon)+.*$', 4660),
			('^.*(herring)+.*$', 4496),
			('^.*(chicken)+.*(thigh)+.*(skin)+.*$', 1125),
			('^.*(chicken)+.*(thigh)+.*$', 1116),
			('^.*(chicken)+.*(drumstick)+.*(skin)+.*$', 1122),
			('^.*(chicken)+.*(drumstick)+.*$', 872),
			('^.*(chicken)+.*(wing)+.*(skin)+.*$', 902),
			('^.*(chicken)+.*(wing)+.*$', 906),
			('^.*(chicken)+.*(breast)+.*(skin)+.*$', 859),
			('^.*(chicken)+.*(breast)+.*$', 863),
			('^.*(oil)+.*(coconut)+.*$', 636),
			('^.*(oil)+.*(olive)+.*$', 637),
			('^.*(coconut)+.*(oil)+.*$', 636),
			('^.*(olive)+.*(oil)+.*$', 637),
			('^.*(soy)+.*(oil)+.*$', 745),
			('^.*(canola)+.*(oil)+.*$', 745),
			('^.*(oil)+.*(canola)+.*$', 695),
			('^.*(suet)+.*$', 3826),
			('^.*(beef)+.*(80)+.*$', 7562),
			('^.*(beef)+.*(70)+.*$', 3956),
			('^.*(steak|entrecote|asado)+.*$', 7315),
			('^.*(milk)+.*(3)+.*$', 180),
			('^.*(milk)+.*(1)+.*$', 154),
			('^.*(1)+.*(milk)+.*$', 154),
			('^.*(cheese)+.*(emek)+.*$', 40),	# swiss cheese?
			('^.*(cheese)+.*(edam)+.*$', 18),
			('^.*(cheddar)+.*$', 9),
			('^.*(avocado)+.*$', 2205),
			('^.*(sweet)+.*(potato)+.*(cooked)+.*$', 3243),
			('^.*(sweet)+.*(potato)+.*(raw)+.*$', 3242),
			('^.*(coconut)+.*(meat)+.*$', 3688),
			('^.*(chicken)+.*(liver)+.*$', 827),
			('^.*(mayo)+.*$', 624),
			('^.*(veal)+.*$', 5215),
			('^.*(lettuce)+.*$', 3036),
			('^.*(apple)+.*$', 2171),
			('^.*(cabbage)+.*$', 2929),
			('^.*(pistachio)+.*$', 3717),
			('^.*(strawberry|strawberries)+.*$', 2430),
			('^.*(cauliflower)+.*$', 2944),
			('^.*(hummus)+.*$', 4848),  # using value for home instead of commercial
			('^.*(cocoa)+.*(butter)+.*$', 654),
	]

	codes = []
	for name in names:
		for regex,c in code_list:
			p = re.compile(regex, re.IGNORECASE)
			m = p.match(name)
			if m != None:
				codes.append(c)
	
	return codes

import copy
pufa_cache = dict()
def get_pufas(food):
	usda_nums = __lookup_usda(food)
	if len(usda_nums) == 0:
		return None

	master_pufas = {}

	for usda_num in usda_nums:
		pufas = pufa_cache.get(usda_num, None)
		if pufas == None:
			pufas = pull_pufas(usda_num)
			pufa_cache[usda_num] = copy.deepcopy(pufas)
		#pufas = copy.deepcopy(pufas)
		for k,v in pufas.items():
			master_pufas[k] = master_pufas.get(k, 0) + float(v)

	return master_pufas, get_omega_ratio(master_pufas)
