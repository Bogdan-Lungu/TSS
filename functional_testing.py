import unittest
import itertools
from main import CinemaSystem 

class TestCinemaComprehensive(unittest.TestCase):

    def setUp(self):
        self.system = CinemaSystem()

    def oracle_price(self, age, is_student, day, row, loyalty):
        """oracol care calculeaza manual pretul asteptat conform specificatiei"""
        price = 30.0
        if 4 <= row <= 6: price += 15.0
        if loyalty > 50: price *= 0.9
        if day >= 6: price *= 1.1
        if age >= 65: price *= 0.9
        elif is_student and day <= 5: price *= 0.85
        return round(price, 2)

    def test_strong_normal_equivalence(self):
        """genereaza si testeaza automat toate cele 32 de combinatii valide"""
        # definirea valorilor reprezentative pentru fiecare clasa
        data = {
            "age": [30, 70],
            "is_student": [True, False],
            "day": [3, 7],
            "row": [2, 5],
            "loyalty": [10, 60]
        }

        # generam produsul cartezian
        combinations = list(itertools.product(*data.values()))
        
        for params in combinations:
            age, is_student, day, row, loyalty = params
            expected = self.oracle_price(age, is_student, day, row, loyalty)
            
            with self.subTest(params=params):
                actual = self.system.calculate_price(age, is_student, day, row, loyalty)
                self.assertEqual(actual, expected, f"Eroare la combinatia: {params}")

    def test_boundary_value_analysis(self):
        """Testeaza valorile critice de frontiera (BVA)."""
        # (varsta, student, zi, rand, puncte)
        bva_cases = [
            (64, False, 1, 1, 0),   # imediat sub limita de Senior
            (65, False, 1, 1, 0),   # limita de senior (reducere 10%)
            
            (30, False, 1, 1, 50),  # limita de loialitate fara reducere
            (30, False, 1, 1, 51),  # limita de loialitate cu reducere
            
            (30, False, 1, 3, 0),   # rand imediat sub VIP
            (30, False, 1, 4, 0),   # primul rand VIP
            (30, False, 1, 6, 0),
            (30, False, 1, 7, 0),
            (30, False, 1, 0, 0),
            (30, False, 1, 9, 0),
            
            (30, False, 5, 1, 0),   # vineri (ultima zi fara taxa weekend)
            (30, False, 6, 1, 0),   # sambata (prima zi cu taxa weekend)
            (30, True, 1, 1, 0),   
            (30, True, 7, 1, 0),   
        ]

        for age, stud, day, row, loy in bva_cases:
            with self.subTest(bva=age):
                actual = self.system.calculate_price(age, stud, day, row, loy)
                self.assertEqual(actual, self.oracle_price(age, stud, day, row, loy))

    def test_robustness_invalid_values(self):
        """testeaza valorile invalide (BVA externe)"""
        invalid_cases = [
            (30, False, 0, 1, 10), # zi sub 1
            (30, False, 8, 1, 10), # zi peste 7
            (30, False, 1, -1, 10),# rand sub 0
            (30, False, 1, 10, 10) # rand peste 9
        ]

        for age, stud, day, row, loy in invalid_cases:
            with self.subTest(invalid=day):
                with self.assertRaises(ValueError):
                    self.system.calculate_price(age, stud, day, row, loy)

if __name__ == '__main__':
    unittest.main()