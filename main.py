import sys

DAYS = [1, 2, 3, 4, 5, 6, 7]
MOVIES = ["Dune 2", "Batman", "Spider-Man", "Inception", "Titanic", "Avatar", "Joker"]
BASE_PRICE = 30.0

class CinemaSystem:
    def __init__(self):
        self.seats = {
            movie: {day: [[False for _ in range(10)] for _ in range(10)] for day in DAYS}
            for movie in MOVIES
        }

    def calculate_price(self, age, is_student, day, row, loyalty_points):
        """calculeaza pretul biletului bazat pe zi, varsta, statut de student si rand"""
        if day not in DAYS:
            raise ValueError("Zi invalida (1-7)")
        if not (0 <= row <= 9):
            raise ValueError("Rand invalid (0-9)")

        current_price = BASE_PRICE

        # locuri VIP (randurile 4, 5, 6)
        if 4 <= row <= 6:
            current_price += 15.0
            
        if loyalty_points > 50:
            current_price *= 0.9

        # scumpire weekend
        if day >= 6:
            current_price *= 1.1

        # reducere (prioritate pensionar >= 65 ani)
        # 2 tipuri de reduceri: pensionar/student
        if age >= 65:
            current_price *= 0.9  
        elif is_student and day <= 5: 
            current_price *= 0.85 

        return round(current_price, 2)

    def calculate_group_total(self, prices_list):
        """aplica reducerea de grup de 10% pentru minimum 5 bilete"""
        if not isinstance(prices_list, list):
            raise TypeError("prices_list trebuie sa fie o lista")
            
        total = sum(prices_list)
        if len(prices_list) >= 5:
            total *= 0.9
        return round(total, 2)

    def book_seat(self, movie, day, row, col):
        if not (0 <= row <= 9 and 0 <= col <= 9):
            raise ValueError("coordonate loc invalide")
        if self.seats[movie][day][row][col]:
            return False # loc ocupat
        self.seats[movie][day][row][col] = True
        return True

def main():
    system = CinemaSystem()
    print("Main Cinema:")

    while True:
        print(f"\nFilme disponibile: {', '.join(MOVIES)}")
        movie_choice = input("Alege filmul (sau 'iesire'): ").strip()
        if movie_choice.lower() == 'iesire': break
        if movie_choice not in MOVIES:
            print("Filmul nu exista!")
            continue

        try:
            day_choice = int(input("Alege ziua (1-Luni,..., 7-Duminica): "))
            if day_choice not in DAYS:
                print("Zi invalida!")
                continue
        except ValueError:
            print("Te rugam sa introduci un numar!")
            continue

        tickets_to_buy = []
        total_cost = 0.0

        while True:
            try:
                age = int(input("Varsta: "))
                is_student = input("Esti student? (da/nu): ").lower() == 'da'
                row = int(input("Randul (0-9): "))
                col = int(input("Coloana (0-9): "))
                loyalty = int(input("Puncte de fidelitate: "))

                price = system.calculate_price(age, is_student, day_choice, row, loyalty)
                
                if system.book_seat(movie_choice, day_choice, row, col):
                    tickets_to_buy.append((row, col, price))
                    total_cost += price
                    print(f"Loc rezervat! Pret: {price} RON")
                else:
                    print("Eroare: Locul este deja rezervat!")

            except ValueError as e:
                print(f"Date invalide: {e}")

            cont = input("\nMai vrei un bilet la acest film? (y/n): ").lower()
            if cont != 'y':
                break

        if tickets_to_buy:
            print("\nChitanta:")
            print(f"Film: {movie_choice} | Ziua: {day_choice}")
            
            # introducem preturile intr-o lista pentru calculul reducerii de grup
            just_prices = [t[2] for t in tickets_to_buy]
            final_total = system.calculate_group_total(just_prices)
            
            for t in tickets_to_buy:
                print(f"  - Rand {t[0]}, Loc {t[1]}: {t[2]} RON")
            
            print(f"Total: {final_total} RON")
            if len(just_prices) >= 5:
                print(" (S-a aplicat o reducere de grup de 10%!)")
            print("--------------------------")

if __name__ == "__main__":
    main()