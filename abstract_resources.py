from import_export.resources import ModelResource

from .abstract_models import * 
from .models import Page 

from box.core.utils import get_multilingual_fields


class AbstractContentResource(ModelResource):

    def get_export_order(self):
        export_order = [
            'page',
            'code',
        ]
        return export_order
    
    def get_import_id_fields(self):
        import_id_fields = [
            'code',
        ]
        return import_id_fields

    def dehydrate_page(self, obj):
        page = None 
        if obj.page: page = obj.page.code 
        return page 

    def before_import_row(self, row, **kwargs):
        if row['page']:
            page_code   = row['page']
            page        = Page.objects.get_or_create(code=page_code)[0]
            row['page'] = page.id


class AbstractTextResource(AbstractContentResource):
    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        export_order = [
            *multilingual_fields['text']
        ]
        return super().get_export_order() + export_order


class AbstractLinkResource(AbstractTextResource):
    def get_export_order(self):
        export_order = [
            'href',
        ]
        return super().get_export_order() + export_order


