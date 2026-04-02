from django.templatetags.static import static
from django.urls import reverse
from django.contrib.messages import get_messages
from django.middleware.csrf import get_token
from jinja2 import Environment
from markupsafe import Markup


def csrf_field(request):
    token = get_token(request)
    return Markup(f'<input type="hidden" name="csrfmiddlewaretoken" value="{token}">')


def url(viewname, *args, **kwargs):
    """Wrapper for Django's reverse() to work with Jinja2 template syntax"""
    if args and kwargs:
        return reverse(viewname, args=args, kwargs=kwargs)
    elif args:
        return reverse(viewname, args=args)
    elif kwargs:
        return reverse(viewname, kwargs=kwargs)
    else:
        return reverse(viewname)


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': url,
        'get_messages': get_messages,
        'csrf_field': csrf_field,
    })
    return env