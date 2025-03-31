from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from .models import Desk, Worker
class ListaKlientow(APIView):
    def get(self, request):
        Available_desks = Desk.objects.filter(is_available=True)
        return Response( status=status.HTTP_200_OK)
    
class UserRegistrationView(APIView):
    def post(self, request):
        """
        Rejestracja nowego użytkownika za pomocą API.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Zapisuje nowego użytkownika
            return Response(
                {"message": f"Użytkownik {user.username} został zarejestrowany pomyślnie."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
