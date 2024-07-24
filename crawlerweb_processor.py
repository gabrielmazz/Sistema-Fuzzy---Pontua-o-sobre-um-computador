import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs

def get_processor_info(url):

    # URL do site do PassMark com o nome do processador
    url = f"https://www.cpubenchmark.net/{url}"
    
    # Envia a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        
        # Faz o parsing do HTML da página
        soup = BeautifulSoup(response.content, "html.parser")

        # Obtém o texto completo da página
        page_text = soup.get_text()
        
        # Retorna o nome completo do processor desejado
        span = soup.find('span', class_='cpuname')
        
        # Nome retornado do processador
        name_processor = span.text
        
        #print(f"\n\n{name_processor}:\n")

        # Procura pelas informações de clock do processador e de quantos cores com suas threads, isso no texto completo da página
        if "Clockspeed:" in page_text:
            clock_start = page_text.index("Clockspeed:") + len("Clockspeed:")
            clock_end = page_text.index("GHz", clock_start)
            base_clock = page_text[clock_start:clock_end].strip()
            print(f"Clockspeed: {base_clock} GHz")
            
            # Adiciona ao arquivo a informação do clockspeed do processador
            #arq.write(base_clock+"\n")
            
            # Classifica se o clock é alto, médio ou baixo
            clockspeed_float = float(base_clock.split()[0])  # Extrai o valor numérico do clockspeed e converte para float
            if clockspeed_float > 3.5:
                classificacao_clock_speed = "Alto"
            elif clockspeed_float >= 2 and clockspeed_float <= 3.5:
                classificacao_clock_speed = "Médio"
            else:
                classificacao_clock_speed = "Baixo"
                
            print(f"Classificação do Clock Speed: {classificacao_clock_speed}\n")
            
        else:
            print("Não foi possível encontrar a informação de Clock Base.")

        if "Cores:" in page_text:
            cores_start = page_text.index("Cores:") + len("Cores:")
            cores_end = page_text.index("Typical", cores_start)
            cores_text = page_text[cores_start:cores_end].strip()
            print(f"Cores: {cores_text}")
            
            # Procura a posição do número 6 na lista de palavras
            indice = cores_text.index('Threads:')

            # Mantém apenas as palavras até o índice do número 6
            cores_text = ' '.join(cores_text[:indice])
            
            # Adiciona ao arquivo a informação dos cores do processador
            #arq.write(cores_text+"\n")
            
            # re.search() juntamente com a expressão regular r"\d+" para encontrar o primeiro valor numérico na string cores_text
            match = re.search(r"\d+", cores_text)  # Encontra o primeiro valor numérico na string

            if match:
                cores = int(match.group())  # Converte o valor numérico para inteiro
            
            if cores > 4:
                classificacao_cores = "Alto"
            elif cores >= 2 and cores <= 4:
                classificacao_cores = "Médio"
            else:
                classificacao_cores = "Baixo"
            print(f"Classificação dos Cores: {classificacao_cores}")
        
        else:
            print("Não foi possível encontrar a informação de Cores.")

    else:
        print("Falha ao obter a página do PassMark.")
        
    return cores_text, base_clock


def return_id():
    processor_card = input('Digite o nome do processador: ')
    processor_card_formatted = processor_card.replace(" ", "+")

    # Faz a requisição para o site
    url = 'https://www.cpubenchmark.net/cpu_lookup.php?cpu=Intel+Core+i5-11400H+%40+2.70GHz&id=4457'
    response = requests.get(url)

    # Analisa o conteúdo HTML da página usando o BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra todos os elementos <a> que contêm o atributo href
    links = soup.find_all('a')

    # Conjunto para armazenar os resultados
    results = set()  # Usando um conjunto para evitar duplicatas

    # Extrai o valor do atributo href de cada link
    for link in links:
        href = link.get('href')
        if processor_card_formatted in href:
            results.add(href)  # Adiciona apenas se não existir na lista

    return list(results)  # Converte o conjunto de volta para uma lista


def opcions(results):
    for i, result in enumerate(results):
        parsed_url = urlparse(result)
        query_parameters = parse_qs(parsed_url.query)
        processor_name = query_parameters.get('cpu')[0]
        pid = query_parameters.get('id')[0]
        print(f"{i}): {processor_name} - {pid}")

    op = int(input('\nDigite o número da opção desejada: '))
    url = results[op]
    return url
    
