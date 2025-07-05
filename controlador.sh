# Script que lanza el controlador POX con los módulos necesarios.
# - Establece el nivel de log en DEBUG para ver mensajes detallados.
# - Usa el módulo 'forwarding.l2_learning' para aprendizaje de capa 2.
# - Ejecuta el módulo personalizado 'controller' donde se define la lógica del firewall.

pox/pox.py log.level --DEBUG forwarding.l2_learning controller
