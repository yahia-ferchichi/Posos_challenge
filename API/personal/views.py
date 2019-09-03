from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.core.exceptions import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .main import main
from .forms import TextForm

def index(request):
    return render(request, 'personal/home.html')
    

def calculateProba(request):
    ''' 
        This function retrieve the user's question from the UI
        and sends the informations about it back to the UI
        using the classifier from main
    '''
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            pred = main(str(form.cleaned_data['your_text']))
            return render(request, 
                          'personal/result.html', 
                          {'content':
                              ["La question '" + 
                               str(form.cleaned_data['your_text']) + 
                               "' est dans le context de type " + 
                               str(pred[0]) + 
                               " avec une probabilité de " 
                               + str(pred[1])]})
    return redirect('/')



    
