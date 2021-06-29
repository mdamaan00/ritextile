import django_filters
from django_filters import DateFilter,NumberFilter
from .models import *

class ItemFilter(django_filters.FilterSet):
    PriceFrom = NumberFilter(field_name = "price",lookup_expr='gte')
    PriceTo = NumberFilter(field_name = "price",lookup_expr='lte')
    class Meta:
        model = Product
        fields = ['category','material','dyeable']


        