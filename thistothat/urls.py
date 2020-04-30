
from django.contrib import admin
from django.urls import path, include, re_path


urlpatterns = [

   path('commodities/', include('commodities.urls')),
   path('cybersyn1984/', admin.site.urls),

]

