from django.core.management.base import BaseCommand
from datetime import datetime 
from pathlib import Path
from io import StringIO, BytesIO
from tablib import Dataset
from sw_utils.utils import get_resource, get_resources
import os, shutil, glob, csv 

from django.core.exceptions import ObjectDoesNotExist



class Command(BaseCommand):

  def print_message(self, result):
    if result:
      self.stdout.write(self.style.SUCCESS('Data imported successfully'))
    else:
      self.stdout.write(self.style.ERROR('DATA HAVENT IMPORTED'))

  def add_arguments(self, parser):
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
    # 3 
    parser.add_argument(
        '-f',
        '--filename',
    )
    parser.add_argument(
        '-e',
        '--extention',
    )
    parser.add_argument(
        '-r',
        '--resource_name',
    )

  def handle(self, *args, **kwargs):

    # 1
    dirname       = kwargs.get('dirname')
    if dirname is None:
      dirname = 'export/'
    
    # 2
    init_filename = kwargs.get('init_filename')
    
    # 3
    filename      = kwargs.get('filename')
    ext           = kwargs.get('extention')
    resource_name = kwargs.get('resource_name')

    if ext is None:
      if filename is not None:
        ext = filename.split('.')[-1]
      else:
        ext = 'csv'

    if resource_name is None and filename is not None:
      resource_name = f"{filename.split('/')[-1].split('.')[0]}"

    # 1
    if not init_filename and not filename:
      result = self.import_from_folder(dirname)

      self.print_message(result)
      return 

    # 2
    if init_filename:
      result = self.import_from_init_file(init_filename)
      self.print_message(result)
      return 

    # 3
    if filename:
      result = self.import_one(filename, resource_name, ext)
      self.print_message(result)
      return 

  # 1
  def import_from_folder(self, dirname):
    if dirname == 'export/':
      path = max(glob.glob(os.path.join(dirname, '*/')), key=os.path.getmtime)
    else:
      path = dirname 
    paths = []
    for root, dir, files in os.walk(path):
      for file in files:
        x = f'{root}/{file}'.replace('//','/')
        paths.append(x)
    for path in paths:
      raw = path.split('/')[-1].split('.')
      result = self.load(path, resource_name=raw[0], ext=raw[1])
      # print(result)
    return True 

  # 2 
  def import_from_init_file(self, init_filename):
    items = [dct for dct in map(dict, csv.DictReader(open(init_filename)))] 
    # TODO: зробити шось з порядком імпортів
    for item in items:
      # print(item)
      if bool(int(item['load'])):
        res = self.load(
          filename=item['filename'], 
          resource_name=item['resource_name'], 
          ext=item['extention'],
        )
    return True 

  # 3
  def import_one(self, filename, resource_name, ext):
    result = self.load(filename, resource_name, ext)
    # result = result['status']
    return result 

  def load(self, filename, resource_name, ext):
    errors = []
    Resource = get_resource(resource_name)
    print("Resource: ", Resource)
    dataset  = Dataset()
    with open(filename, mode='r', encoding='utf-8') as f:
      # imported_data = dataset.load(f.read())
      dataset.load(f.read(), format=ext)
    result = Resource().import_data(dataset, dry_run=True)
    if not result.has_errors():
      Resource().import_data(dataset, dry_run=False)  
      return True 
    else:
      for error in result.row_errors():
        row = error[0]
        error = error[1][0]
        try:
          raise error.error
          # raise Exception(error.error)
        except ObjectDoesNotExist:
          errors.append(error.error)
        print(f"ERROR IN {row} LINE IN FILE {filename}:", error.error)
        # return self.load(filename,resource_name,ext)
      return {
        "status":"OK",
        "errors":errors,
      } 



import import_export



