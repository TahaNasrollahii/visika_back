from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        
        is_best_seller = self.request.query_params.get('is_best_seller')
        is_hot_offer = self.request.query_params.get('is_hot_offer')
        category_slug = self.request.query_params.get('category_slug')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        has_discount = self.request.query_params.get('has_discount')
        brands = self.request.query_params.get('brands')
        ordering = self.request.query_params.get('ordering')

        if is_best_seller == 'true':
            queryset = queryset.filter(is_best_seller=True)
        if is_hot_offer == 'true':
            queryset = queryset.filter(is_hot_offer=True)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        if min_price and min_price.isdigit():
            queryset = queryset.filter(price__gte=int(min_price))
        if max_price and max_price.isdigit():
            queryset = queryset.filter(price__lte=int(max_price))
        if has_discount == 'true':
            queryset = queryset.filter(discount_price__isnull=False)
            
        if brands:
            brand_list = brands.split(',')
            queryset = queryset.filter(brand__in=brand_list)
            
        if ordering:
            if ordering in ['price', '-price', '-created_at', 'created_at', '-reviews_count', 'reviews_count']:
                queryset = queryset.order_by(ordering)
            
        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class BrandListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        category_slug = request.query_params.get('category_slug')
        queryset = Product.objects.exclude(brand='').exclude(brand__isnull=True)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        brands = queryset.values_list('brand', flat=True).distinct()
        return Response(list(brands))
