
import unittest
from main import CinemaSystem

class TestCinemaStructural(unittest.TestCase):
    def setUp(self):
        self.cinema = CinemaSystem()

    # --- 1. Acoperire la nivel de instrucțiune (Statement Coverage) ---
    def test_statement_coverage_path_1(self):
        # Trecem prin TOATE instructiunile decizionale afirmative
        # row=5 (VIP), loyalty=60, day=6 (weekend), age=66 (senior) -> 40.10
        self.assertEqual(self.cinema.calculate_price(66, False, 6, 5, 60), 40.10)

    def test_statement_coverage_path_2(self):
        # Pentru a atinge si linia cu 'elif is_student and day <= 5'
        self.assertEqual(self.cinema.calculate_price(20, True, 3, 1, 10), 25.50)

    # --- 2. Acoperire la nivel de decizie (Branch/Decision Coverage) ---
    def test_branch_coverage_all_false(self):
        # Validam si faptul ca fiecare `if` este evaluat la False (neprimind scumpiri sau reduceri)
        self.assertEqual(self.cinema.calculate_price(30, False, 2, 1, 10), 30.0)

    # --- 3. Acoperire la nivel de condiție (Condition Coverage) ---
    # Ne concentram pe: elif is_student (C1) and day <= 5 (C2):
    def test_condition_T_T(self):
        # C1=True, C2=True -> se executa
        self.assertEqual(self.cinema.calculate_price(20, True, 3, 1, 10), 25.50)

    def test_condition_T_F(self):
        # C1=True, C2=False (day=6) -> False global
        self.assertEqual(self.cinema.calculate_price(20, True, 6, 1, 10), 33.0)

    def test_condition_F_T(self):
        # C1=False, C2=True -> False global
        self.assertEqual(self.cinema.calculate_price(30, False, 3, 1, 10), 30.0)

    # --- 4. Circuite independente (Independent Paths) ---
    # Complexitatea ciclomatică e 8 (7 structuri de decizie + 1)
    # P1: day invalida
    def test_path_1(self):
        with self.assertRaises(ValueError): self.cinema.calculate_price(30, False, 0, 5, 10)
    # P2: row invalid
    def test_path_2(self):
        with self.assertRaises(ValueError): self.cinema.calculate_price(30, False, 3, 15, 10)
    # P3: nicio reducere/scumpire
    def test_path_3(self):
        self.assertEqual(self.cinema.calculate_price(30, False, 1, 1, 10), 30.0)
    # P4: doar VIP
    def test_path_4(self):
        self.assertEqual(self.cinema.calculate_price(30, False, 1, 5, 10), 45.0)
    # P5: doar Fidelitate
    def test_path_5(self):
        self.assertEqual(self.cinema.calculate_price(30, False, 1, 1, 60), 27.0)
    # P6: doar Weekend
    def test_path_6(self):
        self.assertEqual(self.cinema.calculate_price(30, False, 6, 1, 10), 33.0)
    # P7: doar Senior
    def test_path_7(self):
        self.assertEqual(self.cinema.calculate_price(70, False, 1, 1, 10), 27.0)
    # P8: doar Student
    def test_path_8(self):
        self.assertEqual(self.cinema.calculate_price(20, True, 1, 1, 10), 25.5)

if __name__ == '__main__':
    unittest.main()
