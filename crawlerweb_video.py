import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


def get_video_card_info(url):

    # URL do site do PassMark com o nome da placa de vídeo
    url = f"https://www.videocardbenchmark.net/{url}"

    # Envia a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        
        # Faz o parsing do HTML da página
        soup = BeautifulSoup(response.content, "html.parser")

        # Obtém o texto completo da página
        page_text = soup.get_text()
        
        # Retorna o nome completo da placa de video desejada
        span = soup.find('span', class_='cpuname')
        
        # Nome retornado d
        name_video_card = span.text
        
        #print(f"\n\n{name_video_card}:\n")

        # Procura pelas informações de clock base e VRAM no texto completo da página
        if "Core Clock(s):" in page_text:
            base_clock_start = page_text.index("Core Clock(s):") + len("Core Clock(s):")
            base_clock_end = page_text.index("MHz", base_clock_start)
            base_clock = page_text[base_clock_start:base_clock_end].strip()
            print(f"Core Clock(s): {base_clock} MHz")
            
            
            # Classifica se o core clock é alto, médio ou baixo
            coreclock_int = int(base_clock.split()[0])
            if coreclock_int > 1500:
                classificacao_core_clock = "Alto"
            elif coreclock_int >= 1000 and coreclock_int <= 1500:
                classificacao_core_clock = "Médio"
            else:
                classificacao_core_clock = "Baixo"
   
            print(f"Classificação do Core Clock: {classificacao_core_clock}\n")
            
        else:
            print("Não foi possível encontrar a informação de Clock Base.")

        if "Max Memory Size:" in page_text:
            vram_start = page_text.index("Max Memory Size:") + len("Max Memory Size:")
            vram_end = page_text.index("MB", vram_start)
            vram = page_text[vram_start:vram_end].strip()
            print(f"VRAM: {vram} MB")
            
            
            # Classifica se o size da memoria é alto, médio ou baixo
            vram_int = int(vram)
            if vram_int > 6144:
                classificacao_memory_size = "Alto"
            elif vram_int >= 2048 and vram_int <= 6144:
                classificacao_memory_size = "Médio"
            else:
                classificacao_memory_size = "Baixo"
                
            print(f"Classificação da Memory Size: {classificacao_memory_size}\n") 
            
            
        else:
            print("Não foi possível encontrar a informação de VRAM.")
    else:
        print("Falha ao obter a página do PassMark.")
        
    return base_clock, vram


def return_id():
    video_card = input('Digite o nome da placa de vídeo: ')
    video_card_formatted = video_card.replace(" ", "+")

    is_laptop = "laptop" in video_card.lower()

    # Faz a requisição para o site
    url = 'https://www.videocardbenchmark.net/directCompute.html'
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
        if video_card_formatted in href:
            results.add(href)  # Adiciona apenas se não existir na lista

    return list(results)  # Converte o conjunto de volta para uma lista


def opcions(results):
    for i, result in enumerate(results):
        parsed_url = urlparse(result)
        query_parameters = parse_qs(parsed_url.query)
        gpu_name = query_parameters.get('gpu')[0]
        vid = query_parameters.get('id')[0]
        print(f"{i}): {gpu_name} - {vid}")
        
    op = int(input('\nDigite o número da opção desejada: '))
    url = results[op]
    
    return url
    
