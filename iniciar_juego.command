#!/bin/bash
# Iniciar servidor local para "Chile en el Tiempo"
cd "$(dirname "$0")"
echo "Iniciando servidor para Chile en el Tiempo..."
echo "Abriendo en el navegador: http://localhost:8080"
open "http://localhost:8080"
python3 -m http.server 8080
