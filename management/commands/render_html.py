import os
from typing import NewType

from django.core.management import BaseCommand
from django.conf import settings

from bs4 import BeautifulSoup
from pathlib import Path

from ...models import Text, Link, Mailto, Tel


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--path', default='templates copy')

    def handle(self, *args, **kwargs):
        index = 0
        paths = get_file_paths(kwargs['path'])
        file_paths = paths['file_paths']
        new_file_paths = paths['new_file_paths']
        for html_file in file_paths:
            with open(html_file, 'r', encoding="utf8") as raw_html_file:
                base_file_name = os.path.basename(raw_html_file.name).split('.')[0]
                soup = BeautifulSoup(raw_html_file.read(), 'lxml')
        
            for tag in soup.find('body').find_all():
                if tag.string is not None and len(list(tag.children)) == 1:
                    text = tag.string
                    text_res = Text.objects.create(text=text, page_code=base_file_name)
                    html_code = '{{' + f'text{text_res.pk}.text|safe' + '}}'
                    tag.string.replace_with(html_code)
                    tag['text-id'] = text_res.pk
                    soup.html.insert(0, '{% ' + f'render {text_res.pk} as text{text_res.pk}' + ' %}')
        
            for link_tag in soup.find('body').find_all('link', href=True):
                href = link_tag['href']
                link_res = Link.objects.create(href=href, page_code=base_file_name)
                html_code = '{{' + f'link{link_res.pk}.href|safe' + '}}'
                link_tag['link-id'] = link_res.pk
                soup.html.insert(0, '{% ' + f"render {link_res.pk} 'link' as link{link_res.pk}" + ' %}')
            
            for a_tag in soup.find('body').find_all('a', href=True):
                href = a_tag['href']
                if href.find('tel:') == 0:
                    tel_res = Tel.objects.create(href=href, page_code=base_file_name)
                    html_code = '{{' + f'tel{tel_res.pk}.href|safe' + '}}'
                    a_tag['tel-id'] = tel_res.pk
                    soup.html.insert(0, '{% ' + f"render {tel_res.pk} 'tel' as tel{tel_res.pk}" + ' %}')

            for a_tag in soup.find('body').find_all('a', href=True):
                href = a_tag['href']
                if href.find('mailto:') == 0:
                    mailto_res = Mailto.objects.create(href=href, page_code=base_file_name)
                    html_code = '{{' + f'tel{mailto_res.pk}.href|safe' + '}}'
                    a_tag['tel-id'] = mailto_res.pk
                    soup.html.insert(0, '{% ' + f"render {mailto_res.pk} 'mailto' as mailto{mailto_res.pk}" + ' %}')

            new_html = soup.prettify()
            with open(new_file_paths[index], "w") as file:
                file.write(str(new_html))
            index += 1


def get_file_paths(path):
    base_path =  settings.BASE_DIR / path
    file_paths = []
    new_file_paths = []
    for (dirpath, dirnames, filenames) in os.walk(base_path):
        for file in filenames:
            if '.html' in file[-5:]:
                file_paths.append(Path(dirpath) / file)
                new_file_paths.append(Path(dirpath.replace(path, 'templates')) / file)
    return {'file_paths': file_paths, 'new_file_paths': new_file_paths}

