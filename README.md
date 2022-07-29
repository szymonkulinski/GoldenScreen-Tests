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

Pełną rozpiskę testów można znaleźć pod adresem, gdzie testy automatycznę są zaznaczone kolorem zielonym:

https://docs.google.com/spreadsheets/d/1ckYsxgPMeJAIBvLEDr3dVJLd7-Nx4E6c-aCjLeyztg8/edit?usp=sharing

Lokalizacja Plików
```
/Tests
```
Uruchomienie testów
```
pytest -q -s --name admin --password haslo
```
Przez specyfike aplikacji część testów wymaga praw administratora. Z kwestii bezpieczeństwa login oraz hasło administratora jest podawane w argumentach wywołania.

## Przykładowe Testy

- 1.7.3 Zmiana Adresu Email z błędnymi danymi ( różne adresy e-mail )

Kroki
```
1.Niezalogowany użytkownik przechodzi na strone https://goldenscreen.pythonanywhere.com 
2.Użytkownik wybiera z menu opcję "ZALOGUJ SIĘ"
3.Uzupełnia pole "Nazwa użytkownika / Adres e-mail"
4.Uzupełnia pole "Hasło"
5.Wciska przycisk "Zaloguj się"
6. Wybiera placówke kina
7.Użytkownik przechodzi do dashboardu klikając odnośnik "*nazwa użytkownika*" w menu
8.Użytkownik klika w hiperlink "Zmień swój adres email"
9.Użytkownik wpisuje nowy adres email
10.Użytkownik wpisuje drugi adres email
11.Użytkownik wprowadza hasło
12.Użytkownik klika "Zmień Email"
13.Użytkownik klika "Potwierdź"
Kolejne kroki wylogowywują z konta(Aby można było wykonywać test wielokrotnie)
14.Wciska przycisk "Wyloguj się"
```
Warunek Końcowy
```
Po kroku 12 Wyświetla się komunikat: "Podane adresy muszą być takie same."
```
Kod
```python
  def test_173ZmianaAdresuEmailzbdnymidanymirneadresyemail(self):
    self.driver.maximize_window()
    self.driver.get("http://127.0.0.1:8000/repertoire/")
    
    self.driver.find_element(By.ID, "LogIn").send_keys(Keys.ENTER)
    self.driver.find_element(By.ID, "id_username").send_keys("JanKowalski")
    self.driver.find_element(By.ID, "id_password").click()
    self.driver.find_element(By.ID, "id_password").send_keys("Qwerty123")
    self.driver.find_element(By.CSS_SELECTOR, ".bg-secondary").click()
    self.driver.find_element(By.ID, "UserCard").click()
    self.driver.find_element(By.LINK_TEXT, "Zmień swój adres email").click() 
    self.driver.find_element(By.ID, "id_email1").click()
    self.driver.find_element(By.ID, "id_email1").send_keys("jankowalski3@wp.pl")
    self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(2)").click()
    self.driver.find_element(By.ID, "id_email2").click()
    self.driver.find_element(By.ID, "id_email2").send_keys("jan3@wp.pl")
    self.driver.find_element(By.ID, "id_password").click()
    self.driver.find_element(By.ID, "id_password").send_keys("Qwerty123")
    self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(4)").click()
    self.driver.find_element(By.ID, "myBtn").click()
    self.driver.find_element(By.CSS_SELECTOR, ".btn-accept").click()
    self.driver.find_element(By.CSS_SELECTOR, ".errorlist > li").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".errorlist > li").text == "Podane adresy muszą być takie same."
    self.driver.find_element(By.ID, "LogOut").send_keys(Keys.ENTER)
 ```

# Autorzy
Testy: Szymon Kulinski

Strona wykonana przy współpracy z: Michał Kornaus, Piotr Jeka
