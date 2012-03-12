from blog.models import Post, Category
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import datetime, timedelta
from django.http import Http404

def index(request):
    post_list = Post.published_posts.all()
    paginator = Paginator(post_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    categories = Category.objects.all() 

    data = { 
            'articles': posts,
            'categories': categories,
            'popular_articles': get_popular_articles()
            }

    return render_to_response('blog/index.html', 
                              data, 
                              context_instance=RequestContext(request))

def show(request, article_slug):
    try:
        article = Post.objects.get(slug=article_slug)
    except Post.DoesNotExist:
        raise Http404
    
    save = article.save_html()
    
    if not request.user.is_staff:
        article.views = article.views + 1
        article.popularity_rank = calc_pop_rank(article)
        save = True
        
    if save:
        article.save()


    data = {
            'article': article,
            'popular_articles': get_popular_articles()
            }

    return render_to_response( 'blog/show.html', data, context_instance=RequestContext(request))

def category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    post_list = category.posts.filter(date_published__lte=datetime.now()).filter(status="published")
    paginator = Paginator(post_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    categories = Category.objects.all() 

    data = { 
            'articles': posts,
            'categories': categories,
            'category': category
            }

    return render_to_response('blog/index.html',
                                data,
                                context_instance=RequestContext(request))

def calc_pop_rank(article):
    record_time = datetime.now() - article.date_published
    record_time = record_time.total_seconds()

    return ( article.views - 1 ) / ( record_time / 60 / 60 ) 

def get_popular_articles():
    return Post.published_posts.order_by('-popularity_rank')[:10]
