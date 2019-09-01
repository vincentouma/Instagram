from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.insta, name='insta'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^user/(?P<username>\w+)', views.profile, name='profile'),
    url(r'^comment/(?P<image_id>\d+)', views.add_comment, name='comment'),
    url(r'^upload/$', views.upload_image, name='upload_image'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^search/', views.search, name='search'),
    url(r'^edit/',views.edit_profile, name='edit_profile'),

 ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)