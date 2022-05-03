#!/bin/bash

echo ""
docker container exec -it webscraping-python python3 /root/scraping_mangalivre.py

sleep 1

echo "Definindo permissoes da pasta de código-fonte..."
docker container exec webscraping-python chmod 777 -R /root
sleep 1

echo "Processo concluído."
