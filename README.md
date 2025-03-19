====== Instalacja virtual  ========

1 klonuj do jakiegos folderu

2 ctrl+` by wejsc do konsoli

3 instalujesz wirtualke (konsola): python -m venv .venv

4 aktywacja środowiska (konsola): .venv\Scripts\activate

alternatywnie: .venv\Scripts\Activate.ps1

5 instalacja pakietów dla python (konsola): python -m pip install django djangorestframework

6 (opcjonalne) jesli chce pip sie aktualizowac z np(24.0.0 do 25.0.1): python.exe -m pip install --upgrade pip

====== wlaczac uzywajac ====== 

7 cd Booking

8 python manage.py migrate 

9 python manage.py runserver

====== Zmiana w repozytorium ========

1 git add Booking

2 git commit -m "Wiadomość dla nas"

3 git push origin main

