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

<p align="center">
<img width="1012" height="770" alt="cfg_base_code" src="https://github.com/user-attachments/assets/d540beab-3f5f-4b2e-b2fb-bbbd96d25686" />
</p>
<br>
<p align="center">
<img width="728" height="1294" alt="cfg_arbore" src="https://github.com/user-attachments/assets/b704cd40-a99c-4231-92df-8182fafc994d" />
</p>

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
<p align="center">
<img width="1650" height="1190" alt="rulare_pytest" src="https://github.com/user-attachments/assets/acfd319d-e3f0-45bf-9122-9d1cccb390f4" />
<br>
<img width="1638" height="206" alt="rulare_coverage_run" src="https://github.com/user-attachments/assets/d8fa7b4b-d0ea-4fa0-8be2-eb8d66ec3620" />
<br>
<img width="710" height="155" alt="generare_raport" src="https://github.com/user-attachments/assets/f0711309-33d1-47e2-9c60-972fc46a9109" />
</p>

## Raport Utilizare AI
To be added...

## Demo si Prezentare
To be added...video
To be added...ppt
