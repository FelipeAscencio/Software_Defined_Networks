# Imports de bibliotecas externas.
import json

# Imports de bibliotecas de 'POX'.
import pox.openflow.libopenflow_01 as protocolo_openflow
from pox.lib.addresses import EthAddr, IPAddr
from pox.lib.util import dpidToStr
from pox.lib.revent import *
from pox.core import core

# Definición de Constantes.
CODIGO_TCP = 6
CODIGO_UDP = 17
TIPO_IPv4 = 0x800
ARCHIVO_REGLAS = "reglas.json"

# Definición de mensajes para el 'Logger'.
MENSAJE_HABILITACION_FIREWALL = "Habilitando el Firewall."
MENSAJE_REGLAS_INSTALADAS = "Reglas del Firewall instaladas en {}"

# Inicializamos un logger personalizado para mostrar mensajes de depuración, información o errores durante la ejecución del controlador.
logger = core.getLogger()

# Clase que implementa un 'Firewall' definido por software utilizando 'POX' y 'OpenFlow'.
# Escucha los eventos de conexión de switches y aplica reglas de filtrado de tráfico según un archivo 'JSON' de configuración.
class Firewall(EventMixin):

    # Constructor de la clase. Registra el módulo para escuchar eventos de 'OpenFlow'
    # y carga las reglas de firewall desde un archivo JSON externo.
    def __init__(self):
        self.listenTo(core.openflow)
        self._rules = self.leer_reglas(ARCHIVO_REGLAS)
        logger.debug(MENSAJE_HABILITACION_FIREWALL)

    # Manejador del evento 'ConnectionUp', que se activa cuando un switch se conecta al controlador.
    # Recorre las reglas configuradas y aplica aquellas que correspondan al switch que generó el evento.
    def _handle_ConnectionUp(self, event):
        id_switch = event.dpid
        for regla in self._rules:
            if id_switch in regla["switches"]:
                self.aplicar_regla(event, regla)

        logger.debug(MENSAJE_REGLAS_INSTALADAS.format(dpidToStr(id_switch)))

    # Aplica una regla individual al switch que disparó el evento.
    # Construye un objeto de coincidencia (match) con los criterios definidos y
    # envía un mensaje de modificación de flujo para bloquear o permitir tráfico.
    def aplicar_regla(self, event, regla):
        criterio_match = protocolo_openflow.ofp_match()
        tipo_protocolo = {
            "tcp": CODIGO_TCP,
            "udp": CODIGO_UDP,
        }

        # Campos de reglas de la capa de transporte.
        if "puerto_origen" in regla:
            criterio_match.tp_src = regla["puerto_origen"]
        if "puerto_destino" in regla:
            criterio_match.tp_dst = regla["puerto_destino"]

        # Campos de reglas de la capa de red.
        if "ip_origen" in regla:
            criterio_match.nw_src = IPAddr(regla["ip_origen"])
        if "ip_destino" in regla:
            criterio_match.nw_dst = IPAddr(regla["ip_destino"])
        if "tipo_protocolo_transporte" in regla:
            criterio_match.nw_proto = tipo_protocolo[regla["tipo_protocolo_transporte"].lower()]

        # Campos de reglas de la capa de enlace.
        if "mac_origen" in regla:
            criterio_match.dl_src = EthAddr(regla["mac_origen"])
        if "mac_destino" in regla:
            criterio_match.dl_dst = EthAddr(regla["mac_destino"])

        # Solo se filtra tráfico IPv4.
        criterio_match.dl_type = TIPO_IPv4
        mensaje = protocolo_openflow.ofp_flow_mod()
        mensaje.match = criterio_match
        event.connection.send(mensaje)

    # Lee el archivo de configuración que contiene las reglas del firewall
    # y devuelve su contenido como una lista de diccionarios.
    def leer_reglas(self, ruta_archivo):
        print(ruta_archivo)
        with open(ruta_archivo) as archivo_json:
            return json.load(archivo_json)

# Punto de entrada del módulo. Registra e inicializa una instancia de la clase 'Firewall' dentro del núcleo de 'POX'.
def launch():
    core.registerNew(Firewall)
