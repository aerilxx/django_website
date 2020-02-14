from django.shortcuts import render, redirect

# add to your views
def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def panel(request):
	return render(request, 'userPanel.html')

def service(request):
	return render(request, 'service.html')