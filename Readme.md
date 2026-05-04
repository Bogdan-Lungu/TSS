# Proiect Testarea Sistemelor Software - Sistem Cinema

## Tema: Testare unitara in Python
## Membrii Echipei
- Lungu Bogdan Cosmin
- Lascu Daniel

## Descriere Proiect
Acest proiect implementeaza un sistem de gestiune pentru rezervari cinema, cu logica de calcul a pretului biletului in functie de varsta, statut student, zi, rand si puncte de loialitate. Proiectul acopera toate cele 3 etape de implementare si testare: functionala, structurala si mutation testing.

## Configuratie Sistem
- Sistem de Operare: Windows 11
- Limbaj de Programare: Python 3.14.2
- Biblioteci folosite:
    - colorama 0.4.6
    - coverage 7.13.5
    - iniconfig 2.3.0
    - mutmut 2.5.1 (mutation testing — versiunea 2.x este ultima cu suport Windows nativ)
    - packaging 26.0
    - pip 25.3
    - pluggy 1.6.0
    - Pygments 2.20.0
    - pytest 9.0.3

Pentru reproductibilitate, dependintele sunt fixate in `requirements.txt`:
```
pip install -r requirements.txt
```

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

<img width="1012" height="770" alt="cfg_base_code" src="https://github.com/user-attachments/assets/50094425-33a1-40e7-a4bc-e21243051540" />
<br>
<img width="728" height="1294" alt="cfg_arbore" src="https://github.com/user-attachments/assets/7aea843e-dbe3-40c4-8d47-6cbb473374fd" />
<br>
Strategii implementate:
- Statement Coverage: Toate instructiunile executate.
- Decision Coverage: Toate ramurile decizionale (True/False) acoperite.
- Condition Coverage: Testarea conditiilor atomice din expresiile compuse.
- Circuite Independente: Identificarea si testarea cailor de baza conform McCabe.

## Mutation Testing

### Tool si configurare
- **Tool**: `mutmut` v2.5.1 
- **Scope unit testing**: metoda `CinemaSystem.calculate_price` (SUT). Mutantii din `main()` (loop interactiv I/O), `__init__` (initializare matrice locuri) si `book_seat` sunt clasificati ca *out-of-unit-test-scope* - nu tin de unit testing pe `calculate_price`.

### Comenzi de baza
```bash
# PYTHONIOENCODING e necesara pe Windows pentru emoji-urile mutmut
set PYTHONIOENCODING=utf-8

python -m mutmut run        # genereaza si testeaza mutantii
python -m mutmut results    # listeaza supravietuitorii
python -m mutmut show <id>  # arata diff-ul unui mutant
python -m mutmut html       # genereaza raport HTML in html/
```

### Procesul de mutation testing - 2 treceri (Pass A / Pass B)

Procesul de mutation testing a fost impartit in **2 treceri**: prima trecere ruleaza mutmut doar cu suita functional + structural si identifica mutantii ce supravietuiesc, apoi scriem teste tintite in `mutation_tests.py` care omoara acei mutanti, iar la a doua trecere reluam mutmut cu suita extinsa pentru a confirma cresterea scorului.

---

#### PRIMA TRECERE (Pass A) - doar `functional_testing.py` + `structural_tests.py`

`setup.cfg` configurat fara `mutation_tests.py`:
```ini
[mutmut]
paths_to_mutate=main.py
tests_dir=.
runner=python -m pytest -x --tb=no -q functional_testing.py structural_tests.py
```

Mutmut a generat **147 de mutanti** pe `main.py` si i-a testat cu suita existenta:

<img width="773" height="595" alt="mutation_testing_functional_structural_tests" src="https://github.com/user-attachments/assets/255f46fc-06cf-4526-9834-28683067dc3d" />
<br>
<img width="427" height="167" alt="mutation_testing_functional_structural_result" src="https://github.com/user-attachments/assets/dde5dde7-b18e-468e-bbed-ada741e9c2ba" />
<br>


**Rezultat Pass A:**

| Metrica | Valoare |
|---|---|
| Mutanti generati | 147 |
| Mutanti omorati | **45** |
| Mutanti supravietuitori | **102** |
| Mutation score | **30.61%** |

**De ce supravietuiesc atatia mutanti?** SUT-ul declarat (`calculate_price`) este o portiune mica (~30 linii) din `main.py`. Restul fisierului contine cod care nu intra in unit testing-ul SUT:
- `main()` — loop interactiv cu `input()` / `print()` (~85 mutanti, IDs 61-145)
- `__init__` — initializarea matricei de locuri (4 mutanti, IDs 19-22)
- guard `if __name__ == "__main__"` (1 mutant, ID 147)

Dintre cei **102 supravietuitori**, doar un subset mic se afla in scope-ul real al SUT.

---

#### Identificarea mutantilor in scope SUT

Folosind `python -m mutmut show <id>` pentru fiecare supravietuitor relevant, am identificat **5 categorii de mutanti** in scope-ul `calculate_price` pentru care suita functional + structural nu avea teste:

| # | IDs mutmut | Tip mutatie | Exemplu diff |
|---|---|---|---|
| 1 | 2 | Lista `DAYS` — lipseste marti (day=2) | `[1, 2, 3, ...]` → `[1, 3, 3, ...]` |
| 2 | 9..15 (7 mutanti) | Constante `MOVIES` alterate cu prefix/sufix | `"Batman"` → `"XXBatmanXX"` |
| 3 | 24 | Mesaj `ValueError("Zi invalida (1-7)")` | string mutat — substring match nu prinde |
| 4 | 30 | Mesaj `ValueError("Rand invalid (0-9)")` | string mutat — substring match nu prinde |
| 5 | 54 | Boundary operator pentru reducerea student | `is_student and day <= 5` → `is_student and day < 5` |

Pentru fiecare categorie am scris un test in `mutation_tests.py` care diferentiaza explicit codul original de mutant.

---

#### A DOUA TRECERE (Pass B) - cu `mutation_tests.py` adaugat

`setup.cfg` actualizat:
```ini
runner=python -m pytest -x --tb=no -q functional_testing.py structural_tests.py mutation_tests.py
```

Cele **5 teste** din `mutation_tests.py` care tintesc cele 5 categorii identificate:

| Test | Categoria tintita | Mutanti omorati |
|---|---|---|
| `test_kill_mutmut_id_2_days_contains_tuesday` | DAYS — marti | 1 |
| `test_kill_mutmut_id_13_movies_constant_integrity` | MOVIES — toate filmele | 7 |
| `test_kill_mutant_id_24_error_message_day_exact` | "Zi invalida (1-7)" exact match | 1 |
| `test_kill_mutant_id_30_error_message_row_exact` | "Rand invalid (0-9)" exact match | 1 |
| `test_kill_mutmut_id_54_student_day_friday_boundary` | boundary `day <= 5` | 1 |
| **TOTAL** | | **11 mutanti omorati** |

Re-rulam mutmut cu cache curat pentru a forta re-evaluarea tuturor mutantilor:
```powershell
Remove-Item -Recurse -Force .mutmut-cache, html
$env:PYTHONIOENCODING="utf-8"
python -m mutmut run
```
<img width="778" height="576" alt="mutmut_run" src="https://github.com/user-attachments/assets/a403e9d8-2949-4333-80a7-245154650ab4" />
<br>
<img width="420" height="152" alt="mutation_report" src="https://github.com/user-attachments/assets/1bb4521b-ff03-43a3-92ae-bacdaa1cc6d3" />
<br>
**Rezultat Pass B:**

| Metrica | Valoare |
|---|---|
| Mutanti generati | 147 |
| Mutanti omorati | **56** |
| Mutanti supravietuitori | **91** |
| Mutation score | **38.10%** |

---

### Raport comparativ Pass A vs Pass B

| Metrica | Pass A (functional + structural) | Pass B (+ mutation_tests) | Diferenta |
|---|---|---|---|
| Mutanti generati | 147 | 147 | — |
| **Mutanti omorati** | 45 | **56** | **+11** |
| **Mutanti supravietuitori** | **102** | **91** | **−11** |
| **Mutation score** | 30.61% | **38.10%** | **+7.49 pp** |

Cresterea de **+11 mutanti omorati** in Pass B corespunde exact celor 11 mutanti din scope-ul SUT pe care i-am tintit cu cele 5 teste noi adaugate in `mutation_tests.py` (1 + 7 + 1 + 1 + 1). Cei **91 mutanti ramasi in viata** sunt cu totii **out-of-scope** - apartin functiei `main()` (UI loop interactiv), `__init__` (matricea de locuri) si guard-ului `if __name__ == "__main__"`.


## Rularea Testelor si Rezultate

Pentru a rula intreaga suita de teste si a genera raportul de coverage, se folosesc urmatoarele comenzi din radacina proiectului:

1. Rulare pytest pentru toate testele:
   `pytest functional_testing.py structural_tests.py mutation_tests.py -v`
2. Masurare coverage:
   `coverage run --branch -m pytest functional_testing.py structural_tests.py mutation_tests.py`
3. Generare raport in terminal:
   `coverage report -m`
4. Rulare mutation testing (pe Windows, cu encoding setat):
   `set PYTHONIOENCODING=utf-8 && python -m mutmut run`
5. Listare mutanti + raport HTML:
   `python -m mutmut results && python -m mutmut html`

### Capturi de ecran rezultate:

<img width="1356" height="1017" alt="pytest_run_2" src="https://github.com/user-attachments/assets/0a80e166-4f91-4511-b3f2-9cee66b5231d" />
<br>
<img width="1356" height="1017" alt="pytest_run" src="https://github.com/user-attachments/assets/ac9124f6-ba1a-43ce-85a6-f06abd586edc" />
<br>
<img width="1355" height="261" alt="coverage_run" src="https://github.com/user-attachments/assets/23539cc8-6183-4ebe-b60f-fe80c7d2d652" />
<br>
<img width="791" height="200" alt="coverage_report" src="https://github.com/user-attachments/assets/36b73d3a-5537-4ed7-97d4-6d79dd8dfb4f" />
<br>


## Raport Utilizare AI
[LOC PENTRU RAPORT UTILIZARE AI - COMPARATIE TESTE MANUALE VS AUTOGENERATE]

## Demo si Prezentare
[LOC PENTRU LINK VIDEO DEMO PROIECT]
[LOC PENTRU LINK PREZENTARE PPT / PDF]
