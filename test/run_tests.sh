#!/bin/bash

host="localhost"

echo "Starting tests..."
sleep 1

sleep 2
echo "Adding new document"
curl -X POST http://$host:5000/insert \
-H "Content-Type: application/json" \
-d '{"cpf_cnpj": "30.607.887/0001-41", "name": "Alphadale Curtis"}'
echo " "

sleep 2
echo "Adding document that already exists"
curl -X POST http://$host:5000/insert \
-H "Content-Type: application/json" \
-d '{"cpf_cnpj": "30.607.887/0001-41", "name": "Alphadale Curtis"}'
echo " "

sleep 2
echo "loading several documents"
curl -X POST http://$host:5000/load-file \
-H "Content-Type: multipart/form-data" \
-F "file=@/data/Base_Dados_Teste.csv"
echo " "

sleep 2
echo "Getting system status"
curl "http://$host:5000/status"
echo " "

sleep 2
echo "Performing few searches"
sleep 1
curl "http://$host:5000/search?cpf_cnpj=78.355.355/0001-90&name=hess"
sleep 1
curl "http://$host:5000/search?cpf_cnpj=78.355.355/0001-90"
sleep 2
curl "http://$host:5000/search?name=Alphadale"
echo " "

sleep 2
echo "Getting system status"
curl "http://$host:5000/status"
echo " "

echo "finished tests"
sleep 2
echo "exiting..."
sleep 3