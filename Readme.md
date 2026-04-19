# Proiect Testarea Sistemelor Software - Sistem Cinema

## Descriere Proiect
Acest proiect implementeaza un sistem de gestiune pentru rezervari cinema, cu logica de calcul a pretului biletului in functie de varsta, statut student, zi, rand si puncte de loialitate. Proiectul acopera toate cele 3 etape de implementare si testare: functionala, structurala si mutation testing.

## Configuratie Sistem
- Sistem de Operare: Windows 11
- Limbaj de Programare: Python 3.14.2
- Biblioteci folosite:
    - colorama 0.4.6
    - coverage 7.13.5
    - iniconfig 2.3.0
    - packaging 26.0
    - pip 25.3
    - pluggy 1.6.0
    - Pygments 2.20.0
    - pytest 9.0.3

## Analiza Datelor de Intrare (Black-Box)

### Parametri de intrare (Inputs):
- age: intreg pozitiv
- is_student: bool
- day: intreg intre 1-7
- row: intreg intre 0-9
- loyalty points: intreg

### Clase de echivalenta:
- day: zilele saptamanii
    - D_1 = {1,2,3,4,5} (zile din cursul saptamanii)
    - D_2 = {6,7} (weekend)
    - D_3 = {d|d < 1} (invalid)
    - D_4 = {d|d > 7} (invalid)
- row: tipul locului
    - R_1 = {0,1,2,3,7,8,9} (standard)
    - R_2 = {4,5,6} (VIP)
    - R_3 = {r|r < 0} (invalid)
    - R_4 = {r|r > 9} (invalid)
- age: varsta
    - A_1 = {0,...,64}
    - A_2 = {65,...} (pensionar)
    - A_3 = {a|a < 0} (invalid)
- loyalty: puncte fidelitate
    - L_1 = {0,...,50} (fara reducere)
    - L_2 = {51,...} (reducere)
    - L_3 = {l|l < 0} (invalid)
- is_student:
    - S_1 = {True}
    - S_2 = {False}

### Analiza valorilor de frontiera (BVA):
- day: {0, 1, 5, 6, 7, 8}
- row: {-1, 0, 3, 4, 6, 7, 9, 10}
- age: {-1, 0, 64, 65}
- loyalty: {-1, 0, 50, 51}

## Testare Structurala (White-Box)

### Control Flow Graph (CFG)
Nodurile grafului corespund liniilor de cod din functia calculate_price.

[LOC PENTRU IMAGINE: CFG CU CODUL]
[LOC PENTRU IMAGINE: CFG CU ARBORELE / DIAGRAMA]

Strategii implementate:
- Statement Coverage: Toate instructiunile executate.
- Decision Coverage: Toate ramurile decizionale (True/False) acoperite.
- Condition Coverage: Testarea conditiilor atomice din expresiile compuse.
- Circuite Independente: Identificarea si testarea cailor de baza conform McCabe.

## Mutation Testing
Am introdus mutanti neechivalenti (modificari de operatori relationali) pentru a verifica robustetea suitei de teste.
- Au fost eliminati (omorati) mutanti la pragurile de varsta (65) si loialitate (50).

## Rularea Testelor si Rezultate

Pentru a rula intreaga suita de teste si a genera raportul de coverage, se folosesc urmatoarele comenzi din radacina proiectului:

1. Rulare pytest pentru toate testele:
   pytest ProjectFinal/functional_testing.py ProjectFinal/structural_tests.py ProjectFinal/mutation_tests.py -v
2. Masurare coverage:
   coverage run --branch -m pytest ProjectFinal/functional_testing.py ProjectFinal/structural_tests.py ProjectFinal/mutation_tests.py
3. Generare raport in terminal:
   coverage report -m

### Capturi de ecran rezultate:

[IMAGINE: pytest.png - Rezultatele rularii tuturor testelor]
[IMAGINE: coverage_run_test.png - Comanda de masurare coverage]
[IMAGINE: report_m.png - Raportul de coverage final]

## Raport Utilizare AI
[LOC PENTRU RAPORT UTILIZARE AI - COMPARATIE TESTE MANUALE VS AUTOGENERATE]

## Demo si Prezentare
[LOC PENTRU LINK VIDEO DEMO PROIECT]
[LOC PENTRU LINK PREZENTARE PPT / PDF]