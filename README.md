# 23Z-PIS-Process-Mining

# Opis Projektu
Narzędzie do analiz Process Mining

\-  https://en.wikipedia.org/wiki/Process\_mining

\- https://www.processmining.org/process-discovery.html

\- źródła danych: https://www.tf-pm.org/resources/logs

Wymagania:

\- Moduł ładowania danych w trybie batch z bazy relacyjnej lub NoSQL jeśli dane znajdują się w formacie Event Log. 

\- Moduł ładowania danych w trybie online poprzez podłączenie danych w formie online poprzez kolejkę komunikatów np. Kafka

\- Moduł analiz razem z UI 

\- baza relacyjna dla warstwy logiki biznesowej oddzielona od danych procesów

\- UI wykonany w dowolnej współczesnej technologii (np. ReactJS) - podstawowe funkcjonalności to wyświetlanie grafu directly-follows graph oraz proste statystyki dotyczące procesu np. liczba wniosków / liczba wariantów





# Środowisko
- Repozytorium GitHub

<https://github.com/Pecet13/23Z-PIS-Process-Mining.git>

- Skrypty budujące projekt 

Plik requirements.txt w repozytorium

- Serwer CI

Jenkins

- IDE :

Pycharm – python

Datagrip – Baza danych

- Narzędzie do zarządzania zadaniami

Jira - 23Z-PIS-Process-Mining

- Mierzenie pokrycia kodu

Coverage.Py

- Zasoby w sieci:
1. Baza danych do logów – event\_log\_db
1. Baza danych aplikacji – PIS2023Z\_db
1. Maszyna wirtualna mainpis (Ubuntu 20.)


