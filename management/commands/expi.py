from django.core.management.base import BaseCommand
from django.apps import apps
from .utils import set_resource, set_file_path, set_folder_path


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--path', default='export')

    def handle(self, *args, **kwargs):
        models = apps.get_models()
        for model in models:
            folder_path = set_folder_path(model, kwargs['path'])
            file_path = set_file_path(model, kwargs['path'])
            folder_path.mkdir(parents=True, exist_ok=True)
            resource = set_resource(model)
            dataset = resource.export()
            with open(file_path, 'w', newline='', encoding='utf8') as f:
                f.write(dataset.csv)
            print(f'{model.__name__:<20} Success!')
