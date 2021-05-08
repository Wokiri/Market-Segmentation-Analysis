from django.shortcuts import render

# Create your views here.
def home_page_view(request):
    template_name = 'pages/homepage.html'
    
    context = {
        'page_name': 'Home',
    }
    return render(request, template_name, context)