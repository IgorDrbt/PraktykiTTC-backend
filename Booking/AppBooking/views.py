from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .models import Desk, Worker, Reservation
from datetime import date

class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
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

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": f"Użytkownik został zarejestrowany pomyślnie."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeskReservationView(APIView):
    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save()
            return Response({
                "message": f"Biurko {reservation.desk.number} zostało zarezerwowane."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
