from rest_framework import serializers, permissions
from .models import Product, ProductImage, Collection, ProductVariant
from rest_framework.permissions import IsAdminUser


class ProductImageSerializer(serializers.ModelSerializer):

    permission_classes = [IsAdminUser]

    class Meta:
        model = ProductImage
        fields = ['id', 'filename', 'alt_text', 'order', 'image_type']



class ProductVariantSerializer(serializers.ModelSerializer):

    permission_classes = [IsAdminUser]
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_title = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['product','product_title', 'color', 'size', 'stock']

    def get_product_title(self, obj):
        return obj.product.title if obj.product else None




class ProductSerializer(serializers.ModelSerializer):

    permission_classes = [IsAdminUser]
    images = ProductImageSerializer(many=True, read_only=True)
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        read_only_fields = ['slug']
        fields = ['id','title','collection','description_text','slug','categories','gender','price','review','variants','images',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['collection'] = instance.collection.title if instance.collection else None
        try:
            pv = int(float(data.get('price') or 0))
            data['price'] = f"{pv:,}"
        except Exception:
            pass
        return data


class CollectionSerializer(serializers.ModelSerializer):
    permission_classes = [IsAdminUser]
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'slug', 'description', 'release_date', 'products']
        read_only_fields = ['slug']
