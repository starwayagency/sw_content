import csv
from django.core.management.base import BaseCommand
from datetime import datetime 
from pathlib import Path
from datetime import datetime 
from io import StringIO, BytesIO
from tablib import Dataset
from sw_utils.utils import get_resource, get_resources


class Command(BaseCommand):

  def print_message(self, result):
    if result:
      self.stdout.write(self.style.SUCCESS('DATA EXPORTED SUCCESSFULLY'))
    else:
      self.stdout.write(self.style.ERROR('DATA HAVENT EXPORTED'))

  def add_arguments(self, parser):
    parser.add_argument(
        '-e',
        '--extention',
    )
    
    # 1
    parser.add_argument(
        '-d',
        '--dirname',
    )

    # 2
    parser.add_argument(
        '-i',
        '--init_filename',
    )
    parser.add_argument(
        '-l',
        '--limit',
    )

    # 3
    parser.add_argument(
        '-f',
        '--filename',
    )
    parser.add_argument(
        '-r',
        '--resource_name',
    )

  def handle(self, *args, **kwargs):

    # 1
    init_filename = kwargs.get('init_filename')
    limit         = kwargs.get('limit')

    # 2
    dirname = kwargs.get('dirname')
    time    = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    if not dirname is None: 
      dirname = f'{dirname}_{time}'
    else:
      dirname = time

    # 3
    resource_name = kwargs.get('resource_name')
    filename      = kwargs.get('filename')
    if filename is None and resource_name is not None:
      # filename = resource_name + '.' + ext 
      filename = resource_name + '.csv' 

    ext = kwargs['extention']
    if ext is None:
      if filename is None:
        ext = 'csv'
      else:
        ext = filename.split('.')[-1]

    # 1
    if not init_filename and not filename:
      result = self.export_many_from_resources(dirname, ext)
      self.print_message(result)
      return 

    # 2
    if init_filename:
      result = self.export_many_from_init_file(init_filename, ext, limit)
      self.print_message(result)
      return 

    # 3
    if resource_name:
      result = self.export_one(resource_name, filename, ext)
      self.print_message(result)
      return 

  # 1
  def export_many_from_resources(self, dirname, ext):
    for resource in get_resources():
      self.export(resource, dirname, ext)
    return True 

  # 2
  def export_many_from_init_file(self, init_filename, dirname, ext, limit=None):
    items = [dct for dct in map(dict, csv.DictReader(open(init_filename)))] 
    if limit: items = items[:limit]
    for item in items:
        print(item)
        if bool(int(item['load'])):
          self.export(
            resource=get_resource(item['resource_name']), 
            dirname=dirname,
            ext=item['extention'],
          )
    return True 

  # 3
  def export_one(self, resource_name, filename, ext):
    with open(filename, 'w') as f:
      f.write(getattr(get_resource(resource_name)().export(), ext))

  def export(self, resource, dirname, ext):
    print(resource)
    if resource._meta.model:
      app_label   = resource._meta.model._meta.app_label
      folder_name = f'export/{dirname}/{app_label}/' 
      file_name   = f'{resource.__name__}.{ext}'
      path_name   = folder_name + file_name
      Path(folder_name).mkdir(parents=True, exist_ok=True)
      with open(path_name, 'w') as f:
        f.write(getattr(resource().export(), ext))

