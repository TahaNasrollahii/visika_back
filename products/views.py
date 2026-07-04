from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()
        # Optional filters
        is_best_seller = self.request.query_params.get('is_best_seller')
        is_hot_offer = self.request.query_params.get('is_hot_offer')
        category_slug = self.request.query_params.get('category_slug')

        if is_best_seller == 'true':
            queryset = queryset.filter(is_best_seller=True)
        if is_hot_offer == 'true':
            queryset = queryset.filter(is_hot_offer=True)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
