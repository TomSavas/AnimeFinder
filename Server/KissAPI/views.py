from django.http import HttpResponse
from django.views.static import serve
import os

def GetDB(request):
    filepath = '../anime.db'
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
