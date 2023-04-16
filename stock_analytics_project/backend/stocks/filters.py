from django_filters import rest_framework as filters
from .models import StockPrice


class StockPriceFilter(filters.FilterSet):
    date = filters.DateFilter(field_name='date')
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = StockPrice
        fields = ['date']