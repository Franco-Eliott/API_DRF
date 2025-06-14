# from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from shop.models import Category, Product, Article
from shop.serializers import CategoryListSerializer, CategoryDetailSerializer, ProductDetailSerializer, ProductListSerializer, ArticleSerializer

from rest_framework.permissions import IsAuthenticated

from shop.permissions import IsAdminAuthenticated, IsAdminStaff

class MultipleSerializerMixin:

    detail_serailizer_class = None

    def get_serailizer_class(self):
        if self.action == 'retrieve' and self.detail_serailizer_class is not None:
            return self.detail_serailizer_class
        return super().get_serializer_class()

class CategoryViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        product = self.get_object()
        articles = product.products.all()
        for article in articles:
            article.disable()
        product.disable()
        return Response()
    
class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serailizer_class = CategoryDetailSerializer

    permission_classes = [IsAdminAuthenticated, IsAdminStaff]

    def get_queryset(self):
        return Category.objects.all()

class ProductViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):
        
        queryset = Product.objects.filter(active=True)

        category_id = self.request.GET.get('category_id')

        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
    
    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()
    
class ArticleViewset(ReadOnlyModelViewSet):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        
        queryset = Article.objects.filter(active=True)

        product_id = self.request.GET.get('product_id')

        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        
        return queryset


class AdminArticleViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all()