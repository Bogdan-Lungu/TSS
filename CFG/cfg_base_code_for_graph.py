def calculate_price(self, age, is_student, day, row, loyalty_points):
    """calculeaza pretul biletului bazat pe zi, varsta, statut de student si rand"""
    if day not in DAYS:
        raise ValueError("Zi invalida (1-7)")
    if not (0 <= row <= 9):
        raise ValueError("Rand invalid (0-9)")

    current_price = BASE_PRICE

    # locuri VIP (4, 5, 6)
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


# Diagrama cfg:

# 3 -> 5
# 3 -> 4

# 5 -> 11
# 5 -> 6

# 11 -> 12
# 11 -> 14

# 12 -> 14

# 14 -> 15
# 14 -> 18

# 15 -> 18

# 18 -> 19
# 18 -> 23

# 19 -> 23

# 23 -> 25
# 23 -> 24

# 25 -> 26
# 25 -> 28

# 26 -> 28

# 24 -> 28

# 6 -> 28

# 4 -> 28