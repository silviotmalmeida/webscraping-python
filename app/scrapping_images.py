import requests
from bs4 import BeautifulSoup
import subprocess

url = 'http://unionleitor.top/leitor/Shingeki_no_Kyojin/01'
files_folder = '/root/files/'


try:
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')

    for image in html.select('img'):

        image_url = image.get('src')
        image_name = image_url[-7:]

        print(files_folder + image_name)

        # cmd = [ 'wget', files_folder + image_name, image_url]

        # cmd = []

        subprocess.call(f"wget -O '{files_folder + image_name}' '{image_url}'", shell=True)

except Exception as error:
        print(f"Erro no processamento dos dados: {error}")
        exit()