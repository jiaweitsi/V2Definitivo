import matplotlib.pyplot as plot
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Airport:
    def __init__(self, code, lat, lon):
        self.code = code
        self.lat = lat
        self.lon = lon
        self.schengen = False

# ===== IS SCHENGEN AIRPORT =====

def IsSchengenAirport(code):
    if code == "":
        return False

    schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
                'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

    inicio = code[0:2]
    i=0
    found=False
    while i < len(schengen_codes) and not found:
        if schengen_codes[i] == inicio:
            found=True
        else:
            i=i+1
    if found:
        return True
    else:
        return False


def SetSchengen(airport):
    if IsSchengenAirport(airport.code):
        airport.schengen = True
    else:
        airport.schengen = False

def PrintAirport(airport):
    print('ICAO:', airport.code)
    print('Latitude:', airport.lat)
    print('Longitude:', airport.lon)
    print('Schengen:', airport.schengen)


def ConvertirCordinadas(cord_str):
    sentido = cord_str[0]

    grados = float(cord_str[1:3])
    minutos = float(cord_str[3:5])
    segundos = float(cord_str[5:7])

    decimal = grados + (minutos / 60.0) + (segundos / 3600.0)

    if sentido == 'S' or sentido == 'W':
        decimal = decimal * -1

    return decimal

# ===== LOAD AIRPORTS =====
def LoadAirports(filename):
    lista_airports = []
    try:
        archivo = open(filename, "r")
        lineas = archivo.readlines()
        archivo.close()

        for i in range(1, len(lineas)):
            partes = lineas[i].split()
            if len(partes) >= 3:
                codigo = partes[0]

                latitud_decimal = ConvertirCordinadas(partes[1])
                longitud_decimal = ConvertirCordinadas(partes[2])

                nuevo = Airport(codigo, latitud_decimal, longitud_decimal)
                lista_airports.append(nuevo)
    except:
        return []
    return lista_airports

# ===== SAVE SCHENGEN AIRPORTS =====

def SaveSchengenAirports(airports, filename):
    if len(airports) == 0:
        return "Error:Lista vacia"

    f = open(filename, "w")
    f.write("CODE LAT LON\n")

    i = 0
    n = len(airports)
    while i < n:
        a = airports[i]
        SetSchengen(a)
        if a.schengen == True:
            f.write(a.code)
            f.write(" ")
            f.write(str(a.lat))
            f.write(" ")
            f.write(str(a.lon))
            f.write("\n")
        i = i + 1
    f.close()

# ===== ADD AIRPORT =====

def AddAirport(airports, airport):
    i = 0
    encontrado = False
    n = len(airports)

    while i < n and encontrado == False:
        if airports[i].code == airport.code:
            encontrado = True
        else:
            i = i + 1
    if encontrado == False:
        airports.append(airport)
        return True
    else:
        return False

# ===== REMOVE AIRPORT =====

def RemoveAirport(airports, code):
    encontrado = False
    i = 0
    n = len(airports)
    pos = -1
    while i < n and encontrado == False:
        if airports[i].code == code:
            encontrado = True
            pos = i
        else:
            i = i + 1
    if encontrado:
        while pos < n - 1:
            airports[pos] = airports[pos + 1]
            pos = pos + 1
        del airports[n - 1]

# ===== PLOT AIRPORTS =====

def PlotAirports(airports):
    si = 0
    no = 0
    for a in airports:
        SetSchengen(a)
        if a.schengen:
            si = si + 1
        else:
            no = no + 1

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.bar(['Aeropuertos'], [si], label='Schengen', color='blue')
    ax.bar(['Aeropuertos'], [no], bottom=[si], label='No Schengen', color='red')

    ax.set_title("Schengen vs No Schengen")
    ax.legend()

    return fig

# ===== MAP AIRPORTS (PUNTOS GOOGLE EARTH) =====

def MapAirports(airports):
    f = open("airports_map.kml", "w")
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
    f.write("<Document>\n")

    for a in airports:
        f.write("  <Placemark>\n")
        f.write("    <name>" + a.code + "</name>\n")
        # Ponemos una descripcion si es Schengen o no
        estado = "Schengen" if a.schengen else "No Schengen"
        f.write("    <description>" + estado + "</description>\n")
        f.write("    <Point>\n")
        # En KML primero va Longitud y luego Latitud
        f.write("      <coordinates>" + str(a.lon) + "," + str(a.lat) + "</coordinates>\n")
        f.write("    </Point>\n")
        f.write("  </Placemark>\n")

    f.write("</Document>\n")
    f.write("</kml>\n")
    f.close()
    print("Archivo 'airports_map.kml' generado. Ábrelo con Google Earth.")