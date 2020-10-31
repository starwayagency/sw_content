from django.conf import settings 
from django.utils.html import mark_safe, strip_tags
from django.shortcuts import reverse, render
from django.template.loader import render_to_string

from box.core.sw_content.models import *



def set_page(obj, page_code=None):
    if page_code:
        page = Page.objects.filter(code=page_code)
        if page.exists:
            obj.page = page.first() 
            obj.save()


def get_class(content_type):
    mapper = {
        'map':     Map,
        'img':     Img,
        'tiny':    Text,
        'plain':   Text,
        'address': Address,
        'tel':     Tel,
        'mailto':  Mailto,
        'link':    Link,
        'slider':  Slider,
        'slide':   Slide,
    }
    if 'box.apps.sw_shop.sw_catalog' in settings.INSTALLED_APPS:
        from box.apps.sw_shop.sw_catalog.models import Item, ItemCategory
        mapper.update({
            'item':          Item,
            'item_category': ItemCategory,
        })
    if 'box.apps.sw_blog' in settings.INSTALLED_APPS:
        from box.apps.sw_blog.models import Post, PostCategory
        mapper.update({
            'post':          Post,
            'post_category': PostCategory,
        })
    return mapper[content_type] 



def get_context(content_code, content_type='plain', page_code=None):
    klass = get_class(content_type)
    # klass.objects.all().delete()
    obj = klass.objects.get_or_create(code=content_code)[0]
    if content_type == 'slider':
        obj = Slide.objects.all().filter(slider=obj)
    # set_page(obj=obj, page_code=page_code)
    context = {
        'obj':obj,
    }
    return context 


