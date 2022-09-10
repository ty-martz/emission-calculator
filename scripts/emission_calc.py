import numpy as np

def emission_calculator(miles, num_pax=1, exclude_rad_force=True, rad_force=1.891, lbs_to_metr_tons=1/2204.62, em_pp=0.35, round_trip=False, two_way=1):
    '''
    parameters:
        miles: 
    '''
    if round_trip == False:
        two_way = 2
    if exclude_rad_force == True:
        rad_force = 1
    
    if False:
        print('----')
        print('emiss_calc_debug')
        print(f'miles = {type(miles)}')
        print(f'npax = {type(num_pax)}')
        print(f'em_pp = {em_pp}')
        print(f'lbs_cov = {lbs_to_metr_tons}')
        print(f'rf = {exclude_rad_force}')
        print(f'rf_factor = {rad_force}')
        print(f'2way = {round_trip}')
        print(f'rt factor = {two_way}')
        print('')
        
    calc = miles * num_pax * em_pp * lbs_to_metr_tons * rad_force * two_way
    #print(f'Assuming {em_pp} lbs of CO2/pax/mile ==> Tonnes = {calc}')
    return calc