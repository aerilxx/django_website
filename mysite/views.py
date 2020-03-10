from django.shortcuts import render, redirect

# add to your views
def index(request):
    return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def privacy(request):
	return render(request, 'privacy.html')

def service(request):
	return render(request, 'service.html')