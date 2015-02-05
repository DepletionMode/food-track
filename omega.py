from scrape_nutrients import *
import re

def __lookup_usda(name):
	code_list = [
			# regex, code
			('^.*(butter|ghee)+.*$', 132),
			('^.*(salmon)+.*$', 4660),
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
			('^.*(beef)+.*(80)+.*$', 7562),
			('^.*(beef)+.*(70)+.*$', 3956),
			('^.*(steak|entrecote|asado)+.*$', 7315),
			('^.*(milk)+.*(3)+.*$', 180),
			('^.*(milk)+.*(1)+.*$', 154),
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
			('^.*(hummus)+.*$', 4860),
	]

	for regex,c in code_list:
		p = re.compile(regex, re.IGNORECASE)
		m = p.match(name)
		if m != None:
			return c
	
	return None


def get_pufas(food):
	usda_num = __lookup_usda(food)

	if usda_num == None:
		return None

	pufas = pull_pufas(usda_num)
	ratio = get_omega_ratio(pufas)

	return pufas, ratio
