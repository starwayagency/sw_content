from import_export.resources import ModelResource

from box.core.utils import get_multilingual_fields
from .abstract_resources import (
    AbstractContentResource, AbstractLinkResource, 
    AbstractTextResource,
)
from .models import *

base_exclude = [
    'id',
    'created',
    'updated',
]



class PageResource(ModelResource):
    class Meta:
        model = Page
        exclude = base_exclude
       

    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        export_order = [
            'code',
            *multilingual_fields['meta_title'],
            *multilingual_fields['meta_descr'],
            *multilingual_fields['meta_key'],
        ]
        return export_order

    def get_import_id_fields(self):
        import_id_fields = [
            'code',
        ]
        return import_id_fields


class MapResource(AbstractContentResource):
    class Meta:
        model = Map 
        exclude = base_exclude

    def get_export_order(self):
        export_order = [
            'html',
        ]
        return super().get_export_order() + export_order


class ImgResource(AbstractContentResource):
    # TODO: не імпортується alt_ru
    class Meta:
        model = Img 
        exclude = base_exclude 

    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        export_order = [
            'image',
            *multilingual_fields['alt'],
        ]
        return super().get_export_order() + export_order


# AbstractText

class TextResource(AbstractTextResource):
    class Meta:
        model = Text 
        exclude = base_exclude


class AddressResource(AbstractLinkResource):
    class Meta:
        model = Address 
        exclude = base_exclude


# AbstractLink 

class LinkResource(AbstractLinkResource):
    class Meta:
        model = Link 
        exclude = base_exclude
    

class TelResource(AbstractLinkResource):
    class Meta:
        model = Tel 
        exclude = base_exclude 
    

class MailtoResource(AbstractLinkResource):
    class Meta:
        model = Mailto 
        exclude = base_exclude


# class Social():


class SlideResource(ModelResource):
    class Meta:
        model = Slide 
        exclude = [
            'id',
            'created',
            'updated',
            # 'order',
            'page',
        ]
       

    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        export_order = [
            'code',
            # 'page',
            'slider',
            'image',
            *multilingual_fields['alt'],
            *multilingual_fields['title'],
        ]
        return export_order 

    def get_import_id_fields(self):
        fields = [
            'code',
        ]
        return fields 

    # def dehydrate_page(self, obj):
    #     page = None 
    #     if obj.page:
    #         page = obj.page.code 
    #     return page 
    
    def dehydrate_slider(self, obj):
        slider = None 
        if obj.slider:
            slider = obj.slider.code 
        return slider 

    def before_import_row(self, row, **kwargs):
        # if row['page']:
        #     row['page'] = Page.objects.get_or_create(code=row['page'])[0].id
        if row.get('slider'):
            row['slider'] = Slider.objects.get_or_create(code=row['slider'])[0].id


class SliderResource(ModelResource):
    class Meta:
        model = Slider
        exclude = [
            'id',
            'created',
            'updated',
            'order',
        ]

    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        order = [
            'code',
            'page',
            'name',
        ]
        return order 
    
    def get_import_id_fields(self):
        fields = [
            'code',
        ]
        return fields 

    def dehydrate_page(self, obj):
        page = None 
        if obj.page:
            page = obj.page.code 
        return page 

    def before_import_row(self, row, **kwargs):
        if row['page']:
            row['page'] = Page.objects.get_or_create(code=row['page'])[0].id



