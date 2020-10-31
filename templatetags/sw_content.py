from django import template
from django.shortcuts import render 
from django.template.loader import render_to_string 

from ..editor import get_context


register = template.Library()

@register.simple_tag
def render(content_code, content_type='plain', page_code=None):
    context = get_context(content_code=content_code, content_type=content_type, page_code=page_code)
    return context['obj']


