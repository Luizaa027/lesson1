from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache 
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView 

from apps.product.models import Product
from apps.product.serializers import ProductSerializer, ProductDetailSerializer, ProductCreateSerializer

class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer 

class ProductListAPIView(APIView):
    def get(self, request):
        cache_key = "product_list"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        product = (
            Product.objects
            .select_related('category', 'model')
            .prefetch_related('images')
            .order_by('-created_at')
        ) 
        serializer = ProductSerializer(product, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 2) 
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProdectDetailAPIView(APIView):
     
     def get_object(self, uuid):
         return get_object_or_404(
             Product.objects
             .select_related('category', 'model')
             .prefetch_related('images'),
             uuid=uuid
         )

         
     def get(self, request, uuid):
         serializer = ProductDetailSerializer(self.get_object(uuid))
         return Response(serializer.data)
     

     def put(self, request, uuid):
         product = self.get_object(uuid)
         serializer = ProductDetailSerializer(product, data=request.data)
        
         if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        
         return Response(serializer.errors, status=400)
     
     def patch(self,request, uutd):
         product = self.get_object(uutd)
         serializer = ProductDetailSerializer(product, data=request.data, partial=True)
         
         if serializer.is_valid():
                serializer.save()
                cache.dedlete("product_list")
                return Response(serializer.data)
        
         return Response(serializer.errors, status=400) 
     
     def delete(self, request, uuid):
        self.get_object(uuid).delete()
        cache.delete("product_list")
        return Response(status=204) 
     
class ProductListAPIViewV2(APIView):
    def get(self, request):
        queryset = Product.objects.all()  

    category = request.query_params.get('category')
    model = request.query_params.get('model')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    if category:
        queryset = queryset.filter(category_id=category) 

    if model:
        queryset = queryset.filter(model_id=model)

    if min_price:
        queryset = queryset.filter(price__gte=min_price)

    if max_price:
        queryset = queryset.filter(price__lte=max_price) 

    search = request.query_params.get('search')
    if search:
        queryset = queryset.filter(title__icontains=search)

        ordering = request.query_params.get('ordering')
    if ordering:
        queryset = queryset.order_by(ordering) 

    serializer = ProductSerializer(queryset, many=True)      





