import pytest
from main import CinemaSystem

@pytest.fixture
def cinema():
    return CinemaSystem()

# statement coverage
def test_statement_coverage_errors(cinema):
    # linie 4 (zi invalida)
    with pytest.raises(ValueError, match="Zi invalida"):
        cinema.calculate_price(day=8, age=20, is_student=False, row=0, loyalty_points=0)
    
    # linie 6 (rand invalid)
    with pytest.raises(ValueError, match="Rand invalid"):
        cinema.calculate_price(day=1, age=20, is_student=False, row=11, loyalty_points=0)

def test_statement_coverage_all_paths(cinema):
    # atinge liniile 12, 15, 19, 24 (VIP, Loyalty, Weekend, Pensionar)
    # price: 30 + 15 = 45 -> 45 * 0.9 = 40.5 -> 40.5 * 1.1 = 44.55 -> 44.55 * 0.9 = 40.10
    price = cinema.calculate_price(age=70, is_student=False, day=6, row=5, loyalty_points=60)
    assert price == 40.10

    # atinge linia 26 (Student)
    # price: 30 * 0.85 = 25.5
    price = cinema.calculate_price(age=20, is_student=True, day=1, row=0, loyalty_points=0)
    assert price == 25.5

# decision coverage
def test_decision_coverage_false_branches(cinema):
    # testam ramurile "False" pentru IF-urile fara ELSE (liniile 11, 14, 18, 25)
    # nu e VIP, nu are fidelitate, nu e weekend, nu e pensionar, nu e student
    price = cinema.calculate_price(age=30, is_student=False, day=1, row=1, loyalty_points=10)
    assert price == 30.0

# condition coverage (MC/DC logic)
def test_condition_coverage_student_logic(cinema):
    # conditie: is_student and day <= 5
    # 1. True and True -> discount
    assert cinema.calculate_price(20, True, 1, 0, 0) == 25.5
    # 2. True and False (is_student=True, day=6) -> No discount 
    # 30 * 1.1 = 33.0
    assert cinema.calculate_price(20, True, 6, 0, 0) == 33.0
    # 3. False and True (is_student=False, day=1) -> No discount
    assert cinema.calculate_price(20, False, 1, 0, 0) == 30.0

# independent paths (McCabe)
# complexitatea ciclomatica = 8 
# (7 decizii + 1 calea de baza)
def test_independent_circuits_mccabe(cinema):
    # path 1: zi invalida (3 -> 4)
    with pytest.raises(ValueError):
        cinema.calculate_price(age=20, is_student=False, day=0, row=0, loyalty_points=0)
    
    # path 2: rand invalid (5 -> 6)
    with pytest.raises(ValueError):
        cinema.calculate_price(age=20, is_student=False, day=1, row=-1, loyalty_points=0)
        
    # path 3: calea simpla
    assert cinema.calculate_price(30, False, 1, 0, 0) == 30.0
    
    # path 4: VIP Only
    assert cinema.calculate_price(30, False, 1, 5, 0) == 45.0
    
    # path 5: Loyalty Only
    assert cinema.calculate_price(30, False, 1, 0, 100) == 27.0
    
    # path 6: Weekend Only
    assert cinema.calculate_price(30, False, 6, 0, 0) == 33.0
    
    # path 7: Pensionar Only
    assert cinema.calculate_price(65, False, 1, 0, 0) == 27.0
    
    # path 8: Student Only (zi lucratoare)
    assert cinema.calculate_price(20, True, 1, 0, 0) == 25.5
