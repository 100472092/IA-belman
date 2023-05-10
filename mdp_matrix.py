import json


def init():
    """reads the input file and return relevant values"""
    try:
        with open("input-matrix.json") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise "File Not Found" from exc
    return data["final"], data["p_on"], data["p_off"], data["max_it"], data["tolerance"], data["coste_on"], data[
        "coste_off"]


def v_states_init(states: dict):
    """inicialize a dictionary"""
    for i in range((25 - 16) * 2 + 1):
        states[str(i / 2 + 16)] = 0


def belman_it(v_estados: dict, v_estados_prev: dict, coste_on: float, coste_off: float, p_on: dict, p_off: dict,
              tolerancia: float, final_state):
    """one belman iteration for a set of given states"""
    control = True
    for i in range((25 - 16) * 2 + 1):
        # print(i)
        if (i / 2 + 16) == final_state:
            v_estados[str(i / 2 + 16)] = 0
        else:
            encender = coste_on
            apagar = coste_off
            for p in p_on:
                encender += p_on[str(i / 2 + 16)][p] * v_estados_prev[p]
                apagar += p_off[str(i / 2 + 16)][p] * v_estados_prev[p]
            v_estados[str(i / 2 + 16)] = min(encender, apagar)

    for i in range((25 - 16) * 2 + 1):
        if v_estados[str(i / 2 + 16)] - v_estados_prev[str(i / 2 + 16)] > tolerancia:
            control = False
        v_estados_prev[str(i / 2 + 16)] = v_estados[str(i / 2 + 16)]
    return control


def main():
    """Bloque principal: bucle y política óptima"""
    FINAL, P_ON, P_OFF, MAX_IT, TOLERANCE, COSTE_ON, COSTE_OFF = init() # parámetros
    stop = False # condición de parada
    v_prev_estados = {} # valor de cada estado en la iteración i - 1
    v_estados = {} # valor de cada estado en la iteración i

    v_states_init(v_estados) # inicialización
    v_states_init(v_prev_estados)

    it = 0
    while (not stop) and (it < MAX_IT):
        # iteración de belman
        stop = belman_it(v_estados, v_prev_estados, COSTE_ON, COSTE_OFF, P_ON, P_OFF, TOLERANCE, FINAL)
        it += 1

    # Política óptima
    print("***====================***")
    print("Política óptima:")
    for i in range((25 - 16) * 2 + 1):
        # print(i)
        if (i / 2 + 16) == FINAL:
            print(i / 2 + 16, " : ", "META", "coste:", 0)
        else:
            encender = COSTE_ON
            apagar = COSTE_OFF
            for p in P_ON:
                encender += P_ON[str(i / 2 + 16)][p] * v_prev_estados[p] # valor de cada estado
                apagar += P_OFF[str(i / 2 + 16)][p] * v_prev_estados[p]
            encender, apagar = round(encender, 2), round(apagar, 2)
            if encender < apagar:
                print(i / 2 + 16, " : ", "on ", "coste:", encender)
            else:
                print(i / 2 + 16, " : ", "off", "coste:", apagar)
    print("***====================***")
    print("nº de iteraciones:", it)
    print("ESTABILIZADO: ", stop)


if __name__ == "__main__":
    main()
