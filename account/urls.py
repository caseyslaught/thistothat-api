from django.urls import include, path

from account.views import register


urlpatterns = [

    path('request_api_key/', register.RequestApiKeyView.as_view())

]