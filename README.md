====== Instalacja virtual  ========

1 klonuj do jakiegos folderu

-----2 git chechout SCRUM, twoj scrum zadania-------

3 ctrl+` by wejsc do konsoli

4 instalujesz wirtualke (konsola): python -m venv .venv

5 aktywacja środowiska (konsola): .venv\Scripts\activate

alternatywnie: .venv\Scripts\Activate.ps1

6 instalacja pakietów dla python (konsola): python -m pip install django djangorestframework djangorestframework-simplejwt django-cors-headers

7 (opcjonalne) jesli chce pip sie aktualizowac z np(24.0.0 do 25.0.1): python.exe -m pip install --upgrade pip

====== wlaczac uzywajac ====== 

8 cd Booking

9 python manage.py migrate 

10 python manage.py runserver

====== Zmiana w repozytorium ========

1 git add Booking

2 git commit -m "Wiadomość dla nas"

3 git push origin SCRUM jakis

======== Rejestracja w Postmanie =========
http://127.0.0.1:8000/api/register/

Dodajesz uzytkownika 

{

  "username": "?",

  "email": "?@gmail.com",

  "password": "?",

  "password_confirm": "?"

}

takze mozesz wykorzystac go odrazu do logowania w api/login

======= Logowanie w Postmanie ========

Url: http://127.0.0.1:8000/api/login/

Po lewej zamiast GET dajesz POST 

Po tym klikasz Body 

W wyborze zamiast none dajesz raw i po prawej zamiast text dajesz JSON

Po tym ctrl-c ctrl-v

{

    "login": "?",

    "passwd": "?"

}

i SEND

Wynik: 

{

    "refresh": "---------------------------------------------------------------",

    "access": "---------------------------------------------------------------"

}

tak
========= Rejestracja biurka w postamnie =======

http://127.0.0.1:8000/admin/AppBooking/

W admin panelu musi byc stowrzonny login = logowanie odbywa sie poprzez rejestracje i logowanie tak jak na gorze, po tym gdy pojawi sie "login object(x)" uzywamy go do rejestracji workera, potrzebny jest login object jako id_login i imie i nazwisko, po tym mozemy rezerwowac biurko.

http://127.0.0.1:8000/api/reserve/

Do rejestracji - by stworzyc rezerwacje w postmanie potrzeba dwoch reczy, w tabeli Authorization wybieramy Bearer Token, i wklejamy na nasz access token z logina, i Body - raw - JSON

{

    "desk_number": "4",

    "id_worker": "2",

    "reservation_time": "2025-04-05"

}

desk_number - numer biurka, w bazie danych jest on w AppBooking_desk = number

id_worker - jest pokazany w adminie jako worker,
object(x), w bazie w tabeli AppBooking_worker jako id_worker

reservation_time - data dzisiejsza idac jako RRRR-MM-DD

============ ListaKlientow aka lista biurek =============

http://127.0.0.1:8000/api/ListaKlientow/

tak samo jak rezerwacja tak i z lista biurek authorizacja i token, ale tym razem dajemy Body - none

wynik: 

[
    {
        "number": 1,
        "is_available": true
    },
    {
        "number": 4,
        "is_available": true
    }
]

pokazuje dostepne biurka

============ desk-availability ==========

http://127.0.0.1:8000/api/desk-availability/

czarne tlo i dane 
