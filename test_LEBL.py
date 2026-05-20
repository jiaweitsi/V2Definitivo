from LEBL import *
if __name__ == "__main__":
    print("=== TEST LEBL.PY ===\n")

    # Test 1: cargar estructura
    print("Test 1: Cargar estructura del aeropuerto desde Terminals.txt")
    bcn = LoadAirportStructure("Terminals.txt")

    if bcn is None:
        print("No se pudo cargar. Comprueba que Terminals.txt esta en la carpeta.")
    else:
        print("Aeropuerto cargado: " + bcn.code)
        print("Numero de terminales: " + str(len(bcn.terminals)))

        i = 0
        while i < len(bcn.terminals):
            t = bcn.terminals[i]
            print("\nTerminal: " + t.name)
            print("  Aerolineas: " + str(len(t.airlines)))
            print("  Boarding areas: " + str(len(t.boarding_areas)))
            j = 0
            while j < len(t.boarding_areas):
                area = t.boarding_areas[j]
                print("    Area " + area.name + " (" + area.area_type + "): " + str(len(area.gates)) + " gates")
                j = j + 1
            i = i + 1

        # Test 2: asignar gates
        # Usamos Aircraft(aircraft, company, origin, time) igual que tu clase
        print("\nTest 2: Asignar gates a vuelos de prueba")
        vuelo1 = Aircraft("ECMKV", "VLG", "LYBE", "00:04")
        vuelo2 = Aircraft("EIDPG", "RYR", "EGCC", "04:57")

        res1 = AssignGate(bcn, vuelo1)
        res2 = AssignGate(bcn, vuelo2)

        if res1 == 0:
            print("ECMKV asignado correctamente")
        else:
            print("ECMKV NO asignado (aerolinea no encontrada o sin gates libres)")

        if res2 == 0:
            print("EIDPG asignado correctamente")
        else:
            print("EIDPG NO asignado (aerolinea no encontrada o sin gates libres)")

        # Test 3: ocupacion
        print("\nTest 3: Estado de gates")
        ocupacion = GateOccupancy(bcn)
        print("Total gates: " + str(len(ocupacion)))

        libres = 0
        ocupados = 0
        i = 0
        while i < len(ocupacion):
            if ocupacion[i][3] == "Ocupado":
                ocupados = ocupados + 1
            else:
                libres = libres + 1
            i = i + 1

        print("Gates libres: " + str(libres))
        print("Gates ocupados: " + str(ocupados))

        # Test 4: grafica
        print("\nTest 4: Mostrar grafica de gates")
        fig = PlotGates(bcn)
        if fig is not None:
            print("Grafica generada correctamente")
            plt.show()

    print("\n=== FIN TEST ===")
