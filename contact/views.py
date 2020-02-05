from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import QuestionAndAnswer
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template
from django.views import generic

# add to your views
def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')

            template = get_template('contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact from your patient from the websites. ",
                content,
                "Your website" +'',
                ['aerilxx@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return render(request, 'sendContactSucess.html')

    return render(request, 'contact.html', {'form': form_class,})

class Questions(generic.ListView):
    queryset = QuestionAndAnswer.objects.all()
    post_list = QuestionAndAnswer.objects.raw('SELECT * FROM contact_qanda')
    template_name = 'questionsAndAnswer.html'
