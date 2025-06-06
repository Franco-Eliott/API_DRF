from rest_framework import serializers

from shop.models import Category, Product, Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']

    # def validate(self, data):
    #     if data['price'] < 1:
    #         raise serializers.ValidationError('Price must be greater than 1 €')
    #     return data
    
    def validate_price(self, value):
        if value < 1:
            raise serializers.ValidationError('Price must be greater than 1 €')
        return value
          
    def validate_product(self, value):
        if value.active is False:
            raise serializers.ValidationError('The product is not active')
        return value
    

class ProductDetailSerializer(serializers.ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'date_created', 'date_updated', 'category', 'articles']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'date_created', 'date_updated', 'category']


class CategoryDetailSerializer(serializers.ModelSerializer):

    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated', 'products']

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductListSerializer(queryset, many=True)
        return serializer.data


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'date_created', 'date_updated']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            # print('Category already exist')
            raise serializers.ValidationError('Category already exist')
        return value
    
    def validate(self, data):
        if data['name'] not in data['description']:
            raise serializers.ValidationError('Name must be in description')
        return data
