from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
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
from django.db.models import Q
from django.core.paginator import Paginator


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

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
        }, status=status.HTTP_200_OK)



def desk_availability_api(request):
    selected_date = request.GET.get('date')
    is_available = request.GET.get('available')
    page = request.GET.get('page', 1)

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

    if is_available is not None:
        if is_available.lower() == 'true':
            desks = desks.exclude(number__in=reserved_desks)
        elif is_available.lower() == 'false':
            desks = desks.filter(number__in=reserved_desks)

    result = []
    for desk in desks:
        result.append({
            'desk_number': desk.number,
            'reserved': desk.number in reserved_desks
        })

    paginator = Paginator(result, 5)
    page_obj = paginator.get_page(page)

    return JsonResponse({
        'date': selected_date.isoformat(),
        'desks': list(page_obj),
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number
    })

class UserRegistrationView(APIView):
    def post(self, request):
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
    queryset = Desk.objects.all()
    serializer_class = DeskAdminSerializer
    permission_classes = [IsAdminUser]

class WorkerAdminViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerAdminSerializer
    permission_classes = [IsAdminUser]

class ReservationAdminViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationAdminSerializer
    permission_classes = [IsAdminUser]

class ListaBiurek(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
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
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = ReservationSerializer(data=request.data)

            if serializer.is_valid():
                reservation = serializer.save()  
                
                user = reservation.id_user
                message = f"Biurko {reservation.desk.number} zostało pomyślnie zarezerwowane przez {user.username}."

                return Response({"message": message}, status=status.HTTP_201_CREATED)
       
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Wystąpił błąd podczas tworzenia rezerwacji.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
       
class ReservationDateFilterAPIView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reservations = Reservation.objects.all()

        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date:
            reservations = reservations.filter(reservation_time__gte=start_date)
        if end_date:
            reservations = reservations.filter(reservation_time__lte=end_date)

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


