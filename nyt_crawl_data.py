import requests
import regex as re
from bs4 import BeautifulSoup
import json

def fetch_data_from_source(nyt_eco_url):
	print('------------------------')
	print('crawling economic articles from ', nyt_eco_url)
	print('------------------------')
	print('sending request')
	nyt_eco = requests.get(nyt_eco_url)	
	print('------------------------')
	print('Retrieving necessary text data')
	print('------------------------')
	pattern = r'class="css.*?(-[a-zA-Z0-9]+ [a-zA-Z0-9]+)(.*?)</p><p.*?class="css'
	matches = re.findall(pattern, nyt_eco.text, re.DOTALL)
	print(matches)
	print('Data from ',nyt_eco_url,'retrieved')
	return matches 

def processing_text_data(matches):
	print('------------------------------')
	print('processing retrieved text data')
	print('------------------------------')
	print('Spliting Url values')
	print('------------------------------')
	for data in matches:
		title = data[1].split("""">""")[-2]
		content = data[1].split("""">""")[-1]
	print('------------------------------')
	print('Finalizing JSON output')
	print('------------------------------')
	processed_matches = list(map(
        lambda data: {
            'title': data[1].split("""">""")[-2],
            'content': data[1].split("""">""")[-1]
        },
        matches
    ))
	for data in processed_matches:
		data['title'] = data['title'].split('</h3')[0]
	print(processed_matches)
	return processed_matches 

def export_to_json(processed_matches):
	print('------------------------------')
	print('Exporting data to Json')
	print('------------------------------')
	with open('data_nyt.json', 'w') as fp:
		json.dump(processed_matches, fp)

def main():
	nyt_eco_url = 'https://www.nytimes.com/section/business/economy'
	data = fetch_data_from_source(nyt_eco_url)
	processed_data = = processing_text_data(data)
	export_to_json(processed_data)
	print('Finished processing data from ',nyt_eco_url)
	
main()
	
	

