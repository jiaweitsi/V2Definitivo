# interface.py
# Version 3 - Interfaz grafica completa (Aeropuertos + Vuelos + Gates)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from airport import *
from aircraft import *
from LEBL import *

# -------------------------------------------------------
# VARIABLES GLOBALES
# -------------------------------------------------------

lista_trabajo = []   # lista de aeropuertos (Airport)
lista_vuelos = []    # lista de vuelos (Aircraft)
bcn = None           # estructura del aeropuerto (BarcelonaAP)


# =====================================================================
# FUNCIONES - AEROPUERTOS (Version 1)
# =====================================================================

def btn_cargar_click():
    global lista_trabajo
    lista_trabajo = LoadAirports("Airports.txt")
    actualizar_pantalla()
    messagebox.showinfo("Cargar", "Datos cargados correctamente")

def btn_anadir_click():
    c = entrada_cod.get().upper()
    lat = entrada_lat.get()
    lon = entrada_lon.get()

    if len(c) != 4 or not c.isalpha():
        messagebox.showerror("Error", "El código ICAO debe tener 4 LETRAS.")
        return

    try:
        lat = float(lat)
        lon = float(lon)
        nuevo = Airport(c, lat, lon)
        anadido = AddAirport(lista_trabajo, nuevo)
        if anadido:
            actualizar_pantalla()
        else:
            messagebox.showerror("Error", "El aeropuerto ya existe en la lista.")
    except ValueError:
        messagebox.showerror("Error", "Introduce números válidos en Lat y Lon.")

def btn_borrar_click():
    c = entrada_cod.get().upper()
    if c == "":
        messagebox.showwarning("Aviso", "Escribe el código ICAO a borrar.")
        return
    RemoveAirport(lista_trabajo, c)
    actualizar_pantalla()

def btn_guardar_click():
    SaveSchengenAirports(lista_trabajo, "Schengen_Only.txt")
    messagebox.showinfo("Guardar", "Archivo Schengen_Only.txt creado")

def btn_mapa_aeropuertos_click():
    if len(lista_trabajo) == 0:
        messagebox.showwarning("Aviso", "Carga los aeropuertos primero")
        return
    MapAirports(lista_trabajo)
    messagebox.showinfo("KML", "Archivo airports_map.kml generado.")

def actualizar_pantalla():
    caja.delete(1.0, tk.END)
    i = 0
    while i < len(lista_trabajo):
        a = lista_trabajo[i]
        SetSchengen(a)
        if a.schengen:
            res = "SI"
        else:
            res = "NO"
        caja.insert(tk.END, "Cod: " + a.code + " | Lat: " + str(round(a.lat, 4)) +
                    " | Lon: " + str(round(a.lon, 4)) + " | Schengen: " + res + "\n")
        i = i + 1


# =====================================================================
# FUNCIONES - VUELOS (Version 2)
# =====================================================================

def btn_cargar_vuelos_click():
    global lista_vuelos
    lista_vuelos = LoadArrivals("Arrivals.txt")
    actualizar_pantalla_vuelos()
    messagebox.showinfo("Vuelos", "Vuelos cargados correctamente")

def btn_mapa_kml_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Aviso", "Carga los vuelos primero")
        return
    if len(lista_trabajo) == 0:
        messagebox.showwarning("Aviso", "Carga los aeropuertos primero")
        return
    MapFlights(lista_vuelos, lista_trabajo)
    messagebox.showinfo("KML", "Archivo trayectorias.kml generado.")

def btn_vuelos_largos_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Aviso", "Carga los vuelos primero")
        return
    if len(lista_trabajo) == 0:
        messagebox.showwarning("Aviso", "Carga los aeropuertos primero")
        return
    vuelos_distantes = LongFlightArrivals(lista_vuelos, lista_trabajo)
    caja.delete(1.0, tk.END)
    caja.insert(tk.END, "--- VUELOS LARGA DISTANCIA (>2000km) ---\n")
    i = 0
    while i < len(vuelos_distantes):
        v = vuelos_distantes[i]
        caja.insert(tk.END, "Avion: " + str(v.aircraft) + " | Origen: " +
                    str(v.origin) + " | Hora: " + str(v.time) + "\n")
        i = i + 1

def btn_exportar_vuelos_largos_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Aviso", "Carga los vuelos primero")
        return
    if len(lista_trabajo) == 0:
        messagebox.showwarning("Aviso", "Carga los aeropuertos primero")
        return
    vuelos_especiales = LongFlightArrivals(lista_vuelos, lista_trabajo)
    if len(vuelos_especiales) > 0:
        exito = SaveFlights(vuelos_especiales, "vuelos_inspeccion_especial.txt")
        if exito:
            messagebox.showinfo("Exportar", "Guardados " + str(len(vuelos_especiales)) + " vuelos.")
        else:
            messagebox.showerror("Error", "No se pudo crear el archivo")
    else:
        messagebox.showwarning("Atención", "No hay vuelos de más de 2000km")

def actualizar_pantalla_vuelos():
    caja.delete(1.0, tk.END)
    i = 0
    while i < len(lista_vuelos):
        v = lista_vuelos[i]
        caja.insert(tk.END, "Avión: " + str(v.aircraft) + " | Origen: " +
                    str(v.origin) + " | Hora: " + str(v.time) +
                    " | Compañia: " + str(v.company) + "\n")
        i = i + 1

def btn_guardar_vuelos_fichero_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Error", "No hay vuelos cargados")
        return
    exito = SaveFlights(lista_vuelos, "vuelos_guardados.txt")
    if exito:
        messagebox.showinfo("Guardar", "Vuelos guardados en 'vuelos_guardados.txt'")
    else:
        messagebox.showerror("Error", "No se ha podido guardar el archivo")


# =====================================================================
# FUNCIONES - GATES (Version 3)
# =====================================================================

def btn_cargar_estructura_click():
    global bcn
    resultado = LoadAirportStructure("Terminals.txt")
    if resultado is None:
        messagebox.showerror("Error", "No se pudo cargar Terminals.txt")
        return
    bcn = resultado
    actualizar_pantalla_gates()
    messagebox.showinfo("Estructura", "Aeropuerto " + bcn.code + " cargado correctamente")


def btn_asignar_gates_click():
    if bcn is None:
        messagebox.showerror("Error", "Primero carga la estructura (Terminals.txt)")
        return
    if len(lista_vuelos) == 0:
        messagebox.showerror("Error", "Primero carga los vuelos")
        return

    asignados = 0
    no_asignados = 0
    i = 0
    while i < len(lista_vuelos):
        resultado = AssignGate(bcn, lista_vuelos[i])
        if resultado == 0:
            asignados = asignados + 1
        else:
            no_asignados = no_asignados + 1
        i = i + 1

    actualizar_pantalla_gates()
    messagebox.showinfo("Gates", "Asignados: " + str(asignados) +
                        "\nNo asignados: " + str(no_asignados))


def btn_ver_ocupacion_click():

    if bcn is None:
        messagebox.showerror("Error","Primero carga la estructura del aeropuerto")
        return
    caja.delete(1.0, tk.END)

    ocupacion = GateOccupancy(bcn)

    total_gates = 0
    gates_libres = 0
    gates_ocupados = 0
    i = 0
    while i < len(ocupacion):
        gate = ocupacion[i]
        total_gates = total_gates + 1
        estado = gate[3]

        if estado == "Ocupado":
            gates_ocupados = gates_ocupados + 1
        else:
            gates_libres = gates_libres + 1
        i = i + 1

    caja.insert( tk.END,"Total gates: " + str(total_gates) + "\n")
    caja.insert(tk.END, "Gates libres: " + str(gates_libres) + "\n")
    caja.insert(tk.END, "Gates ocupados: " + str(gates_ocupados) + "\n")


def actualizar_pantalla_gates():
    caja.delete(1.0, tk.END)
    if bcn is None:
        caja.insert(tk.END, "No hay estructura cargada.\n")
        return

    ocupacion = GateOccupancy(bcn)
    caja.insert(tk.END, "=== OCUPACION DE GATES - " + bcn.code + " ===\n\n")

    terminal_actual = ""
    area_actual = ""
    i = 0
    while i < len(ocupacion):
        g = ocupacion[i]
        if g[0] != terminal_actual:
            terminal_actual = g[0]
            area_actual = ""
            caja.insert(tk.END, "\nTERMINAL " + terminal_actual + "\n")
        if g[1] != area_actual:
            area_actual = g[1]
            caja.insert(tk.END, "  Area " + area_actual + ":\n")
        caja.insert(tk.END, "    " + g[2] + " -> " + g[3])
        if g[3] == "Ocupado":
            caja.insert(tk.END, " (" + g[4] + ")")
        caja.insert(tk.END, "\n")
        i = i + 1

# =====================================================================
# GRAFICOS
# =====================================================================

canvas_picture = None

def mostrar_grafico_en_interfaz(figura):
    global canvas_picture
    if canvas_picture is not None:
        canvas_picture.get_tk_widget().destroy()
    figura.set_size_inches(5, 4)
    canvas_obj = FigureCanvasTkAgg(figura, master=panel_graficas)
    canvas_obj.draw()
    canvas_picture = canvas_obj
    widget = canvas_obj.get_tk_widget()
    widget.grid(row=0, column=0, padx=5, pady=5)

def btn_grafica_aeropuertos_click():
    if not lista_trabajo:
        messagebox.showwarning("Aviso", "Carga los aeropuertos primero")
        return
    figura = PlotAirports(lista_trabajo)
    mostrar_grafico_en_interfaz(figura)

def btn_grafica_llegadas_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Error", "Carga los vuelos primero")
        return
    fig = PlotArrivals(lista_vuelos)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)

def btn_grafica_airlines_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Error", "Carga los vuelos primero")
        return
    fig = PlotAirlines(lista_vuelos)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)

def btn_grafica_schengen_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning("Error", "Carga los vuelos primero")
        return
    fig = PlotFlightsType(lista_vuelos)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)

def btn_grafica_gates_click():
    if bcn is None:
        messagebox.showerror("Error", "Primero carga la estructura del aeropuerto")
        return
    fig = PlotGates(bcn)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)


# =====================================================================
# DISEÑO DE LA INTERFAZ
# =====================================================================

root = tk.Tk()
root.title('Airport Manager')
root.geometry("1100x750")
root.configure(bg="#F7F8FC")

# ---------- ESTILOS -----------
style = ttk.Style()
style.theme_use("clam")


style.configure("Panel.TLabelframe", background="#E8ECF7", padding=3)
style.configure("Panel.TLabelframe.Label", font=("Segoe UI", 8, "bold"))


style.configure("Action.TButton", background="#CDE7FF", padding=2, font=("Segoe UI", 8))
style.map("Action.TButton", background=[("active", "#AED6F1")])

style.configure("Flight.TButton", background="#FADBD8", padding=2, font=("Segoe UI", 8))
style.map("Flight.TButton", background=[("active", "#F5B7B1")])

style.configure("Gate.TButton", background="#E8DAEF", padding=2, font=("Segoe UI", 8))
style.map("Gate.TButton", background=[("active", "#D2B4DE")])

style.configure("Graph.TButton", background="#D5F5E3", padding=2, font=("Segoe UI", 8))
style.map("Graph.TButton", background=[("active", "#ABEBC6")])

style.configure("Primary.TButton", background="#D6EAF8", padding=2, font=("Segoe UI", 8))

style.configure("TLabel", font=("Segoe UI", 8))
style.configure("TEntry", font=("Segoe UI", 8))

# ---------- GRID PRINCIPAL ----------
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=3)
root.rowconfigure(1, weight=2)

# ================= PANEL IZQUIERDO =================
left_panel = ttk.Frame(root)
left_panel.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=6, pady=6)
left_panel.columnconfigure(0, weight=1)

# -------------------------------------------------------
# SECCION: AEROPUERTOS
# -------------------------------------------------------
acciones = ttk.LabelFrame(left_panel, text="Aeropuertos", style="Panel.TLabelframe")
acciones.grid(row=0, column=0, sticky="ew", pady=2)

ttk.Button(acciones, text="Cargar Aeropuertos",
           style="Action.TButton", command=btn_cargar_click).grid(sticky="ew", pady=1)
ttk.Button(acciones, text="Guardar Schengen",
           style="Action.TButton", command=btn_guardar_click).grid(sticky="ew", pady=1)
ttk.Button(acciones, text="Ver Puntos Google Earth",
           style="Action.TButton", command=btn_mapa_aeropuertos_click).grid(sticky="ew", pady=1)

# -------------------------------------------------------
# SECCION: AÑADIR / BORRAR (Versión 1)
# -------------------------------------------------------
datos = ttk.LabelFrame(left_panel, text="Añadir / Borrar Aeropuerto", style="Panel.TLabelframe")
datos.grid(row=1, column=0, sticky="ew", pady=2)

# Ponemos las entradas en una sola fila para ahorrar espacio
fila_icao = ttk.Frame(datos)
fila_icao.pack(fill="x", pady=1)
ttk.Label(fila_icao, text="ICAO:").pack(side=tk.LEFT)
entrada_cod = ttk.Entry(fila_icao, width=6)
entrada_cod.pack(side=tk.LEFT, padx=2)

fila_lat = ttk.Frame(datos)
fila_lat.pack(fill="x", pady=1)
ttk.Label(fila_lat, text="Lat: ").pack(side=tk.LEFT)
entrada_lat = ttk.Entry(fila_lat, width=10)
entrada_lat.pack(side=tk.LEFT, padx=2)

fila_lon = ttk.Frame(datos)
fila_lon.pack(fill="x", pady=1)
ttk.Label(fila_lon, text="Lon:").pack(side=tk.LEFT)
entrada_lon = ttk.Entry(fila_lon, width=10)
entrada_lon.pack(side=tk.LEFT, padx=2)

# Añadir y Borrar en la misma fila
fila_botones = ttk.Frame(datos)
fila_botones.pack(fill="x", pady=2)
ttk.Button(fila_botones, text="Añadir", style="Primary.TButton",
           command=btn_anadir_click).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=1)
ttk.Button(fila_botones, text="Borrar",
           command=btn_borrar_click).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=1)

# -------------------------------------------------------
# SECCION: VUELOS (Versión 2)
# -------------------------------------------------------
vuelos_frame = ttk.LabelFrame(left_panel, text="Gestión de Vuelos", style="Panel.TLabelframe")
vuelos_frame.grid(row=2, column=0, sticky="ew", pady=2)

botones_vuelos = [
    ("Cargar Vuelos",            btn_cargar_vuelos_click),
    ("Generar KML trayectorias", btn_mapa_kml_click),
    ("Filtrar Vuelos Largos",    btn_vuelos_largos_click),
    ("Guardar Vuelos",           btn_guardar_vuelos_fichero_click),
    ("Exportar a fichero Vuelos Largos",   btn_exportar_vuelos_largos_click),
]

for txt, cmd in botones_vuelos:
    ttk.Button(vuelos_frame, text=txt, style="Flight.TButton",
               command=cmd).grid(sticky="ew", pady=1)

# -------------------------------------------------------
# SECCION: GATES (Version 3)
# -------------------------------------------------------
gates_frame = ttk.LabelFrame(left_panel, text="Gestión de Gates (V3)", style="Panel.TLabelframe")
gates_frame.grid(row=3, column=0, sticky="ew", pady=2)

botones_gates = [
    ("Cargar Estructura (Terminals.txt)", btn_cargar_estructura_click),
    ("Asignar Gates a Vuelos",       btn_asignar_gates_click),
    ("Ver Ocupación de Gates",       btn_ver_ocupacion_click),
]

for txt, cmd in botones_gates:
    ttk.Button(gates_frame, text=txt, style="Gate.TButton",
               command=cmd).grid(sticky="ew", pady=1)

# ================= CONSOLA DERECHA (arriba) =================
consola = ttk.LabelFrame(root, text="Consola / Resultados", style="Panel.TLabelframe")
consola.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)

scrollbar_caja = tk.Scrollbar(consola)
scrollbar_caja.pack(side=tk.RIGHT, fill=tk.Y)

caja = tk.Text(consola, font=("Courier", 9), yscrollcommand=scrollbar_caja.set)
caja.pack(fill=tk.BOTH, expand=True)
scrollbar_caja.config(command=caja.yview)

# ================= PANEL GRAFICAS (abajo derecha) =================
panel_graficas = ttk.LabelFrame(root, text="Visualización de Gráficas")
panel_graficas.grid(row=1, column=1, padx=6, pady=3, sticky="nsew")
panel_graficas.rowconfigure(0, weight=1)
panel_graficas.columnconfigure(0, weight=1)

# ================= BOTONES GRAFICAS (fila inferior) =================
graficas = ttk.LabelFrame(root, text="Gráficas", style="Panel.TLabelframe")
graficas.grid(row=2, column=0, columnspan=2, sticky="ew", padx=6, pady=3)
graficas.columnconfigure((0, 1, 2, 3, 4), weight=1)

botones_graficas = [
    ("Schengen vs NoSchengen",        btn_grafica_aeropuertos_click),
    ("Llegadas por hora",             btn_grafica_llegadas_click),
    ("Vuelos por Aerolínea",          btn_grafica_airlines_click),
    ("Vuelos Schengen vs NoSchengen", btn_grafica_schengen_click),
    ("Mapa de Gates",                 btn_grafica_gates_click),
]

for i, (txt, cmd) in enumerate(botones_graficas):
    ttk.Button(graficas, text=txt, style="Graph.TButton",
               command=cmd).grid(row=0, column=i, sticky="ew", padx=3, pady=3)

root.mainloop()