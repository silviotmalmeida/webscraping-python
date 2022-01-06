# importando as dependências
import requests  # biblioteca de requisições http
from bs4 import BeautifulSoup  # biblioteca de tratamento de html
import subprocess  # biblioteca de comandos do sistema
import os  # biblioteca de manipulação de pastas
import shutil  # biblioteca de manipulação de pastas

# url principal do mangá na Union Mangás
main_url = 'http://unionleitor.top/pagina-manga/shingeki-no-kyojin'

# obtendo a pasta do projeto
project_folder = os.path.dirname(os.path.realpath(__file__))

# nomeando a pasta de saída dos arquivos
files_folder = 'files'

# definindo o capítulo inicial a ser baixado
initial_chapter = 1

# definindo o capítulo final a ser baixado
final_chapter = 1

# tratamento de exceções
try:

    # se a pasta de arquivos ainda não existir, será criada
    if not os.path.isdir(f'{project_folder}/{files_folder}'):
        os.mkdir(f'{project_folder}/{files_folder}')

    # fazendo a requisição na url principal
    response = requests.get(main_url)

    # tratando o html recebido
    html = BeautifulSoup(response.text, 'html.parser')

    # iniciando o dicionário que armazenará os pares { pasta : url interna }
    folder_url = {}

    # coletando todas as tag <a> da url principal
    for url in html.select('a'):

        # se o texto da tag possuir os caracteres 'Cap. ', corresponde a um capítulo
        if 'Cap. ' in url.text:

            # nomeando a pasta do capítulo a partir do texto da tag
            chapter_folder = float(url.text[5:])

            # obtendo o url do capítulo a partir do atributo href
            chapter_url = url.get('href')

            # populando o dicionário com a pasta e a url do capítulo
            folder_url[chapter_folder] = chapter_url

    # percorrendo o dicionário ordenado pelo capítulo
    for chapter_folder, chapter_url in sorted(folder_url.items()):

        # se o número da capítulo estiver entre o intervalo especificado, prossegue
        if chapter_folder >= initial_chapter and chapter_folder <= final_chapter:

            # fazendo a requisição na url do capítulo
            response = requests.get(chapter_url)

            # tratando o html recebido
            html = BeautifulSoup(response.text, 'html.parser')

            # se já existir uma pasta com o mesmo nome do capítulo, remove a mesma
            if os.path.isdir(f'{project_folder}/{files_folder}/{chapter_folder}'):
                shutil.rmtree(
                    f'{project_folder}/{files_folder}/{chapter_folder}')

            # criando a pasta do capítulo
            os.mkdir(f'{project_folder}/{files_folder}/{chapter_folder}')

            # coletando todas as tag <img> da url do capítulo
            for image in html.select('img'):

                # obtendo a url da imagem a partir do atributo src
                image_url = image.get('src')

                # definindo a página da imagem a partir do atributo pag, e configurando com 3 dígitos
                image_page = image.get('pag').zfill(3)

                # utilizando o wget para realizar o download da imagem
                subprocess.call(
                    f"wget -O '{project_folder}/{files_folder}/{chapter_folder}/{image_page}' '{image_url}'", shell=True)

# em caso de erro:
except Exception as error:

    # exibe a mensagem
    print(f"Ocorreu um erro: {error}")

    # encerra a execução do script
    exit()
