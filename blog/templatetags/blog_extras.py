from django import template
register = template.Library()
from django.conf import settings
from django.template.defaultfilters import stringfilter
import os.path
import tweepy

@register.filter
@stringfilter
def templatename(post_type, folder):
    template_path = folder + "/posttypes/"
    full_file_path = settings.SITE_ROOT + "/" + folder + "/templates/" + template_path + post_type + ".html"

    if os.path.isfile(full_file_path):
        return template_path + post_type + ".html" 
    else:
        return False

@register.filter
@stringfilter
def get_tweet(tweet_id):
    try:
        tweet = tweepy.api.get_status(tweet_id)
    except:
        tweet = {}
    return tweet

@register.filter
def get_photo(article):
    return article.media.filter(featured=1)[0] if article.media.filter(featured=1) else False

@register.filter
@stringfilter
def get_quote(quote_content):
    try:
        data = quote_content.split('--')
        quote = {
                    'content': data[0],
                    'author': data[1] if data[1] else ''
                }
    except:
        quote = {
                    'content':  quote_content
                }

    return quote
