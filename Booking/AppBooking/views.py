from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

class ListaKlientow(APIView):
    def get(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)

