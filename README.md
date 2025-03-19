====== Instalacja virtual  ========

(pobierać tylko w folderze: cd \PraktykiTTC-backend)

konsola: python -m venv .venv

aktywacja środowiska (konsola): .venv\Scripts\activate

instalacja pakietów dla python (konsola): python -m pip install django djangorestframework

python.exe -m pip install --upgrade pip

====== Zmiana w repozytorium ========

git add Booking

git commit -m "Wiadomość dla nas"

git push origin main

====== wlaczac uzywajac ====== 

cd Booking

python manage.py migrate 

python manage.py runserver
