# script com função de baixar mangás no site mangalivre.net

# importando as dependências
# biblioteca de requisições http com suporte a javascript
from requests_html import HTMLSession
from bs4 import BeautifulSoup  # biblioteca de tratamento de html
import subprocess  # biblioteca de comandos do sistema
import os  # biblioteca de manipulação de pastas
import shutil  # biblioteca de manipulação de pastas
import re  # biblioteca de expressões regulares
from PIL import Image  # biblioteca para tratamento de imagens


# url principal do mangá na Mangá Livre
# main_url = 'https://mangalivre.net/manga/noblesse/296'
main_url = 'https://mangalivre.net/manga/solo-leveling/7702'

# obtendo a pasta do projeto
project_folder = os.path.dirname(os.path.realpath(__file__))

# nomeando a pasta de saída dos arquivos
files_folder = 'files'

# definindo o capítulo inicial a ser baixado
initial_chapter = 15

# definindo o capítulo final a ser baixado
final_chapter = 15

# tratamento de exceções
try:

    # se a pasta de arquivos ainda não existir, será criada
    if not os.path.isdir(f'{project_folder}/{files_folder}'):
        os.mkdir(f'{project_folder}/{files_folder}')

    # criando a sessão
    session = HTMLSession()

    # fazendo a requisição na url principal
    response = session.get(main_url)
    response.html.render(scrolldown=25, sleep=1, timeout=20)

    # se a requisição não retornar dados, lança uma exceção
    if not 200 == response.status_code:
        raise Exception(f'Falha na requisição, código {response.status_code}')

    # tratando o html recebido
    html = BeautifulSoup(response.html.html, 'html.parser')

    # fechando a conexão
    response.close()

    # fechando a sessão
    session.close()

    # iniciando o dicionário que armazenará os pares { pasta : url interna }
    folder_url = {}

    # coletando todas as tag <a> da url principal
    for url in html.select('a'):

        # se o atributo title da tag possuir os caracteres 'Ler Capitulo ', corresponde a um capítulo
        if url.get('title') != None and 'Ler Capítulo ' in url.get('title'):

            # nomeando a pasta do capítulo a partir do title da tag
            chapter_folder = (url.get('title')[13:]).zfill(9)

            # obtendo o url do capítulo a partir do atributo href
            chapter_url = f'http://mangalivre.net{url.get("href")}'

            # populando o dicionário com a pasta e a url do capítulo
            folder_url[chapter_folder] = chapter_url

    # percorrendo o dicionário ordenado pelo capítulo
    for chapter_folder, chapter_url in reversed(folder_url.items()):

        # obtendo o valor numérico do capítulo
        chapter_number = float(re.sub(r'[^0-9.]', '', chapter_folder))

        # se o número da capítulo estiver entre o intervalo especificado, prossegue
        if chapter_number >= initial_chapter and chapter_number <= final_chapter:

            # criando a sessão
            session = HTMLSession()

            # fazendo a requisição na url do capítulo
            response = session.get(chapter_url)
            response.html.render(timeout=20)

            # se a requisição não retornar dados, lança uma exceção
            if not 200 == response.status_code:
                raise Exception(f'Falha na requisição, código {response.status_code}')

            # tratando o html recebido
            html = BeautifulSoup(response.html.html, 'html.parser')

            # fechando a conexão
            response.close()

            # fechando a sessão
            session.close()
          
            # se já existir uma pasta com o mesmo nome do capítulo, remove a mesma
            if os.path.isdir(f'{project_folder}/{files_folder}/{chapter_folder}'):
                shutil.rmtree(
                    f'{project_folder}/{files_folder}/{chapter_folder}')

            # criando a pasta do capítulo
            os.mkdir(f'{project_folder}/{files_folder}/{chapter_folder}')

            # obtendo o número total de páginas do capítulo
            total_pages = html.select('em[reader-total-pages]')
            total_pages = int(total_pages[0].text)

            # fazendo as requisições das páginas do capítulo
            for image_page in range(total_pages):

                # criando a sessão
                session = HTMLSession()

                # fazendo a requisição na url do capítulo
                response = session.get(f'{chapter_url}#/!page{image_page}')
                response.html.render(timeout=60)

                # se a requisição não retornar dados, lança uma exceção
                if not 200 == response.status_code:
                    raise Exception(f'Falha na requisição, código {response.status_code}')

                # tratando o html recebido
                html = BeautifulSoup(response.html.html, 'html.parser')

                # fechando a conexão
                response.close()

                # fechando a sessão
                session.close()

                # obtendo o elemento da imagem da página
                image = html.select_one('img[referrerpolicy]')
                
                # obtendo a url da imagem a partir do atributo src
                image_url = image.get('src')

                # obtendo a extensão do arquivo
                image_extension = image_url.split('.')[-1]

                # utilizando o wget para realizar o download da imagem
                cmd = subprocess.run(
                    f"wget --tries=99 -O '{project_folder}/{files_folder}/{chapter_folder}/{str(image_page).zfill(9)}.{image_extension}' '{image_url}'", shell=True)

                # se ocorrer um erro, lança uma exceção
                if cmd.returncode != 0:
                    raise Exception(f'Erro baixando a imagem {image_url}')

                # abrindo a imagem original
                old_image = Image.open(
                    f'{project_folder}/{files_folder}/{chapter_folder}/{str(image_page).zfill(9)}.{image_extension}').convert('RGB')

                # obtendo as dimensões da imagem original
                width, height = old_image.size

                # definindo o width máximo da imagem
                new_width = 960

                # se a imagem original for maior:
                if width > new_width:

                    # calcula o novo height para manter a proporção
                    new_height = round((new_width*height)/width)

                    # cria uma nova imagem redimensionada
                    new_image = old_image.resize(
                        (new_width, new_height), Image.LANCZOS)

                # senão
                else:

                    # mantém as dimensões originais
                    new_image = old_image

                # salvando a nova imagem, otimizando a qualidade
                new_image.save(
                    f'{project_folder}/{files_folder}/{chapter_folder}/_{str(image_page).zfill(9)}.{image_extension}',
                    optimize=True,
                    quality=50
                )

                # apagando a imagem original
                cmd = subprocess.run(
                    f"rm -rf '{project_folder}/{files_folder}/{chapter_folder}/{str(image_page).zfill(9)}.{image_extension}'", shell=True)

                # se ocorrer um erro, lança uma exceção
                if cmd.returncode != 0:
                    raise Exception(
                        f'Erro apagando a imagem {project_folder}/{files_folder}/{chapter_folder}/{str(image_page).zfill(9)}.{image_extension}')

            # utilizando o imagemagick para realizar converter o capítulo em pdf
            cmd = subprocess.run(
                f"cd '{project_folder}/{files_folder}/{chapter_folder}/'; convert * '{chapter_folder}.pdf'", shell=True)

            # se ocorrer um erro, lança uma exceção
            if cmd.returncode != 0:
                raise Exception(
                    f'Erro convertendo o capítulo {chapter_folder}')

            # movendo o capítulo em pdf para a pasta de arquivos
            cmd = subprocess.run(
                f"mv '{project_folder}/{files_folder}/{chapter_folder}/{chapter_folder}.pdf' '{project_folder}/{files_folder}/{chapter_folder}.pdf'", shell=True)

            # se ocorrer um erro, lança uma exceção
            if cmd.returncode != 0:
                raise Exception(f'Erro movendo o capítulo {chapter_folder}')

            # apagando a pasta com as imagens
            cmd = subprocess.run(
                f"rm -rf '{project_folder}/{files_folder}/{chapter_folder}/'", shell=True)

            # se ocorrer um erro, lança uma exceção
            if cmd.returncode != 0:
                raise Exception(
                    f'Erro apagando a pasta {project_folder}/{files_folder}/{chapter_folder}')

            print(f'Arquivo {chapter_folder}.pdf pronto.\n')

# em caso de erro:
except Exception as error:

    # exibe a mensagem
    print(f"Ocorreu um erro. {error}")

    # encerra a execução do script
    exit()
