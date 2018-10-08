from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.signup, name='signup'),
    url(r'^index/$', views.index, name='index'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^comment/(?P<post_id>\d+)', views.add_comment, name='comment'),
    url(r'^new/image$', views.new_image, name='new-image'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
