from rest_framework import mixins, viewsets
from rest_framework.serializers import ValidationError

from shop.models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_destroy(self, instance):
        if instance.products.all().count():
            raise ValidationError({"error": "Категория прикреплена к товару"})
        instance.delete()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(deleted=False)

    def perform_create(self, serializer):
        published = self.request.data.get("published", True)

        try:
            categories = Category.objects.filter(
                id__in=self.request.data.getlist("categories")
            )
        except ValueError:
            raise ValidationError(
                {"categories": "id категории должно быть числом."}
            )

        if categories.count() < 2 or categories.count() > 10:
            raise ValidationError(
                {
                    "categories": "У каждого товара должно быть от 2х до 10 категорий."
                }
            )

        serializer.save(categories=categories, published=published)

    def perform_update(self, serializer):
        self.perform_create(serializer)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
