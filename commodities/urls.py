from django.urls import include, path


from commodities.views import hs


urlpatterns = [

    path('hs/<str:code>', hs.GetHsItemView.as_view())

]