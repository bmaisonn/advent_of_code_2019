import pandas as pd

def compute_fuel_amount(mass):
    return (mass//3) - 2

def compute_fuel_for_fuel(mass):
    fuel_need_for_fuel = 0
    tmp = mass

    while True:
        fuel_for_fuel = compute_fuel_amount(tmp)
        if fuel_for_fuel <= 0:
            break
        fuel_need_for_fuel += fuel_for_fuel
        tmp = fuel_for_fuel
    
    return fuel_need_for_fuel

def compute_fuel_need_for_pod(df):
    df['fuel_per_pod'] = (df['mass']
                          .apply(compute_fuel_amount))
    df['fuel_for_fuel'] = (df['fuel_per_pod']
                          .apply(compute_fuel_for_fuel))
    return df



if __name__ == '__main__':

    df = (pd
         .read_csv('/mnt/c/Users/Bertrand/Documents/advent/input1_pods_mass.txt', names=['mass'])
         .pipe(compute_fuel_need_for_pod))

    fuel_needed = (df['fuel_per_pod'] + df['fuel_for_fuel']).sum()
    
    print(fuel_needed)

