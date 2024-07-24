import CPUxRAM as cr
import GPUxRAM as gr
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Inputs
gpu = ctrl.Antecedent(np.arange(0, 101, 1), 'GPU')
cpu = ctrl.Antecedent(np.arange(0, 101, 1), 'CPU')

# Outputs
resultado = ctrl.Consequent(np.arange(0, 101, 1), 'resultado')


# Funções de Pertinência
gpu['Pessimo'] = fuzz.trimf(gpu.universe, [-20.8333333333333, 0, 20.8333333333333])
gpu['Baixo'] = fuzz.trimf(gpu.universe, [4.16666666666667, 25, 45.8333333333333])
gpu['Medio'] = fuzz.trimf(gpu.universe, [29.1666666666667, 50, 70.8333333333333])
gpu['Bom'] = fuzz.trimf(gpu.universe, [54.1666666666667, 75, 95.8333333333333])
gpu['Muito Bom'] = fuzz.trimf(gpu.universe, [79.1666666666667, 100, 120.833333333333])

cpu['Pessimo'] = fuzz.trimf(cpu.universe, [-20.8333333333333, 0, 20.8333333333333])
cpu['Baixo'] = fuzz.trimf(cpu.universe, [4.16666666666667, 25, 45.8333333333333])
cpu['Medio'] = fuzz.trimf(cpu.universe, [29.1666666666667, 50, 70.8333333333333])
cpu['Bom'] = fuzz.trimf(cpu.universe, [54.1666666666667, 75, 95.8333333333333])
cpu['Muito Bom'] = fuzz.trimf(cpu.universe, [79.1666666666667, 100, 120.833333333333])

resultado['Pessimo'] = fuzz.trimf(resultado.universe, [-20.8333333333333, 0, 20.8333333333333])
resultado['Baixo'] = fuzz.trimf(resultado.universe, [4.16666666666667, 25, 45.8333333333333])
resultado['Medio'] = fuzz.trimf(resultado.universe, [29.1666666666667, 50, 70.8333333333333])
resultado['Bom'] = fuzz.trimf(resultado.universe, [54.1666666666667, 75, 95.8333333333333])
resultado['Muito Bom'] = fuzz.trimf(resultado.universe, [79.1666666666667, 100, 120.833333333333])

# Regras
rules = [
    ctrl.Rule(gpu['Muito Bom'] & cpu['Muito Bom'], resultado['Muito Bom']),
    ctrl.Rule(gpu['Muito Bom'] & cpu['Bom'], resultado['Muito Bom']),
    ctrl.Rule(gpu['Muito Bom'] & cpu['Medio'], resultado['Muito Bom']),
    ctrl.Rule(gpu['Muito Bom'] & cpu['Baixo'], resultado['Muito Bom']),
    ctrl.Rule(gpu['Muito Bom'] & cpu['Pessimo'], resultado['Muito Bom']),
    ctrl.Rule(gpu['Bom'] & cpu['Muito Bom'], resultado['Muito Bom']),
    ctrl.Rule(gpu['Bom'] & cpu['Bom'], resultado['Bom']),
    ctrl.Rule(gpu['Bom'] & cpu['Medio'], resultado['Medio']),
    ctrl.Rule(gpu['Bom'] & cpu['Baixo'], resultado['Baixo']),
    ctrl.Rule(gpu['Bom'] & cpu['Pessimo'], resultado['Pessimo']),
    ctrl.Rule(gpu['Medio'] & cpu['Muito Bom'], resultado['Muito Bom']),
    ctrl.Rule(gpu['Medio'] & cpu['Bom'], resultado['Medio']),
    ctrl.Rule(gpu['Medio'] & cpu['Medio'], resultado['Medio']),
    ctrl.Rule(gpu['Medio'] & cpu['Baixo'], resultado['Baixo']),
    ctrl.Rule(gpu['Medio'] & cpu['Pessimo'], resultado['Pessimo']),
    ctrl.Rule(gpu['Baixo'] & cpu['Muito Bom'], resultado['Muito Bom']),
    ctrl.Rule(gpu['Baixo'] & cpu['Bom'], resultado['Baixo']),
    ctrl.Rule(gpu['Baixo'] & cpu['Medio'], resultado['Baixo']),
    ctrl.Rule(gpu['Baixo'] & cpu['Baixo'], resultado['Baixo']),
    ctrl.Rule(gpu['Baixo'] & cpu['Pessimo'], resultado['Pessimo']),
    ctrl.Rule(gpu['Pessimo'] & cpu['Muito Bom'], resultado['Muito Bom']),
    ctrl.Rule(gpu['Pessimo'] & cpu['Bom'], resultado['Pessimo']),
    ctrl.Rule(gpu['Pessimo'] & cpu['Medio'], resultado['Pessimo']),
    ctrl.Rule(gpu['Pessimo'] & cpu['Baixo'], resultado['Pessimo']),
    ctrl.Rule(gpu['Pessimo'] & cpu['Pessimo'], resultado['Pessimo'])
]

# Criação do sistema de controle
system = ctrl.ControlSystem(rules)

# Criação do simulador
simulator = ctrl.ControlSystemSimulation(system)


resultado_CPU = cr.result_CPURAM()
resultado_GPU = gr.result_GPURAM()


# Set inputs
simulator.input['GPU'] = resultado_GPU
simulator.input['CPU'] = resultado_CPU

# Computa os resultados
simulator.compute()

# Acessa a variável de saída
result = simulator.output['resultado']
print("Resultado Final:", result)

