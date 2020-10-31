from ..models import * 
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import JsonResponse



@api_view()
def contents_list(request):
    
    return Response()



@api_view()
def content(request, code):
    return Response({
        "code":code
    })
    return JsonResponse({})
