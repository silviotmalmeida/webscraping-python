#!/bin/bash

echo ""
docker container exec -it webscrapping-python python3 /root/scrapping_mangalivre.py

sleep 1

echo "Definindo permissoes da pasta de código-fonte..."
docker container exec webscrapping-python chmod 777 -R /root
sleep 1

echo "Processo concluído."
