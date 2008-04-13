# context processors meant to be used with RequestContext
# Read more: http://www.djangoproject.com/documentation/templates_python/#subclassing-context-requestcontext

def settings(request):
    "Insert settings module into the context automatically."
    from django.conf import settings
    return {
        'settings':settings,
    }