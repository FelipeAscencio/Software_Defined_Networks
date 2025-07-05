#!/bin/bash

# Script que lanza Mininet con una topología personalizada definida en 'mininet.py'.
# Usa la topología llamada 'topologia_cadena' con la cantidad de switches indicada como argumento ($1).
# Se habilita el uso de direcciones MAC y ARP, se selecciona Open vSwitch como switch,
# y se configura un controlador remoto externo.

# Validar los argumentos.
if [ -z "$1" ]; then
  echo "Uso: $0 <cantidad_de_switches>"
  exit 1
fi

# Limpiar cualquier instancia previa de Mininet
sudo mn -c

# Ejecutar Mininet con el número de switches dado
sudo mn --custom mininet.py --topo=topologia_cadena,$1 --mac --arp --switch ovsk --controller remote
