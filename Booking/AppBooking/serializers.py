from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Desk, Worker, Reservation, Login

class DeskAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = '__all__'

class WorkerAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

class ReservationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class LoginAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['login', 'passwd']

class UserRegistrationSerializer(serializers.ModelSerializer):
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
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class ReservationSerializer(serializers.ModelSerializer):
    desk_number = serializers.IntegerField()  # Numer biurka
    id_worker = serializers.PrimaryKeyRelatedField(queryset=Worker.objects.all())  # ForeignKey zamiast IntegerField
    reservation_time = serializers.DateTimeField()  # Czas rezerwacji

    class Meta:
        model = Reservation
        fields = ['desk_number', 'id_worker', 'reservation_time']

    def create(self, validated_data):
        """
        Tworzenie rezerwacji biurka.
        """
        desk_number = validated_data['desk_number']
        id_worker = validated_data['id_worker']
        reservation_time = validated_data['reservation_time']

        try:
            desk = Desk.objects.get(number=desk_number)
            if not desk.is_available:
                raise serializers.ValidationError(f"Biurko {desk_number} jest już zarezerwowane.")

            existing_reservation = Reservation.objects.filter(id_worker=id_worker, reservation_time=reservation_time)
            if existing_reservation.exists():
                raise serializers.ValidationError(f"Pracownik {id_worker.name_worker} {id_worker.surname_worker} ma już rezerwację na ten czas.")

            reservation = Reservation.objects.create(
                reservation_time=reservation_time,
                desk=desk,
                id_worker=id_worker  
            )

            desk.is_available = False
            desk.save()

            return reservation

        except Desk.DoesNotExist:
            raise serializers.ValidationError("Biurko o podanym numerze nie istnieje.")
        except Worker.DoesNotExist:
            raise serializers.ValidationError("Pracownik o podanym ID nie istnieje.")
        except serializers.ValidationError as e:
            raise serializers.ValidationError(str(e))


class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ['number', 'is_available']  
