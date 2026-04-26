import pytest
from main import CinemaSystem, DAYS, MOVIES

@pytest.fixture
def cinema():
    return CinemaSystem()

# teste suplimentare derivate din analiza supravietuitorilor
# generati de mutmut pe main.py 

# teste tintesc clase de mutanti care supravietuiesc suitei
# functional_testing.py + structural_tests.py:
#   - mutatii pe string-urile din mesajele de eroare
#   - mutatii pe limitele zilei din saptamana din comparatia 'day <= 5'
#   - mutatii pe string-urile din filmele de input

def test_kill_mutmut_id_2_days_contains_tuesday(cinema):
    """
    mutmut id = 2
    DAYS = [1, 2, 3, 4, 5, 6, 7]  ->  DAYS = [1, 3, 3, 4, 5, 6, 7]
    mutantul scoate ziua 2 din lista. calculate_price(day=2, ...)
    ar arunca ValueError 'Zi invalida' in mutant, dar nu in cod-ul original
    """
    # day=2 (marti) trebuie sa fie zi valida si sa returneze pretul standard
    price = cinema.calculate_price(age=30, is_student=False, day=2, row=0, loyalty_points=0)
    assert price == 30.0, "Mutantul DAYS-tuesday a supravietuit! Day=2 trebuie sa fie valid."

def test_kill_mutmut_id_13_movies_constant_integrity():
    """
    mutmut id = 13
      MOVIES = [..., 'Batman', ...]  ->  MOVIES = [..., 'XXBatmanXX', ...]
    mutmut adauga prefix/sufix 'XX' la fiecare string din MOVIES (7 mutanti)
    suita anterioara nu valida continutul MOVIES, deci toti supravietuiau
    aici verificam exact lista, omorand toti cei 7 mutanti dintr-un singur test
    """
    expected = ["Dune 2", "Batman", "Spider-Man", "Inception", "Titanic", "Avatar", "Joker"]
    assert MOVIES == expected, f"MOVIES a fost mutat: {MOVIES}"

def test_kill_mutant_id_24_error_message_day_exact(cinema):
    """
    mutmut id = 24
    vizeaza mutantii care altereaza string-ul 'Zi invalida (1-7)'
    testele structural_tests.py folosesc match=\"Zi invalida\" (substring)
    deci o mutatie de tip 'XXZi invalida (1-7)XX' supravietuieste
    aici comparam exact intregul mesaj
    """
    with pytest.raises(ValueError) as exc:
        cinema.calculate_price(age=30, is_student=False, day=8, row=0, loyalty_points=0)
    assert str(exc.value) == "Zi invalida (1-7)"

def test_kill_mutant_id_30_error_message_row_exact(cinema):
    """
    mutmut id = 30
    vizeaza mutantii care altereaza string-ul 'Rand invalid (0-9)'
    acelasi pattern ca testul anterior: substring match nu prinde mutatia
    """
    with pytest.raises(ValueError) as exc:
        cinema.calculate_price(age=30, is_student=False, day=1, row=10, loyalty_points=0)
    assert str(exc.value) == "Rand invalid (0-9)"

def test_kill_mutmut_id_54_student_day_friday_boundary(cinema):
    """
    mutmut id = 54
      elif is_student and day <= 5:  ->  elif is_student and day < 5:
    mutatie de tip boundary pe operatorul de comparatie 
    mutantul exclude vinerea (day=5) din intervalul de reducere pentru studenti
    test: student, day=5, fara alte reduceri
      - original: 30.0 * 0.85 = 25.5
      - mutant:   30.0 (nu se aplica reducerea student)
    """
    price = cinema.calculate_price(age=30, is_student=True, day=5, row=0, loyalty_points=0)
    assert price == 25.5, (
        f"Mutantul day<5 a supravietuit! La day=5 student, pretul trebuie sa fie 25.5, "
        f"dar a fost {price}."
    )
