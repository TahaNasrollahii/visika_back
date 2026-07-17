from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('vendor/', include('vendor_api.urls')),
]

from django.urls import re_path
from django.views.static import serve
import os
from django.http import Http404

def custom_serve(request, path, document_root=None, show_indexes=False):
    # Try serving from the actual git repo first (for products/categories)
    repo_media = os.path.join(settings.BASE_DIR, 'media')
    if os.path.exists(os.path.join(repo_media, path)):
        return serve(request, path, document_root=repo_media, show_indexes=show_indexes)
    
    # Fallback to the configured MEDIA_ROOT (for Vercel's /tmp/media uploaded avatars)
    try:
        return serve(request, path, document_root=document_root, show_indexes=show_indexes)
    except Http404:
        raise Http404("Media not found in repo or tmp")

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', custom_serve, {'document_root': settings.MEDIA_ROOT}),
]
