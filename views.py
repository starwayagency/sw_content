from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Page 


from functools import wraps


def handle_route(function):
    @wraps(function)
    def wrap(request, slug, *args, **kwargs):
        # page = get_object_or_404(Page, code=code)
        page = get_object_or_404(Page, slug=slug)
        print('babski')
        return render(request, 'dev/index.html', locals())

        return function(request, *args, **kwargs)
    return wrap



# @handle_route
def page(request, code):
    page = get_object_or_404(Page, code=code)
    print('babski contacts')
    # template = 'dev/index.html'
    template = f'dev/{page.code}.html' 

    return render(request, template, locals())




