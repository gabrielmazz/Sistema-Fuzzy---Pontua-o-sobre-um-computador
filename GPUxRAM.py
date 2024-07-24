#Código do matlab em python
import crawlerweb_video as cv
import ram_choice as rc
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def result_GPURAM():
    # Criação das variáveis de entrada e saída
    g_clock = ctrl.Antecedent(np.arange(0, 3500, 1), 'G_Clock')
    vram = ctrl.Antecedent(np.arange(0, 12, 0.1), 'VRAM')
    ram = ctrl.Antecedent(np.arange(2, 128, 0.1), 'RAM')
    result = ctrl.Consequent(np.arange(0, 100, 0.1), 'Result_GPUxRAM')

    # Definição das funções de pertinência
    # trimf = aceita decimais
    g_clock['Baixo'] = fuzz.trimf(g_clock.universe, [-1458.33, 0, 1500])
    g_clock['Médio'] = fuzz.trimf(g_clock.universe, [500, 1750, 2500])
    g_clock['Alto'] = fuzz.trimf(g_clock.universe, [2000, 3500, 5000])

    vram['Baixo'] = fuzz.trapmf(vram.universe, [-4, 0, 2, 4])
    vram['Médio'] = fuzz.trapmf(vram.universe, [2, 4, 6, 8])
    vram['Alto'] = fuzz.trapmf(vram.universe, [6, 8, 12, 16])

    ram['Baixo'] = fuzz.trapmf(ram.universe, [-4, 0, 2, 4])
    ram['Médio'] = fuzz.trapmf(ram.universe, [2, 4, 8, 12])
    ram['Alto'] = fuzz.trapmf(ram.universe, [8, 12, 64, 128])

    result['Péssimo'] = fuzz.trimf(result.universe, [-20.8333333333333, 0, 20.8333333333333])
    result['Mínimo'] = fuzz.trimf(result.universe, [4.16666666666667, 25, 45.8333333333333])
    result['Médio'] = fuzz.trimf(result.universe, [29.1666666666667, 50, 70.8333333333333])
    result['Bom'] = fuzz.trimf(result.universe, [54.1666666666667, 75, 95.8333333333333])
    result['Muito Bom'] = fuzz.trimf(result.universe, [79.1666666666667, 100, 120.833333333333])
    

    # Cria as regras
    rules = [
        ctrl.Rule(g_clock['Alto'] & vram['Alto'] & ram['Alto'], result['Muito Bom']),
        ctrl.Rule(g_clock['Alto'] & vram['Alto'] & ram['Médio'], result['Bom']),
        ctrl.Rule(g_clock['Alto'] & vram['Alto'] & ram['Baixo'], result['Médio']),
        ctrl.Rule(g_clock['Alto'] & vram['Médio'] & ram['Alto'], result['Bom']),
        ctrl.Rule(g_clock['Alto'] & vram['Médio'] & ram['Médio'], result['Médio']),
        ctrl.Rule(g_clock['Alto'] & vram['Médio'] & ram['Baixo'], result['Mínimo']),
        ctrl.Rule(g_clock['Alto'] & vram['Baixo'] & ram['Alto'], result['Médio']),
        ctrl.Rule(g_clock['Alto'] & vram['Baixo'] & ram['Médio'], result['Mínimo']),
        ctrl.Rule(g_clock['Alto'] & vram['Baixo'] & ram['Baixo'], result['Péssimo']),
        ctrl.Rule(g_clock['Médio'] & vram['Alto'] & ram['Alto'], result['Bom']),
        ctrl.Rule(g_clock['Médio'] & vram['Alto'] & ram['Médio'], result['Médio']),
        ctrl.Rule(g_clock['Médio'] & vram['Alto'] & ram['Baixo'], result['Mínimo']),
        ctrl.Rule(g_clock['Médio'] & vram['Médio'] & ram['Alto'], result['Médio']),
        ctrl.Rule(g_clock['Médio'] & vram['Médio'] & ram['Médio'], result['Mínimo']),
        ctrl.Rule(g_clock['Médio'] & vram['Médio'] & ram['Baixo'], result['Péssimo']),
        ctrl.Rule(g_clock['Médio'] & vram['Baixo'] & ram['Alto'], result['Mínimo']),
        ctrl.Rule(g_clock['Médio'] & vram['Baixo'] & ram['Médio'], result['Péssimo']),
        ctrl.Rule(g_clock['Médio'] & vram['Baixo'] & ram['Baixo'], result['Péssimo']),
        ctrl.Rule(g_clock['Baixo'] & vram['Alto'] & ram['Alto'], result['Médio']),
        ctrl.Rule(g_clock['Baixo'] & vram['Alto'] & ram['Médio'], result['Mínimo']),
        ctrl.Rule(g_clock['Baixo'] & vram['Alto'] & ram['Baixo'], result['Péssimo']),
        ctrl.Rule(g_clock['Baixo'] & vram['Médio'] & ram['Alto'], result['Mínimo']),
        ctrl.Rule(g_clock['Baixo'] & vram['Médio'] & ram['Médio'], result['Péssimo']),
        ctrl.Rule(g_clock['Baixo'] & vram['Médio'] & ram['Baixo'], result['Péssimo']),
        ctrl.Rule(g_clock['Baixo'] & vram['Baixo'] & ram['Alto'], result['Péssimo']),
        ctrl.Rule(g_clock['Baixo'] & vram['Baixo'] & ram['Médio'], result['Péssimo']),
        ctrl.Rule(g_clock['Baixo'] & vram['Baixo'] & ram['Baixo'], result['Péssimo'])
    ]

    # Cria o sistema de controle
    system = ctrl.ControlSystem(rules)
    simulation = ctrl.ControlSystemSimulation(system)

    # Solicita o nome da placa de vídeo ao usuário
    results_cv = cv.return_id()

    # Solicita o choice da placa de vídeo ao usuário
    url  = cv.opcions(results_cv)

    # Chama a função para obter as informações da placa de vídeo
    classificacao_core_clock, classificacao_memory_size = cv.get_video_card_info(url)

    ram = int(input("\n\nDiga a quantidade de RAM: "))

    # Chama a função que define a classificação da ram
    classificacao_ram = rc.RAM(ram)

    # Define os valores de entrada
    simulation.input['G_Clock'] = float(classificacao_core_clock)
    simulation.input['VRAM'] = float(classificacao_memory_size)
    simulation.input['RAM'] = float(classificacao_ram)

    # Avalia o sistema de controle
    simulation.compute()

    # Obtém o resultado
    resultado_GPU = simulation.output['Result_GPUxRAM']
    #print("Resultado: ", resultado_GPU)

    return resultado_GPU