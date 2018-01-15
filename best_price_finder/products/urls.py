from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from products import views

urlpatterns = (
    url(r'^product/$', views.ProductList.as_view()),
    url(r'^pricing_block/$', views.PricingBlockList.as_view()),
    url(r'^best_price/$', views.BestPrice.as_view(), name='something')
)
urlpatterns = format_suffix_patterns(urlpatterns)
