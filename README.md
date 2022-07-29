# GoldenScreen

## Opis projektu
GoldenScreen to aplikacja internetowa służąca do rezerwacji biletów kinowych, z dodatkową opcją oceniania filmów dostępnych w bibliotece kina.

# Testy
Kazdy z testów napisany został pod historyjkę, oraz posiada parametry takie jak ID,	Wersja, Nazwa, Dane wejściowe, Warunki Wstępne, Kroki, Oczekiwany Rezultat,	Warunek Końcowy.

- Format ID:

X.Y.Z

X - ID Modułu

Y - ID Historyjki

Z - ID Testy

Przykładowo, 1.2.5 oznacza, że test jest to test o ID 5 dla historyjki o ID 2 z modułu o ID 1.

Pełną rozpiskę testów można znaleźć pod adresem:

https://docs.google.com/spreadsheets/d/1ckYsxgPMeJAIBvLEDr3dVJLd7-Nx4E6c-aCjLeyztg8/edit?usp=sharing

Lokalizacja Plików
```
/Tests
```
Uruchomienie testów
```
pytest -q -s --name admin --password haslo
```
Przez specyfike aplikacji większość testów wymaga praw administratora. Z kwestii bezpieczeństwa login oraz hasło administratora jest podawane w argumentach wywołania.



# Autorzy
Testy: Szymon Kulinski

Strona wykonana przy współpracy z: Michał Kornaus, Piotr Jeka
