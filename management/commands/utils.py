from django.conf import settings
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget


def set_resource(model):
    resource = resources.modelresource_factory(model=model)()
    resource.Meta.model = model
    resource.Meta.fields = []
    concrete_fields = model._meta.concrete_fields
    for field in model._meta.get_fields():
        if field in concrete_fields and not field.many_to_many:
            resource.Meta.fields.append(field.name)
            if field.many_to_many:
                resource.Meta.fields.append(field.name)
                related_model = field.related_model
                command = f'resource.{field.name} = fields.Field(widget=ManyToManyWidget(related_model))'
                data = {
                    'resource': resource,
                    'fields': fields, 
                    'related_model': related_model, 
                    'ManyToManyWidget': ManyToManyWidget
                }
                exec(command, data)
    return resource

def set_file_path(model, base_path):
    label = model._meta.label
    folder_label = label[:label.rfind('.')]
    file_name = label[label.rfind('.') + 1:] + '.csv'
    file_path = settings.BASE_DIR / base_path / folder_label / file_name
    return file_path

def set_folder_path(model, base_path):
    label = model._meta.label
    folder_label = label[:label.rfind('.')]
    folder_path = settings.BASE_DIR / base_path / folder_label
    return folder_path

