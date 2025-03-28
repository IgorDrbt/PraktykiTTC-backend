from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, ReservationSerializer
from .models import Desk, Worker, Reservation

class ListaKlientow(APIView):
    authentication_classes = [JWTAuthentication]
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        Available_desks = Desk.objects.filter(is_available=True)
        serializer = DeskSerializer(Available_desks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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

class DeskReservationView(APIView):
    authentication_classes = [JWTAuthentication]
    permissions_classes = [IsAuthenticated]

    def post(self, request):
        """
        Tworzenie rezerwacji biurka przez użytkownika.
        """
        serializer = ReservationSerializer(data=request.data)

        if serializer.is_valid():
            reservation = serializer.save()  # Tworzymy rezerwację, używając serializer'a
            return Response({
                "message": f"Biurko {reservation.desk.number} zostało pomyślnie zarezerwowane przez {reservation.worker.name_worker} {reservation.worker.surname_worker}."
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

