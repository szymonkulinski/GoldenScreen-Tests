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
/Tests/GoldenTest.py -- Plik z kodem testów
/Tests/conftest.py -- Plik konfiguracyjny
```
Uruchomienie testów
```
pytest -q -s --name admin --password haslo
```
Przez specyfike aplikacji część testów wymaga praw administratora. Z kwestii bezpieczeństwa login oraz hasło administratora jest podawane w argumentach wywołania.

## Przykładowe Testy

- 1.7.3 Zmiana Adresu Email z błędnymi danymi ( różne adresy e-mail )

W teście tym logujemy się istniejące konto. Następnie przechodzimy do dashboardu użytkownika i zmieniamy email z błednymi danymi w postaci różniących się adresów email, oraz sprawdzamy czy wyświetlił się odpowiedni komunikat "Podane adresy muszą być takie same."

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
 
- 6.1.2 Dodanie nowego filmu istniejącego już w bazie danych

Test polega na sprawdzeniu poprawnego działania walidacji tego, czy dodawany film nie istnieje już w bazie danych. Dobrze działająca aplikacja powinień powiadomić administratora komunikatem o powieleniu filmu "Movie with this Title and ReleaseDate already exists."

Kroki
```
1.Klika "Zaloguj się" w menu
2. Wpisuje login administratora
3. Wpisuje hasło administratora
4. Klika przycisk "Zaloguj się"
5.Użytkownik przechodzi do panelu administracyjnego klikając odnościk "Panel Administracyjny" w menu
6.Przechodzi do bazy danych klikając hiperlink "Movies"
Dwukrotnie:
  7.Przechodzi podstrony dodawania filmu klikając odnośnik "Add Movie"
  8.Wprowadza Title
  9.Wprowadza Description
  10.Wprowadza ProductionCountry
  11.Wprowadza Director
  12.Wprowadza Screenwriter
  13.Wprowadza Cast
  14.Wprowadza Trailer
  15.Wybiera Images
  16.Wybiera Genre
  17.Wprowadza Slug
  18.Wprowadza ReleaseDate
  19.Wprowadza Length
  20.Wciska przycisk "SAVE"
21. Użytkownik wchodzi w szczegóły filmu klikając nazwe filmu
22. Użytkownik sprawdza czy wszystkie dane są zgodne z danymi w danych wejściowych
Kolejne kroki usuwają film i wylogowywyją z konta admina(Aby można było wykonywać test wielokrotnie)
18. Klika "Delete"
19. Klika "Yes, i'm sure"
20. Klika "Log Out"
```
Warunek Końcowy
```
Administrator dostaje komunikat o powieleniu się filmu "Movie with this Title and ReleaseDate already exists."
```
Kod
```python
  def test_613dodanieFilmuBezNazwy(self, name, password):
    self.driver.maximize_window()
    self.driver.get("http://127.0.0.1:8000/repertoire/")

    self.driver.find_element(By.ID, "LogIn").send_keys(Keys.ENTER)
    self.driver.find_element(By.ID, "id_username").send_keys("name")
    self.driver.find_element(By.ID, "id_password").send_keys("password")
    self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
    self.driver.find_element(By.ID, "AdminPanel").click()
    self.driver.find_element(By.LINK_TEXT, "Movies").click()
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
    self.driver.find_element(By.ID, "id_title").send_keys(" ")
    self.driver.find_element(By.ID, "id_description").send_keys("Wujek zostaje zmuszony do opieki nad nastoletnim bratankiem po śmierci jego ojca.")
    self.driver.find_element(By.ID, "id_productionCountry").send_keys("USA")
    self.driver.find_element(By.ID, "id_director").send_keys("Kenneth Lonergan")
    self.driver.find_element(By.ID, "id_screenwriter").send_keys("Kenneth Lonergan")
    self.driver.find_element(By.ID, "id_cast").send_keys("Casey Affleck, Lucas Hedges, Michelle Williams, Kyle Chandler")
    self.driver.find_element(By.ID, "id_trailer").clear()
    self.driver.find_element(By.ID, "id_trailer").send_keys("http://www.youtube.com/embed/gsVoD0pTge0")
    self.driver.find_element(By.CSS_SELECTOR, "#id_images > option:nth-child(10)").click()
    dropdown = self.driver.find_element(By.ID, "id_genre")
    dropdown.find_element(By.XPATH, "//option[. = 'Dramat']").click()
    self.driver.find_element(By.ID, "id_slug").clear()
    self.driver.find_element(By.ID, "id_slug").send_keys("manchasterbythesea")
    self.driver.find_element(By.ID, "id_releaseDate").clear()
    self.driver.find_element(By.ID, "id_releaseDate").send_keys("2016-01-23")
    self.driver.find_element(By.ID, "id_length").clear()
    self.driver.find_element(By.ID, "id_length").send_keys("137")
    self.driver.find_element(By.NAME, "_save").send_keys(Keys.ENTER)
    assert self.driver.find_element_by_class_name('errorlist').text == "To pole jest wymagane."
    self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(4)").click()
```
 
# Autorzy
Testy: Szymon Kulinski

Strona wykonana przy współpracy z: Michał Kornaus, Piotr Jeka
