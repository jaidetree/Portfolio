from blog.models import Post
from projects.models import Project
from media.models import Media
from content.models import ContentSection
from django.shortcuts import render
from django.template import RequestContext
from oneoffs.forms import ContactForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
import urllib2

def home(request):
    projects = Project.completed.all()[:6]
    featured_projects = Project.objects.filter(featured=True)[:3]
    articles = Post.published_posts.all()[:5]

    data = { 
            'is_home': True,
            'projects': projects,
            'featured_projects': featured_projects,
            'articles': articles
           }
    return render(request, 
        'home.html', 
        data, 
        context_instance=RequestContext(request))

def about(request):
    sections = {'about': '', 'values':'', 'logo':''}

    for slug, content in sections.items():
        sections[slug] = ContentSection.objects.get(slug=slug).html

    media = {
                'headshot': Media.objects.get(slug="headshot-nov-8-2011").file
            }

    data = {'sections': sections, 'media': media}

    # exit(RequestContext(request)) 
    return render(request, 'about.html', data, context_instance=RequestContext(request))

def contact(request):
    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():
            subject = 'Test: ' + form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            is_a_bot = request.POST['is_a_bot'] if request.POST.has_key('is_a_bot') else False


            if is_a_bot:
                return HttpResponse("No bots bro!")

            recipients = ['jayzawrotny@gmail.com']

            if cc_myself:
                recipients.append(sender)

            headers = { 'Reply-To': sender }
            message = sender + " writes:\r\n\r\n" + message
            msg = EmailMessage(subject, message, 'postmaster@jayzawrotny.com', recipients, [], headers=headers)
            msg.send()

            return HttpResponseRedirect('/contact/thanks')
        else:
            pass

    data = {
        'form': ContactForm(),
        'content': { 
            'contact': ContentSection.objects.get(slug='contact').html,
            'media': ContentSection.objects.get(slug='contact-media').html,
        } 
    }
    return render(request, 'contact.html', data, context_instance=RequestContext(request))

def contact_thanks(request):
    data = {}
    return render(request, 'contact_thanks.html', data, context_instance=RequestContext(request))

def latest_dribbble_shot(request):
    data = urllib2.urlopen("http://api.dribbble.com/players/jayzawrotny/shots");
    return HttpResponse(data, mimetype="application/json")

