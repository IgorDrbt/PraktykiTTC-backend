from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Reservation, Desk, Worker

class  UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        """
        Validate that passwords match.
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Hasła muszą być takie same")
        return data

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
        except Exception as e:
            raise serializers.ValidationError(f"Error creating user: {str(e)}")
        return user

class ReservationSerializer(serializers.ModelSerializer):
    desk_number = serializers.IntegerField()  # Numer biurka
    worker_id = serializers.IntegerField()  # ID pracownika
    reservation_time = serializers.DateTimeField()  # Czas rezerwacji

    class Meta:
        model = Reservation
        fields = ['desk_number', 'worker_id', 'reservation_time']

    def create(self, validated_data):
        """
        Tworzenie rezerwacji biurka.
        """
        desk_number = validated_data['desk_number']
        worker_id = validated_data['worker_id']
        reservation_time = validated_data['reservation_time']

        # Sprawdzenie, czy biurko istnieje i jest dostępne
        try:
            desk = Desk.objects.get(number=desk_number)
            if not desk.is_available:
                raise serializers.ValidationError(f"Biurko {desk_number} jest już zarezerwowane.")

            worker = Worker.objects.get(id_worker=worker_id)

            # Sprawdzanie, czy pracownik nie ma już rezerwacji na ten czas
            existing_reservation = Reservation.objects.filter(worker=worker, reservation_time=reservation_time)
            if existing_reservation.exists():
                raise serializers.ValidationError(f"Pracownik {worker.name_worker} {worker.surname_worker} ma już rezerwację na ten czas.")

            # Tworzenie rezerwacji
            reservation = Reservation.objects.create(
                reservation_time=reservation_time,
                desk=desk,
                worker=worker
            )

            # Zaktualizowanie dostępności biurka
            desk.is_available = False
            desk.save()

            return reservation

        except Desk.DoesNotExist:
            raise serializers.ValidationError("Biurko o podanym numerze nie istnieje.")
        except Worker.DoesNotExist:
            raise serializers.ValidationError("Pracownik o podanym ID nie istnieje.")