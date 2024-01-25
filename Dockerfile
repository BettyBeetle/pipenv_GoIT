# Użyj obrazu Pythona 3.8 jako obrazu bazowego
FROM python:3.11.7

# Skopiuj plik pyassist.py do katalogu /usr/src/ w kontenerze
COPY pyassist.py /usr/src/pyassist.py

# Zainstaluj niezbędne zależności (jeśli są potrzebne)
# Możesz dodać tutaj polecenia instalacji pakietów, które są wymagane przez twój skrypt Pythona.

# Ustaw katalog roboczy na /usr/src/
WORKDIR /usr/src

# Uruchom plik pyassist.py po uruchomieniu kontenera
CMD ["python", "pyassist.py"]
