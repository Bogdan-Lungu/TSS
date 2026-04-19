import pytest
from main import CinemaSystem

@pytest.fixture
def cinema():
    return CinemaSystem()

def test_kill_mutant_loyalty_boundary(cinema):
    """
    omoara mutantul care schimba '>' in '>=' la punctele de fidelitate
    cod original: if loyalty_points > 50: (50 nu are reducere)
    """
    # testam exact valoarea 50
    # daca pretul este 30.0, inseamna ca NU s-a aplicat reducerea (corect)
    # daca un mutant ar schimba in '>=', pretul ar fi 27.0 si testul ar pica (mutant omorat)
    price = cinema.calculate_price(age=30, is_student=False, day=1, row=0, loyalty_points=50)
    assert price == 30.0, "Mutantul de loialitate a supravietuit! 50 de puncte nu ar trebui sa ofere reducere."

def test_kill_mutant_senior_boundary(cinema):
    """
    omoara mutantul care schimba '>=' in '>' la varsta de pensionar
    cod original: if age >= 65: (65 are reducere)
    """
    # testam exact varsta de 65
    # daca pretul este 27.0 (30 * 0.9), inseamna ca s-a aplicat reducerea (corect)
    # daca un mutant ar schimba in '>', pretul ar fi 30.0 si testul ar pica (mutant omorat)
    price = cinema.calculate_price(age=65, is_student=False, day=1, row=0, loyalty_points=0)
    assert price == 27.0, "Mutantul de varsta a supravietuit! La 65 de ani trebuie sa existe reducere."

def test_kill_mutant_student_weekend(cinema):
    """
    omoara mutantul care schimba 'day <= 5' in 'day < 5' la reducerea de student
    vineri (ziua 5) trebuie sa aiba inca reducere de student
    """
    # vineri (5) este ultima zi lucratoare
    # studentul trebuie sa aiba reducere
    # 30 * 0.85 = 25.5
    price = cinema.calculate_price(age=20, is_student=True, day=5, row=0, loyalty_points=0)
    assert price == 25.5, "Mutantul de zi student a supravietuit! Vinerea trebuie sa aiba reducere."