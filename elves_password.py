def nth_digit(n, idx):
    return n // 10**idx % 10

def nb_digits(n):
    nb = 1
    while(True):
        n = n // 10
        if n > 0:
            nb += 1
        else:
            break
    return nb

def meets_criteras(n):
    if n > 999999 or n < 0:
        return False
    
    last_number = None
    nb_adjacent_numbers_in_a_row = 1
    has_two_adjacent_numbers = False

    for idx in range(nb_digits(n)):
        digit = nth_digit(n, idx)

        if not last_number is None:
            if digit > last_number:
                return False
            
            if digit == last_number:
                nb_adjacent_numbers_in_a_row += 1
            else:
                if nb_adjacent_numbers_in_a_row == 2:
                    has_two_adjacent_numbers = True
                nb_adjacent_numbers_in_a_row = 1
        last_number = digit
    
    if nb_adjacent_numbers_in_a_row == 2:
        has_two_adjacent_numbers = True

    return has_two_adjacent_numbers

assert(meets_criteras(112222))
assert(meets_criteras(111122))
assert(not meets_criteras(123444))

nb_ok = 0
for i in range(272091, 815433):
    if meets_criteras(i):
        nb_ok += 1

print(nb_ok)