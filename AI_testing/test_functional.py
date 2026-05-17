
import unittest
from main import CinemaSystem

class TestCinemaFunctional(unittest.TestCase):
    def setUp(self):
        self.cinema = CinemaSystem()

    # --- 1. Partiționare în Clase de Echivalență (ECP) ---
    def test_ecp_valid_regular_no_discount(self):
        # Clasa: Zi saptamana (1-5), Rand normal, Non-VIP, Fara reducere varsta/fidelitate/student
        self.assertEqual(self.cinema.calculate_price(30, False, 3, 2, 10), 30.0)

    def test_ecp_valid_vip_weekend_senior_loyalty(self):
        # Clase cumulate: Weekend (6-7), VIP (4-6), Pensionar (>=65), Fidelitate (>50)
        # Calcul: (30+15)*0.9*1.1*0.9 = 45 * 0.9 * 1.1 * 0.9 = 40.095 -> rotunjit la 40.10
        self.assertEqual(self.cinema.calculate_price(70, False, 6, 5, 100), 40.10)

    def test_ecp_valid_student_discount(self):
        # Clasa: Student în zi de săptămână
        self.assertEqual(self.cinema.calculate_price(20, True, 2, 1, 0), 25.50)

    def test_ecp_invalid_day_exception(self):
        # Clasa invalida: Ziua > 7
        with self.assertRaises(ValueError):
            self.cinema.calculate_price(30, False, 8, 2, 10)

    def test_ecp_invalid_row_exception(self):
        # Clasa invalida: Rand > 9
        with self.assertRaises(ValueError):
            self.cinema.calculate_price(30, False, 3, 10, 10)

    # --- 2. Analiza Valorilor de Frontieră (BVA) ---
    def test_bva_day_boundaries(self):
        # Limitele saptamanii si trecerea la weekend
        self.assertEqual(self.cinema.calculate_price(30, False, 1, 2, 10), 30.0)  # Luni
        self.assertEqual(self.cinema.calculate_price(30, False, 5, 2, 10), 30.0)  # Vineri
        self.assertEqual(self.cinema.calculate_price(30, False, 6, 2, 10), 33.0)  # Sambata
        self.assertEqual(self.cinema.calculate_price(30, False, 7, 2, 10), 33.0)  # Duminica

    def test_bva_row_boundaries(self):
        # Limitele locurilor VIP (4, 5, 6)
        self.assertEqual(self.cinema.calculate_price(30, False, 3, 3, 10), 30.0)  # Sub VIP
        self.assertEqual(self.cinema.calculate_price(30, False, 3, 4, 10), 45.0)  # VIP inceput
        self.assertEqual(self.cinema.calculate_price(30, False, 3, 6, 10), 45.0)  # VIP sfarsit
        self.assertEqual(self.cinema.calculate_price(30, False, 3, 7, 10), 30.0)  # Peste VIP

    def test_bva_age_boundaries(self):
        # Limita pentru pensionar
        self.assertEqual(self.cinema.calculate_price(64, False, 3, 2, 10), 30.0)  # Imediat sub limita
        self.assertEqual(self.cinema.calculate_price(65, False, 3, 2, 10), 27.0)  # Fix pe limita

    def test_bva_loyalty_boundaries(self):
        # Limita pentru puncte fidelitate
        self.assertEqual(self.cinema.calculate_price(30, False, 3, 2, 50), 30.0)  # Fix limita (nu intra)
        self.assertEqual(self.cinema.calculate_price(30, False, 3, 2, 51), 27.0)  # Imediat peste limita

if __name__ == '__main__':
    unittest.main()
