from django.contrib import admin
from django.urls import path, include
from messaging.views import home_view
from django.conf import settings
from django.conf.urls.static import static


# from django.views.generic import TemplateView

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('', home_view, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('messaging/', include('messaging.urls')),
    path('wallet/', include('wallet.urls')),
    
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
