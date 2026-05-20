import matplotlib.pyplot as plt
import matplotlib.patches as patches
from aircraft import Aircraft
from airport import IsSchengenAirport


class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = None


class BoardingArea:
    def __init__(self, name):
        self.name = name
        self.area_type = None  # "Schengen" o "non-Schengen"
        self.gates = []


class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = []


class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []


# ===== SET GATES =====
def SetGates(area, init_gate, end_gate, prefix):
    if end_gate <= init_gate:
        return -1

    area.gates = []
    i = init_gate
    while i <= end_gate:
        gate_name = prefix + "G" + str(i)
        gate = Gate(gate_name)
        area.gates.append(gate)
        i = i + 1

    return len(area.gates)


# ===== LOAD AIRLINES =====
def LoadAirlines(terminal, t_name):
    filename = t_name + "_Airlines.txt"
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        terminal.airlines = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line != "":
                parts = line.split('\t')
                if len(parts) >= 2:
                    airline_code = parts[1].strip()
                    terminal.airlines.append(airline_code)
            i = i + 1

        return len(terminal.airlines)

    except FileNotFoundError:
        print("Archivo " + filename + " no encontrado")
        return -1


# ===== LOAD AIRPORT STRUCTURE =====
def LoadAirportStructure(filename):
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except FileNotFoundError:
        print("Error: Archivo " + filename + " no encontrado")
        return None

    if len(lines) < 1:
        print("Archivo vacio")
        return None
    # Primera linea: LEBL 2 terminals
    first_line = lines[0].strip().split()
    code = first_line[0]
    num_terminals = int(first_line[1])

    bcn = BarcelonaAP(code)

    line_idx = 1
    t = 0
    while t < num_terminals and line_idx < len(lines):
        # Linea de terminal: Terminal T1 5 boarding areas
        terminal_line = lines[line_idx].strip().split()
        terminal_name = terminal_line[1]
        num_areas = int(terminal_line[2])

        terminal = Terminal(terminal_name)
        LoadAirlines(terminal, terminal_name)

        line_idx = line_idx + 1
        a = 0
        while a < num_areas and line_idx < len(lines):
            # Linea de area: Area A Schengen Gates 1 - 11
            area_parts = lines[line_idx].strip().split()

            area_name = area_parts[1]
            area_type = area_parts[2]
            init_gate = int(area_parts[4])
            end_gate = int(area_parts[6])

            prefix = terminal_name + area_name

            area = BoardingArea(area_name)
            area.area_type = area_type
            SetGates(area, init_gate, end_gate, prefix)

            terminal.boarding_areas.append(area)

            line_idx = line_idx + 1
            a = a + 1

        bcn.terminals.append(terminal)
        t = t + 1

    return bcn


# ===== IS AIRLINE IN TERMINAL =====
def IsAirlineInTerminal(terminal, name):
    if name == "":
        return False

    if len(terminal.airlines) == 0:
        return False

    i = 0
    while i < len(terminal.airlines):
        if terminal.airlines[i] == name:
            return True
        i = i + 1

    return False


# ===== SEARCH TERMINAL =====
def SearchTerminal(bcn, name):
    t = 0

    while t < len(bcn.terminals):
        terminal = bcn.terminals[t]
        found = IsAirlineInTerminal(terminal, name)
        if found == True:
            return terminal.name
        t = t + 1
    return ""

# ===== ASSIGN GATE =====
def AssignGate(bcn, aircraft):

    terminal_name = SearchTerminal(bcn, aircraft.company)
    if terminal_name == "":
        return -1

    terminal = None
    i = 0
    while i < len(bcn.terminals):
        if bcn.terminals[i].name == terminal_name:
            terminal = bcn.terminals[i]
        i = i + 1

    if terminal is None:
        return -1

    is_schengen = IsSchengenAirport(aircraft.origin) #Volvemos a llamar a la funcion de la V1
    if is_schengen:
        write = "Schengen"
    else:
        write = "non-Schengen"

    i = 0
    while i < len(terminal.boarding_areas):
        area = terminal.boarding_areas[i]
        if area.area_type == write:
            j = 0
            while j < len(area.gates):
                gate = area.gates[j]
                if not gate.occupied:
                    gate.occupied = True
                    gate.aircraft_id = aircraft.aircraft
                    return 0
                j = j + 1
        i = i + 1

    return -1


# ===== GATE OCCUPANCY =====
def GateOccupancy(bcn):
    occupancy = []
    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]
        j = 0
        while j < len(terminal.boarding_areas):
            area = terminal.boarding_areas[j]
            k = 0
            while k < len(area.gates):
                gate = area.gates[k]
                if gate.occupied:
                    status = "Ocupado"
                    aircraft_id = gate.aircraft_id
                else:
                    status = "Libre"
                    aircraft_id = "-"

                occupancy.append([terminal.name, area.name,
                                       gate.name, status, aircraft_id])
                k = k + 1
            j = j + 1
        i = i + 1

    return occupancy


# ===== PLOT GATES =====
def PlotGates(bcn):
    if bcn is None or len(bcn.terminals) == 0:
        print("Error: No hay estructura de aeropuerto")
        return None

    fig, axes = plt.subplots(1, len(bcn.terminals), figsize=(15, 6))

    # Si solo hay 1 terminal axes no es lista, lo convertimos
    if len(bcn.terminals) == 1:
        axes = [axes]
    t = 0
    while t < len(bcn.terminals):
        terminal = bcn.terminals[t]
        ax = axes[t]

        ax.set_title("Terminal " + terminal.name, fontsize=14, fontweight='bold')
        ax.set_xlim(-0.5, 10)
        ax.set_ylim(-0.5, len(terminal.boarding_areas) * 3)
        ax.axis('off')

        y_pos = len(terminal.boarding_areas) * 3 - 1

        a = 0
        while a < len(terminal.boarding_areas):
            area = terminal.boarding_areas[a]

            ax.text(-0.3, y_pos, area.name + " (" + area.area_type + ")",fontsize=10, fontweight='bold')
            y_pos = y_pos - 0.7

            x_pos = 0
            g = 0
            while g < len(area.gates):
                gate = area.gates[g]

                if gate.occupied:
                    color = '#e74c3c'  # rojo
                else:
                    color = '#2ecc71'  # verde

                rect = patches.Rectangle((x_pos, y_pos - 0.5), 0.8, 0.4,
                                         linewidth=1, edgecolor='black',
                                         facecolor=color, alpha=0.7)
                ax.add_patch(rect)

                if gate.occupied:
                    label = gate.aircraft_id[0:3]
                else:
                    label = "G" + str(g + 1)

                ax.text(x_pos + 0.4, y_pos - 0.3, label,
                        ha='center', va='center',
                        fontsize=8, fontweight='bold', color='white')

                x_pos = x_pos + 1
                if x_pos > 9:
                    x_pos = 0
                    y_pos = y_pos - 0.7

                g = g + 1

            y_pos = y_pos - 1.5
            a = a + 1

        t = t + 1

    plt.tight_layout()
    return fig




