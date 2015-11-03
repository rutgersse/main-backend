from bs4 import BeautifulSoup
import requests

def gettextdata(url):
	s = requests.get(url)
	return s.text
	
def convertsoup(text):
	return BeautifulSoup(text, 'html.parser')

def extractdata(soup):
	data = {}
	for link in soup.find_all('a'):
		data[link.get_text()] = link.get('href')

	return data

def extractdatalist(soup):
	data = []
	for link in soup.find_all('a'):
		data.append(link.get_text())
	return data

url = 'http://www.citytowninfo.com/places'
start = gettextdata(url)
start = start[start.find('<table>'):start.find('</table>')+8]
# print start
# text = gettextdata(url)
soup = convertsoup(start)
data = extractdata(soup)

final_data = {}
# for k,v in data.items():
# 	print k, v
ulta_list = {}
count = 1
for k,v in data.items():
	if v.count('/') > 4:
		continue
	print str(count) + 'Extracting data for state : ' + k 
	count = count + 1
	text = gettextdata(data[k])
	soup = convertsoup(text)
	# print soup
	soup = soup.select('#cities_and_towns')
	final_data[k] = extractdatalist(soup[0])

	for x in final_data[k]:
		ulta_list[x] = k
	# print final_data[k]
	# print '-----------------------------------------------------'


import json
with open('data.json', 'w') as outfile:
    json.dump(final_data, outfile, sort_keys = True, indent = 4)

with open('ultadata.json', 'w') as outfile:
    json.dump(ulta_list, outfile, sort_keys = True, indent = 4)
    
for k,v in final_data.items():
	print k, v

