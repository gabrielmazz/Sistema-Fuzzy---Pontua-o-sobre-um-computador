def RAM(ram):
    if ram <= 4:
        classificacao_ram = "Baixa"
    elif ram > 4 and ram <= 8:
        classificacao_ram = "Média"
    else:
        classificacao_ram = "Alta"

    print(f"Classificação da RAM: {classificacao_ram}\n")
    
    return ram

def RAM_Frequency(f_ram):
    if f_ram < 1600:
        classificacao_frequencia_ram = "Baixa"
    elif f_ram >= 1600 and f_ram < 3200:
        classificacao_frequencia_ram = "Média"
    else:
        classificacao_frequencia_ram = "Alta"
        
    print(f"Classificação da Frequência da RAM: {classificacao_frequencia_ram}\n")
    
    return f_ram