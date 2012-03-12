from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.tag
def sidebox(parser, token):
    args = token.split_contents()

    # Get the sidebar title, if there is one.
    title = parser.compile_filter(args[1]) if len(args) > 1 else ""

    # Get teh sidebar class_name, if there is one.
    class_name = parser.compile_filter(args[2]) if len(args) > 2 else ""

    # Parse upuntil {% endsidebox %}
    nodelist = parser.parse(('endsidebox',))

    # Delete the {% sidebox %} token???
    parser.delete_first_token()

    return WidgetNode(nodelist, title, class_name)

class WidgetNode(template.Node):
    def __init__(self, nodelist, title, class_name):
        self.nodelist = nodelist
        self.title = title or ""
        self.class_name = class_name or ""

    def render(self, context):                                                       
        # Set our two variables if available else use empty string.
        title = self.title.resolve(context) if self.title else ""
        class_name = self.class_name.resolve(context) if self.class_name else ""

        # Loads our main _widget.html template.
        output = template.loader.get_template('_widget.html')

        # Not really sure what this does I admit but it was in the docs
        # for including a template in a template tag.
        # Has something to do with rendering the content first.
        tmpl = template.Template(self.nodelist.render(context))

        # Mark our content as HTML safe and strip trailing/leading newlines.
        content = mark_safe(tmpl.render(context).strip('\n'))

        # Set the data we're going to pass to the template. 
        # content is the inner html the sidebox template tags are 
        # wrapped around.
        data = {'content': content, 'title': title, 'class_name': class_name}

        # Return the rendered template file's html with the content now inside of it. 
        return output.render(template.Context(data))

@register.filter
def parse(value):
    t = template.Template(value)
    c = template.Context({})
    return t.render(c)

@register.tag
def parsecontent(parser, token):
    # Parse upuntil {% endsidebox %}
    nodelist = parser.parse(('endcontent',))

    # Delete the {% sidebox %} token???
    parser.delete_first_token()

    return ContentNode(nodelist )

class ContentNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):                                                       

        tmpl = template.Template(self.nodelist.render(context))

        # Mark our content as HTML safe and strip trailing/leading newlines.
        content = tmpl.render(context)

        # Return the rendered template file's html with the content now inside of it. 
        return content
