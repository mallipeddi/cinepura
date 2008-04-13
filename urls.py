from django.conf.urls.defaults import *
import os
from django.conf import settings

urlpatterns = patterns('',
    # STRICTLY USE ONLY in dev environment
    (r'^static_media/(?P<path>.*)$', 'django.views.static.serve', 
                                    {'document_root': os.path.join(settings.APP_DIR, 'static_media/')}),
    (r'^', include('cinepura.iphone.urls')),
)
