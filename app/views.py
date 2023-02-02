from django.shortcuts import render , redirect
from django.http import HttpResponse
from .extras import *
import threading
from .threads import Contert_to_audio
# Create your views here.

def home(request):
    return render(request, 'home.html')

def upload(request):
    file_var = request.FILES['file']
    data = file_to_text(file_var,request)
    return render(request, 'pages.html',context=data)

# def get_audio(request,page_no = None):
#     data = Contert_to_audio(request, page_no).start()
#     print(data)
#     return render(request, "play.html",data)
#     return redirect()
def get_page(request):
    data = request.session['data']
    return render(request, "play.html",data)

def get_audio(request,page_no = None):
    data = text_to_audio(request, page_no)
    return HttpResponse('Done..!')
