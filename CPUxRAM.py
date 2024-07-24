import crawlerweb_processor as cp
import ram_choice as rc
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib as plt
import numpy as np


def result_CPURAM():

    # Inputs
    clock = ctrl.Antecedent(list(np.arange(1, 14.1, 0.1)), 'Clock')
    nucleo = ctrl.Antecedent(list(np.arange(1, 12.1, 0.1)), 'Nucleo')
    ram = ctrl.Antecedent(list(np.arange(0, 4600.1, 0.1)), 'RAM')

    # Outputs
    result_cpuram = ctrl.Consequent(list(np.arange(0, 100.1, 0.1)), 'Result CPUxRAM')

    # Funções de Pertinência
    clock['Baixo'] = fuzz.trimf(clock.universe, [-2.75, 1, 2])
    clock['Médio'] = fuzz.trimf(clock.universe, [1.5, 2.5, 4])
    clock['Alto'] = fuzz.trapmf(clock.universe, [3, 5.625, 10.38, 13.38]) 

    nucleo['Baixo'] = fuzz.trapmf(nucleo.universe, [-4, 1, 2, 4])
    nucleo['Médio'] = fuzz.trapmf(nucleo.universe, [2, 4, 6, 8])
    nucleo['Alto'] = fuzz.trapmf(nucleo.universe, [6, 8, 10, 12])

    ram['Baixo'] = fuzz.trimf(ram.universe, [-1333.33333333333, 0, 1333.33333333333])
    ram['Médio'] = fuzz.trimf(ram.universe, [266.666666666667, 1600, 2933.33333333333])
    ram['Alto'] = fuzz.trimf(ram.universe, [1866.66666666667, 3200, 6000.33333333333])

    result_cpuram['Pessimo'] = fuzz.trimf(result_cpuram.universe, [-20.8333333333333, 0, 20.8333333333333])
    result_cpuram['Baixo'] = fuzz.trimf(result_cpuram.universe, [4.16666666666667, 25, 45.8333333333333])
    result_cpuram['Médio'] = fuzz.trimf(result_cpuram.universe, [29.1666666666667, 50, 70.8333333333333])
    result_cpuram['Bom'] = fuzz.trimf(result_cpuram.universe, [54.1666666666667, 75, 95.8333333333333])
    result_cpuram['Muito Bom'] = fuzz.trimf(result_cpuram.universe, [79.1666666666667, 100, 120.833333333333])

    # Regras
    rules = [
        ctrl.Rule(clock['Alto'] & nucleo['Alto'] & ram['Alto'], result_cpuram['Muito Bom']),
        ctrl.Rule(clock['Alto'] & nucleo['Alto'] & ram['Médio'], result_cpuram['Muito Bom']),
        ctrl.Rule(clock['Alto'] & nucleo['Alto'] & ram['Baixo'], result_cpuram['Bom']),
        ctrl.Rule(clock['Alto'] & nucleo['Médio'] & ram['Alto'], result_cpuram['Muito Bom']),
        ctrl.Rule(clock['Alto'] & nucleo['Médio'] & ram['Médio'], result_cpuram['Bom']),
        ctrl.Rule(clock['Alto'] & nucleo['Médio'] & ram['Baixo'], result_cpuram['Médio']),
        ctrl.Rule(clock['Alto'] & nucleo['Baixo'] & ram['Alto'], result_cpuram['Muito Bom']),
        ctrl.Rule(clock['Alto'] & nucleo['Baixo'] & ram['Médio'], result_cpuram['Bom']),
        ctrl.Rule(clock['Alto'] & nucleo['Baixo'] & ram['Baixo'], result_cpuram['Médio']),
        ctrl.Rule(clock['Médio'] & nucleo['Alto'] & ram['Alto'], result_cpuram['Muito Bom']),
        ctrl.Rule(clock['Médio'] & nucleo['Alto'] & ram['Médio'], result_cpuram['Bom']),
        ctrl.Rule(clock['Médio'] & nucleo['Alto'] & ram['Baixo'], result_cpuram['Médio']),
        ctrl.Rule(clock['Médio'] & nucleo['Médio'] & ram['Alto'], result_cpuram['Bom']),
        ctrl.Rule(clock['Médio'] & nucleo['Médio'] & ram['Médio'], result_cpuram['Médio']),
        ctrl.Rule(clock['Médio'] & nucleo['Médio'] & ram['Baixo'], result_cpuram['Baixo']),
        ctrl.Rule(clock['Médio'] & nucleo['Baixo'] & ram['Alto'], result_cpuram['Bom']),
        ctrl.Rule(clock['Médio'] & nucleo['Baixo'] & ram['Médio'], result_cpuram['Médio']),
        ctrl.Rule(clock['Médio'] & nucleo['Baixo'] & ram['Baixo'], result_cpuram['Baixo']),
        ctrl.Rule(clock['Baixo'] & nucleo['Alto'] & ram['Alto'], result_cpuram['Bom']),
        ctrl.Rule(clock['Baixo'] & nucleo['Alto'] & ram['Médio'], result_cpuram['Médio']),
        ctrl.Rule(clock['Baixo'] & nucleo['Alto'] & ram['Baixo'], result_cpuram['Baixo']),
        ctrl.Rule(clock['Baixo'] & nucleo['Médio'] & ram['Alto'], result_cpuram['Médio']),
        ctrl.Rule(clock['Baixo'] & nucleo['Médio'] & ram['Médio'], result_cpuram['Baixo']),
        ctrl.Rule(clock['Baixo'] & nucleo['Médio'] & ram['Baixo'], result_cpuram['Pessimo']),
        ctrl.Rule(clock['Baixo'] & nucleo['Baixo'] & ram['Alto'], result_cpuram['Médio']),
        ctrl.Rule(clock['Baixo'] & nucleo['Baixo'] & ram['Médio'], result_cpuram['Baixo']),
        ctrl.Rule(clock['Baixo'] & nucleo['Baixo'] & ram['Baixo'], result_cpuram['Pessimo'])
    ]

    # Criação do sistema de controle e do simulador
    system = ctrl.ControlSystem(rules)
    simulator = ctrl.ControlSystemSimulation(system)

    # Solicita o nome do processador ao usuário
    results_cp = cp.return_id()

    # Retorna o nome e a id do processador
    url = cp.opcions(results_cp)

    # Chama a função para obter as informações da processador
    classificacao_cores, classificacao_clock_speed = cp.get_processor_info(url)

    # Define a frequencia da ram
    f_ram = int(input("\nDiga qual a frequencia da RAM: "))
        
    classificacao_frequencia_ram = rc.RAM_Frequency(f_ram)

    simulator.input['Clock'] = float(classificacao_clock_speed)
    simulator.input['Nucleo'] = float(classificacao_cores)
    simulator.input['RAM'] = float(classificacao_frequencia_ram)

    simulator.compute()

    # Accessa as variáveis de saída
    result_CPU = simulator.output['Result CPUxRAM']
    #print("Resultado:", result_CPU)

    return result_CPU



