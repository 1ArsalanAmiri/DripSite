import django_filters
from .models import Product
from django_filters import rest_framework as filters



class ProductFilter(django_filters.FilterSet):
    size = django_filters.CharFilter(field_name="sizes__value", lookup_expr="iexact")
    color = django_filters.CharFilter(field_name="colors__name", lookup_expr="iexact")
    category = django_filters.CharFilter(field_name="categories__name", lookup_expr="iexact")
    gender = django_filters.CharFilter(field_name="genders", lookup_expr="iexact")

    #Price filter
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte" , min_value=0)
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte" , max_value=1000)

    ordering = filters.OrderingFilter(
        fields=(
            ('price', 'price'),   # price ascending
            ('-price', 'price_desc'),  # price descending
            ('title', 'title'),
        )
    )

    def filter_sizes(self, queryset, name, value):
        values = self.request.GET.getlist('size')
        return queryset.filter(sizes__value__in=values).distinct()

    def filter_colors(self, queryset, name, value):
        values = self.request.GET.getlist('color')
        return queryset.filter(colors__name__in=values).distinct()


    class Meta:
        model = Product
        fields = ["size", "color", "category", "gender", "price"]