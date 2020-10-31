from django.urls import path, include 
from .views import * 


urlpatterns = [
    path('', include('box.core.sw_content.api.urls')),
    # path('<code>/',  page,  name='page'),
]











# from django.conf import settings 
# from django.shortcuts import render 

# from django.conf import settings 
# # CMS_TEMPLATES = settings.CMS_TEMPLATES 

# from functools import partial




# class Dynamo(object):
#     def __init__(self):
#         pass

#     @staticmethod
#     def init(function_name):
#         dynamo = Dynamo()
#         code = f'''
#             def {function_name}(self, request):
#                 from django.shortcuts import render
#                 return render(request, "{function_name}.html", locals())
#         '''
#         result = {}
#         exec(code.strip(), result)
#         setattr(dynamo.__class__, name, result[name])
#         return dynamo




# for template_name in CMS_TEMPLATES:
#     function_name = template_name.split('.')[0]
#     url = function_name + '/'
#     name = function_name 
#     service = Dynamo.init(function_name)
#     urlpatterns.append(partial(path, url, partial(getattr(service, function_name)), name=name)())


