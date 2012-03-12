from django.contrib.syndication.views import Feed
from blog.models import Post

class LatestPostsFeed(Feed):
    title = "Jay Zawrotny's Blog Articles"
    link = "/blog/"
    description = "A blog on web design, development, general design, and industry insight."

    def items(self):
        return Post.published_posts.all()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_html()

    def item_link(self, item):
        return item.get_absolute_url()
