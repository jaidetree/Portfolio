from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from associates.models import Associate
import re


def index(request):
    agent = request.META.get('HTTP_USER_AGENT').lower()
    data = {
        'featured_people': Associate.objects.filter(inner_circle=True).filter(type="P"),
    }
    template = "index_default.html"

    try: 
        if agent.find('webkit') >= 0 and agent.find('mobile') == -1:
            if agent.find(' chrome/') >= 0:
                m = re.search(r"chrome/([\d]+)", str(agent))
                if int(m.group(1)) >= 18:
                    template = "index_svg.html"

            elif agent.find('safari') >= 0:
                m = re.search(r"version/([\d]+)", agent)
                if int(m.group(1)) >= 4:
                    template = "index_svg.html"
    except:
        pass

    template = "index_svg.html"
    return render(request, 'associates/' + template, data, context_instance=RequestContext(request))

def show(request, name_slug):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        template = 'associates/show_ajax.html'
        ajax = True
    else:
        template = 'associates/show.html' # Make sure you rename it back to "show.html"
        ajax = False

    associates = Associate.objects.all();
    associate = Associate.objects.get(slug=name_slug)

    data = {
        'associate': associate,
        'associates': associates,
        'ajax': ajax
    }

    context = RequestContext(request)

    return render(request, template, data, context_instance=context)


