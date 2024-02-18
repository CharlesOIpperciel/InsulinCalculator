import math

# Constants
ACIDOSE_DOSE = 0.1
HYPERGLYCEMIE_CETONE_DOSE = 0.8
HYPERGLYCEMIE_SANS_CETONE_DOSE = 0.6
INJECTION_3 = 3
INJECTION_4 = 4


def round_numbers(value):
    x = math.floor(value)
    if (value - x) < .50:
        return x
    else:
        return math.ceil(value)


def get_state():
    while True:
        print('\nVeuillez choisir parmi les trois situations au diagnostic suivantes (1,2 ou 3):')
        print('1. Acidose (1u/kg/jour)')
        print('2. Hyperglycémie + cétone (0,8u/kg/jr)')
        print('3. Hyperglycémie sans cétone (0,6u/kg/jr)\n')
        state = input('Choix: ')

        if state == '1':
            return ACIDOSE_DOSE
        elif state == '2':
            return HYPERGLYCEMIE_CETONE_DOSE
        elif state == '3':
            return HYPERGLYCEMIE_SANS_CETONE_DOSE
        else:
            print('Choix invalide.')


def get_weight():
    while True:
        input_weight = input('\nVeuillez entrez le poids du patient en kg avec un point (exemple: xx.xx): ')

        try:
            weight = float(input_weight)
            if weight < 0:
                print('\nLe poids ne peut pas être plus petit que 0.')
            else:
                return weight
        except ValueError:
            print('\nVeuillez entrer une valeur valide.')


def get_injections():
    while True:
        print('\nVeuillez choisir parmi les deux types de régime suivants (3 ou 4):')
        print('- 3 injections')
        print('- 4 injections\n')
        choice = input('Choix: ')

        if choice == '3' or choice == '4':
            return int(choice)
        else:
            print('Choix invalide.')


def summary(state, weight, injections):
    print(f'\nSituation au diagnostic: {state} u/kg/jr')
    print(f'Poids du patient: {weight} kg')
    print(f'Type de régime: {injections} injections')


def get_DTQ(regime, poids):
    print(f'DTQ: {round_numbers(regime * poids)} u/jr')
    return round_numbers(regime * poids)


def get_standard_doses_per_meal(DTQ, injectionType):
    if injectionType == 3:
        UR_Dejeuner = round_numbers((DTQ * (2 / 3)) * (1 / 3))
        UR_Souper = round_numbers((DTQ * (1 / 3)) * (1 / 2))
        return UR_Dejeuner, UR_Souper
    if injectionType == 4:
        return round_numbers((0.6 * DTQ) / 3)
    return None


def get_sensibility(DTQ):
    return round_numbers(100 / DTQ)


def get_correction(interval, se, ng):
    return round_numbers((interval - ng) / se)


def hs_correction(interval, se, sd):
    if round_numbers((interval - sd) / se) < 0:
        return 0
    return round_numbers((interval - sd) / se)


def print_rapid_table(DTQ, injectionType):
    sensibility = get_sensibility(DTQ)
    glycemie_normale = 5
    glycemie_normale2 = 7
    interval1 = 8
    interval2 = 12
    interval3 = 17

    if injectionType == 3:
        sd_dej, sd_souper = get_standard_doses_per_meal(DTQ, injectionType)
        thirdRow_dej = sd_dej + get_correction(interval1, sensibility, glycemie_normale)
        fourthRow_dej = sd_dej + get_correction(interval2, sensibility, glycemie_normale)
        fifthRow_dej = sd_dej + get_correction(interval3, sensibility, glycemie_normale)
        thirdRow_souper = sd_souper + get_correction(interval1, sensibility, glycemie_normale)
        fourthRow_souper = sd_souper + get_correction(interval2, sensibility, glycemie_normale)
        fifthRow_souper = sd_souper + get_correction(interval3, sensibility, glycemie_normale)
        fourthRowHS = hs_correction(interval2, sensibility, glycemie_normale2)
        fifthRowHS = hs_correction(interval3, sensibility, glycemie_normale2)

        belowSd_dej = sd_dej - get_correction(interval1, sensibility, glycemie_normale)
        belowSd_souper = sd_souper - get_correction(interval1, sensibility, glycemie_normale)

        print(f'|---------- Rapid (UR) Table -- Sensibilité: {sensibility} ----------|')
        print('|--------------------------------------------------------|')
        print('|------------------ | Déjeuner (u) | Souper (u) | HS (u) |')
        print(f'|[< 4] ------------ |    {belowSd_dej:3}       |   {belowSd_souper:3}      |   0    |')
        print(f'|[4,1 < {interval1}] -------- |    {sd_dej:3}       |   {sd_souper:3}      |   0    |')
        print(f'|[8,1 < {interval2}] ------- |    {thirdRow_dej:3}       |   {thirdRow_souper:3}      |   0    |')
        print(
            f'|[12,1 < {interval3}]------- |    {fourthRow_dej:3}       |   {fourthRow_souper:3}      | {fourthRowHS:3}    |')
        print(f'|[> 17] ----------- |    {fifthRow_dej:3}       |   {fifthRow_souper:3}      | {fifthRowHS:3}    |')
        print('|--------------------------------------------------------|')

    elif injectionType == 4:
        sd = get_standard_doses_per_meal(DTQ, injectionType)
        thirdRow = sd + get_correction(interval1, sensibility, glycemie_normale)
        fourthRow = sd + get_correction(interval2, sensibility, glycemie_normale)
        fifthRow = sd + get_correction(interval3, sensibility, glycemie_normale)
        fourthRowHS = hs_correction(interval2, sensibility, glycemie_normale2)
        fifthRowHS = hs_correction(interval3, sensibility, glycemie_normale2)
        belowSd = sd - get_correction(interval1, sensibility, glycemie_normale)

        print(f'|---------------- Rapid (UR) Table -- Sensibilité: {sensibility} ----------------|')
        print('|--------------------------------------------------------------------|')
        print('|------------------ | Déjeuner (u) | Diner (u) | Souper (u) | HS (u) |')
        print(f'|[< 4] ------------ |    {belowSd:3}       |   {belowSd:3}     |   {belowSd:3}      |   0    |')
        print(f'|[4,1 < {interval1}] -------- |    {sd:3}       |   {sd:3}     |   {sd:3}      |   0    |')
        print(
            f'|[8,1 < {interval2}] ------- |    {thirdRow:3}       |   {thirdRow:3}     |   {thirdRow:3}      |   0    |')
        print(
            f'|[12,1 < {interval3}]------- |    {fourthRow:3}       |   {fourthRow:3}     |   {fourthRow:3}      | {fourthRowHS:3}    |')
        print(
            f'|[> 17] ----------- |    {fifthRow:3}       |   {fifthRow:3}     |   {fifthRow:3}      | {fifthRowHS:3}    |')
        print('|--------------------------------------------------------------------|')


def print_basal_value(DTQ, injectionType):
    if injectionType == 3:
        NPH_Dej = round_numbers((DTQ * (2 / 3)) * (2 / 3))
        NPH_HS = round_numbers((DTQ * (1 / 3)) * (1 / 2))
        print(f'NPH Déjeuner: {NPH_Dej} u')
        print(f'NPH HS: {NPH_HS} u')
    elif injectionType == 4:
        basale = 0.4 * DTQ
        print(f'Basale (HS): {basale} u')


def generate_rapid_table(DTQ, injectionType):
    print_basal_value(DTQ, injectionType)
    print_rapid_table(DTQ, injectionType)


def main():
    regime = get_state()
    poids = get_weight()
    injections = get_injections()
    summary(regime, poids, injections)

    generate_rapid_table(get_DTQ(regime, poids), injections)


if __name__ == '__main__':
    main()
