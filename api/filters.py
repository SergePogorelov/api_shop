from django_filters import rest_framework as filters

from shop.models import Product


class ProductFilter(filters.FilterSet):
    price_from = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_to = filters.NumberFilter(field_name="price", lookup_expr="lte")
    categories = filters.CharFilter(field_name="categories__name")

    class Meta:
        model = Product
        fields = ["name", "categories", "published", "price_from", "price_to"]
