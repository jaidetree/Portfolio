from projects.models import Project, Category, Resource
from django.shortcuts import render
from django.template import RequestContext

def show(request, project_slug):

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        template = 'projects/show_ajax.html'
        ajax = True
    else:
        template = 'projects/show.html' # Make sure you rename it back to "show.html"
        ajax = False
    
    project = Project.objects.get(slug=project_slug)
    data = { 
            'project': project,
            'ajax': ajax 
           }

    context = RequestContext(request)

    return render(request,
            template,
            data,
            context_instance=context)

def index(request):
    projects = Project.completed.order_by('category', '-date_created')
    data = { 'projects': projects }

    return render(request, 'projects/index.html', data, context_instance=RequestContext(request))

def resource(request, resource_slug):
    # projects = Project.completed.filter(resource__slug=resource_slug).order_by('category', '-date_created')
    projects = Resource.objects.get(slug=resource_slug).projects.filter(complete=True).exclude(image='').order_by('category', '-date_created')
    data = { 'projects': projects }

    return render(request, 'projects/index.html', data, context_instance=RequestContext(request))
