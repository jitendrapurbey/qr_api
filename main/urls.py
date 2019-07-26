from django.conf.urls import url
from . import views
from api.views import CreateQRView

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^generate-qr$', views.generate_qr, name='generate_qr'),

]