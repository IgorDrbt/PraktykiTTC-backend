# Bookingapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer

class ProductList(APIView):
    def get(self, request, *args, **kwargs):
        # Mock data instead of database queries
        products = [
            {"name": "Product 1", "description": "Description for product 1", "price": 19.99},
            {"name": "Product 2", "description": "Description for product 2", "price": 29.99},
            {"name": "Product 3", "description": "Description for product 3", "price": 39.99}
        ]
        
        # Serialize mock data
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
