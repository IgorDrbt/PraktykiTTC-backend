from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Desk
from .serializers import DeskSerializer

class ListaKlientow(APIView):
    def get(self, request):
        Available_desks = Desk.objects.filter(is_available=True)
        serializer = DeskSerializer(Available_desks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

