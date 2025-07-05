# Imports de bibliotecas de 'MININET'.
from mininet.topo import Topo

# Constantes.
HOST_1 = "h1"
HOST_2 = "h2"
HOST_3 = "h3"
HOST_4 = "h4"
PRIMER_SWITCH = 0
ULTIMO_SWITCH = -1
INDICE_INICIAL_ENLACE = 1
UNO = 1

# Definición de mensajes de error.
MENSAJE_ERROR_CANTIDAD_SWITCHES = "La cantidad de switches debe ser un número positivo."

# Clase que define una topología personalizada de Mininet con forma de cadena,
# donde los switches están conectados en serie y hay cuatro hosts distribuidos en los extremos.
class Cadena(Topo):

    # Constructor de la clase. Recibe la cantidad de switches como parámetro,
    # crea los hosts y switches, y establece los enlaces entre ellos.
    def __init__(self, cantidad_switches: int, **opts):
        super(self.__class__, self).__init__(self, opts)

        # Validamos que la cantidad de switches ingresada sea válida.
        if cantidad_switches < INDICE_INICIAL_ENLACE:
            raise ValueError(MENSAJE_ERROR_CANTIDAD_SWITCHES)

        # Añadimos los 4 hosts (h) a la topología.
        h1 = self.addHost(HOST_1)
        h2 = self.addHost(HOST_2)
        h3 = self.addHost(HOST_3)
        h4 = self.addHost(HOST_4)

        # Añadimos los 'n' switches (s) a la topología.
        switches = [self.addSwitch(f"s{i + UNO}") for i in range(cantidad_switches)]
        self.addLink(h1, switches[PRIMER_SWITCH])
        for i in range(INDICE_INICIAL_ENLACE, cantidad_switches):
            self.addLink(switches[i - UNO], switches[i])

        # Añadimos los últimos links restantes.
        self.addLink(h2, switches[PRIMER_SWITCH])
        self.addLink(h3, switches[ULTIMO_SWITCH])
        self.addLink(h4, switches[ULTIMO_SWITCH])

# Diccionario que registra la topología con un nombre identificador ('topologia_cadena'),
# necesario para que Mininet pueda reconocerla al ejecutarse con la opción '--topo'.
topos = {"topologia_cadena": Cadena}
