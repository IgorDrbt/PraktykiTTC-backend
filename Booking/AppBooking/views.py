from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, ReservationSerializer, DeskSerializer, DeskAdminSerializer, WorkerAdminSerializer, ReservationAdminSerializer, LoginAdminSerializer
from django.http import JsonResponse
from rest_framework import status, viewsets, generics
from datetime import date
from .models import Desk, Worker, Reservation
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class LoginView(generics.GenericAPIView):
    permission_classes = []  
    serializer_class = LoginAdminSerializer  

    def post(self, request, *args, **kwargs):
        login = request.data.get('login')
        password = request.data.get('passwd')

        if not login or not password:
            return Response({"error": "Login and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Attempting login with: {login}, {password}")

        try:
            user = User.objects.get(username=login)
            print(f"Found user: {user}")

            if not check_password(password, user.password):
                print("Invalid password")
                return Response({"error": "Invalid credentials - incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            return Response({"error": "Invalid credentials - no such user"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generowanie tokenu JWT
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
        }, status=status.HTTP_200_OK)



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

class UserRegistrationView(APIView):
    def post(self, request):
        """
        Rejestracja nowego użytkownika za pomocą API.
        """
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = User.objects.create_user(username=username, password=password)

            return Response(
                {"message": f"Użytkownik {user.username} został zarejestrowany pomyślnie."},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeskAdminViewSet(viewsets.ModelViewSet):
    """
    Admin view for managing desks (CRUD operations).
    """
    queryset = Desk.objects.all()
    serializer_class = DeskAdminSerializer
    permission_classes = [IsAdminUser]

class WorkerAdminViewSet(viewsets.ModelViewSet):
    """
    Admin view for managing workers (CRUD operations).
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerAdminSerializer
    permission_classes = [IsAdminUser]

class ReservationAdminViewSet(viewsets.ModelViewSet):
    """
    Admin view for managing reservations (CRUD operations).
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationAdminSerializer
    permission_classes = [IsAdminUser]

class ListaKlientow(APIView):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
            available_desks = Desk.objects.filter(is_available=True)
            
            serializer = DeskSerializer(available_desks, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Wystąpił błąd podczas pobierania biurek.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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