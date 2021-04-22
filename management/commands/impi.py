from imp_exp.management.commands.utils import set_resource, set_file_path
from django.core.management.base import BaseCommand
import tablib
from django.apps import apps

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--path', default='export')


    def handle(self, *args, **kwargs):
        models = apps.get_models()
        for model in models:
            file_path = set_file_path(model, kwargs['path'])
            resource = set_resource(model)
            dataset = tablib.Dataset()
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                dataset.load(f.read(), format='csv')
                resource.import_data(dataset)
                print(f'{model.__name__:<20} Success!')
