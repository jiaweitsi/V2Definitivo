from airport import *
import matplotlib.pyplot as plt
import math

class Aircraft:
    def __init__(self, aircraft, company, origin, time):
        self.aircraft= aircraft #string
        self.company= company #3 letras ICAO code
        self.origin= origin #4 letras ICAO code
        self.time= time #formato hh:mm

# ===== LOAD ARRIVALS =====

def LoadArrivals(filename):
    lista_arrivals= []
    try:
        f= open(filename,"r")
        lineas = f.readlines()
        f.close()

        i=1
        while i < len(lineas):
            partes = lineas[i].split()
            if len(partes)==4:
                aircraft = partes[0]
                origin = partes[1]
                time = partes[2]
                company = partes[3]
                if ':' in time:
                    nuevo= Aircraft(aircraft, company, origin, time)
                    lista_arrivals.append(nuevo)
            i=i+1

    except FileNotFoundError:
        print("No se encontro el archivo:", filename)
        return []
    return lista_arrivals

# ===== PLOT ARRIVALS =====

def PlotArrivals(aircrafts):

    if len(aircrafts) == 0:
        print("No existeix la llista")
        return

    Vx = range(24)  # hores
    Vy = [0] * 24  # arribades/hora
    i = 0
    while i < len(aircrafts):
        fila = aircrafts[i]
        tiempo= fila.time
        partes = tiempo.split(":")

        hlanding = int(partes[0])

        Vy[hlanding] = Vy[hlanding] + 1
        i = i + 1

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(Vx, Vy, color='skyblue', edgecolor='black')
    ax.set_title("Frecuencia de aterrizajes por hora")
    ax.set_ylabel("Número de aviones")
    ax.set_xlabel("Hora del día")
    ax.set_xticks(range(0, 24))

    return fig

# ===== SAVE FLIGHTS  =====

def SaveFlights(aircrafts, filename):
    if len(aircrafts) == 0:
        print("No existeix la llista")
        return False
    try:
        out = open(filename, 'w')
        out.write("Aircraft\tOrigin\tTime\tCompany\n")
        i = 0
        while i < len(aircrafts):
            fila = aircrafts[i]

            aircraft = fila.aircraft
            origin = fila.origin
            arrival = fila.time
            airline = fila.company

            if aircraft == "":
                aircraft = "-"
            if origin == "":
                origin = "-"
            if arrival == "":
                arrival = "-"
            if airline == "":
                airline = "-"
            out.write(aircraft + "\t" + origin + "\t" + arrival + "\t" + airline + "\n")

            i = i + 1

        out.close()
        return True
    except:
        print("No se pudo guardar el archivo")
        return False

# ===== PLOT AIRLINES =====

def PlotAirlines(aircrafts):
        if len(aircrafts) == 0:
            print("No existeix la llista")
            return

        Vx = []  # aerolinies
        Vy = []  # nº vols
        i = 0
        while i < len(aircrafts):
            fila = aircrafts[i]
            airline = fila.company
            if airline not in Vx:
                Vx.append(airline)
                Vy.append(1)
            else:
                encontrado = False
                x = 0
                while not encontrado and x < len(Vx):
                    if Vx[x] == airline:
                        encontrado = True
                    else:
                        x = x + 1
                if encontrado:
                    Vy[x] = Vy[x] + 1
            i=i+1

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.bar(Vx, Vy, color='orange')
        ax.set_xlabel("Aerolíneas")
        ax.set_ylabel("Número de vuelos")
        ax.set_title("Vuelos por Compañía")

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

# ===== PLOT FLIGHTS TYPE (SCHENGEN VS NO SCHENGEN) =====

def PlotFlightsType(aircrafts):

    if len(aircrafts) > 0:
        schengen = 0
        no_schengen = 0

        schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
                    'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

        i = 0
        while i < len(aircrafts):
            fila = aircrafts[i]
            origen = fila.origin
            inicio = origen[0:2]
            encontrado = False
            j = 0
            while j < len(schengen_codes) and not encontrado:
                if schengen_codes[j] == inicio:
                    encontrado = True
                else:
                    j = j + 1

            # CORREGIDO: antes ponía "if schengen == True" (comparaba el contador, no el bool)
            if encontrado == True:
                schengen = schengen + 1
            else:
                no_schengen = no_schengen + 1

            i = i + 1

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.bar(['Schengen', 'No Schengen'], [schengen, no_schengen], color=['blue', 'red'])

        ax.set_title("Vuelos Schengen vs No Schengen")
        ax.set_ylabel("Cantidad de vuelos")

        return fig
    else:
        return None

# ===== MAP FLIGHTS (GOOGLE EARTH: lINIAS) =====

def MapFlights(lista_arrivals, lista_airports):

    f = open("trayectorias.kml", "w")

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')

    # Color verde Schengen
    f.write('<Style id="schengen">\n')
    f.write('<LineStyle>\n')
    f.write('<color>ff00ff00</color>\n')
    f.write('<width>3</width>\n')
    f.write('</LineStyle>\n')
    f.write('</Style>\n')

    # Color rojo no Schengen
    f.write('<Style id="normal">\n')
    f.write('<LineStyle>\n')
    f.write('<color>ff0000ff</color>\n')
    f.write('<width>3</width>\n')
    f.write('</LineStyle>\n')
    f.write('</Style>\n')

    lat_dest = 41.297445
    lon_dest = 2.0832941

    schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
                      'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

    i = 0

    while i < len(lista_arrivals):

        vuelo = lista_arrivals[i]
        codigo_de_donde_viene = vuelo.origin
        aeropuerto_encontrado = None

        j = 0
        while j < len(lista_airports):
            if lista_airports[j].code == codigo_de_donde_viene:
                aeropuerto_encontrado = lista_airports[j]
            j = j + 1

        if aeropuerto_encontrado != None:
            # Mirar si es Schengen
            estilo = "normal"
            k = 0
            while k < len(schengen_codes):
                if vuelo.origin[0:2] == schengen_codes[k]:
                    estilo = "schengen"
                k = k + 1

            f.write('<Placemark>\n')
            f.write('  <name>' + vuelo.aircraft + ' desde ' + vuelo.origin + '</name>\n')
            f.write('  <styleUrl>#' + estilo + '</styleUrl>\n')
            f.write('  <LineString>\n')
            f.write('    <coordinates>\n')

            # Coordenadas bien escritas
            f.write('      ' +
                    str(aeropuerto_encontrado.lon) + ',' +
                    str(aeropuerto_encontrado.lat) + ',0 ' +
                    str(lon_dest) + ',' +
                    str(lat_dest) + ',0\n')

            f.write('    </coordinates>\n')
            f.write('  </LineString>\n')
            f.write('</Placemark>\n')

        i = i + 1

    f.write('</Document>\n')
    f.write('</kml>\n')

    f.close()

    print("Archivo KML generado.")

# ===== LONG FLIGHT ARRIVALS =====

def LongFlightArrivals(aircrafts, lista_aeropuertos):
    vuelos_largos = []

    lat_bcn = 0
    lon_bcn = 0
    k = 0
    while k < len(lista_aeropuertos):
        if lista_aeropuertos[k].code == "LEBL":
            lat_bcn = lista_aeropuertos[k].lat
            lon_bcn = lista_aeropuertos[k].lon
        k = k + 1

    radio_tierra = 6371

    i = 0
    while i < len(aircrafts):
        vuelo = aircrafts[i]

        lat_origen = 0
        lon_origen = 0
        encontrado = False

        j = 0
        while j < len(lista_aeropuertos) and not encontrado:
            if lista_aeropuertos[j].code == vuelo.origin:
                lat_origen = lista_aeropuertos[j].lat
                lon_origen = lista_aeropuertos[j].lon
                encontrado = True
            j = j + 1

        if encontrado:
            phi1 = math.radians(lat_origen)
            phi2 = math.radians(lat_bcn)
            dphi = math.radians(lat_bcn - lat_origen)
            dlambda = math.radians(lon_bcn - lon_origen)

            a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distancia = radio_tierra * c

            if distancia > 2000:
                vuelos_largos.append(vuelo)

        i = i + 1

    return vuelos_largos



