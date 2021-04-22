import xml
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv


dict_results = []
fieldnames = [
    'code',
    'text',
    'text_uk',
    'text_ru',
    'text_en',
]

with open('page1.html', 'r') as old_html_file:
    soup = BeautifulSoup(old_html_file.read(), 'lxml')

index = 0
for tag in soup.find_all():
    if tag.string is not None and len(list(tag.children)) == 1:
        index += 1
        code = f'code_{index}'
        text_code = ''
        text_code += '{{'
        text_code += f'{code}.text|safe'
        text_code += '}}'
        string = tag.string
        tag.string.replace_with(text_code)
        dict_results.append({
            "code": code,
            'text': string,
            'text_uk': string,
            'text_ru': string,
            'text_en': string,
        })
new_text = soup.prettify()

with open('new_page.html', 'w') as new_html_file:
    new_html_file.write(new_text)


with open('TextResource.csv' , 'a') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for dict_result in dict_results:
        writer.writerow(dict_result)