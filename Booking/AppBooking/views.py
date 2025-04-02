from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, ReservationSerializer
from .models import Desk, Reservation
from django.http import JsonResponse
from rest_framework import status, serializers
from datetime import date
from django.contrib.auth.models import User

class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

def desk_availability_api(request):
    selected_date = request.GET.get('date')
    if selected_date:
        try:
            selected_date = date.fromisoformat(selected_date)
        except ValueError:
            return JsonResponse({'error': 'Zły format daty. Użyj RRRR-MM-DD'}, status=400)
    else:
        selected_date = date.today()

    desks = Desk.objects.all()
    reserved_desks = Reservation.objects.filter(
        reservation_time=selected_date
    ).values_list('desk_id', flat=True)

    result = []
    for desk in desks:
        result.append({
            'desk_number': desk.number,
            'reserved': desk.id in reserved_desks
        })

    return JsonResponse({
        'date': selected_date.isoformat(),
        'desks': result
    })


class ListaKlientow(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            Available_desks = Desk.objects.filter(is_available=True)
            serializer = DeskSerializer(Available_desks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Wystąpił błąd podczas pobierania biurek.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Tworzenie rezerwacji biurka przez użytkownika.
        """
        try:
            serializer = ReservationSerializer(data=request.data)

            if serializer.is_valid():
                reservation = serializer.save()  
                return Response({
                    "message": f"Biurko {reservation.desk.number} zostało pomyślnie zarezerwowane przez {reservation.worker.name_worker} {reservation.worker.surname_worker}."
                }, status=status.HTTP_201_CREATED)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
            {"error": "Wystąpił błąd podczas tworzenia rezerwacji.", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        












