import sys, getopt
from collections import OrderedDict
import json;
from pprint import pprint

def getMenuItemGroupLinkList(menuLinkList):
	menuListHtml = []
	menuListHtml.append('<ul>')
	for item in menuLinkList:
		menuListHtml.append('\t<li> <a title=""'+item['title'].replace('&','&amp;')+'"" href=""' + item['url'] + '""> ' + item['title'].replace('&','&amp;') + '</a> </li>')
	menuListHtml.append('</ul>')
	
	return menuListHtml

def getItemGroupHtml(category, option, itemGroupJson):
	itemGroupHtml = [];
	itemGroupHtml.append('<li class=""drop__column-block"">');
	itemGroupHtml.append('\t<a href=""'+itemGroupJson['url']+'"" class="drop__head-item"> <i class=""icn icn__'+itemGroupJson['iconClassName']+'""></i> <span>'+itemGroupJson['title']+'</span> </a>')
	if 'links' in itemGroupJson:
		itemGroupHtml.append('\n\t'.join(getMenuItemGroupLinkList(itemGroupJson['links'])))
	itemGroupHtml.append('</li>');
	return itemGroupHtml;

def getSortOptionMenuHtml(category, option, optionJson, display):
	menuHtml = [];
	menuHtml.append('<div id=""nav__home-'+category+'-'+option.lower().replace(' ','-')+'"" class=""drop__content-item"" style=""display: '+display+';"">')
	for menuCol in optionJson:
		menuHtml.append('\t<ul class=""drop__column column-two"">')
		for itemGroup in menuCol:
			menuHtml.append("\t\t".join(getItemGroupHtml(category, option, itemGroup)))
		menuHtml.append('</ul>')
	menuHtml.append('</div>')
	return menuHtml;

def getCategoryHtml(category, categoryJson):
	categoryHtml = [];
	categoryMenuHtml = [];
	categoryHtml.append('<ul class=""drop drop--mega"">')
	if 'sort_options' in categoryJson:
		categoryHtml.append('<div class=""drop__sort ""> <span class=""drop__sort-label"">Shop by:</span>')
		categoryHtml.append('\t<ul class=""drop_sort-items"">')
		counter = 0
		for opts, optsJson in categoryJson['sort_options'].iteritems():
			categoryHtml.append('\t\t<li> <a href=""javascript:void(0)"" class=""drop__tab-but active"" data-expand=""nav__home-'+category + '-' + opts.lower().replace(' ', '-') + '"">' + opts + '</a> </li>')
			categoryMenuHtml.append(''.join(getSortOptionMenuHtml(category, opts, optsJson, 'block' if counter==0 else 'none')))
			counter = counter +1
		categoryHtml.append('\t</ul>')
		categoryHtml.append('</div>')
		categoryHtml.append('<div class=""drop__content-wrapper"">')
		categoryHtml.append('\n\t'.join(categoryMenuHtml))
		categoryHtml.append('</div>')
	
	categoryHtml.append('</ul>')
	return categoryHtml;

def main(argvs):
	inputfile = ''
	outputfile = ''
	category = ''
	commandExample = 'Correct Usage : nav.py -i <inputfile> -o <outputfile> -c <category>'
	## Read Command line args
	try:
		opts, args = getopt.getopt(argvs,"hi:o:c:",["ifile=","ofile=","category="])
	except getopt.GetoptError as err:
		print commandExample
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print commandExample
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-c", "--category"):
			category = arg
	print category

	# Open and parse the input file as JSON
	with open(inputfile) as nav_file:
		nav = json.load(nav_file, object_pairs_hook=OrderedDict)
	# Convert the selected JSON into required HTML
	html = "\n".join(getCategoryHtml(category,nav[category]))
	outFile = open(outputfile, 'w')
	outFile.write(html)
	outFile.close()

if __name__ == "__main__":
   main(sys.argv[1:])