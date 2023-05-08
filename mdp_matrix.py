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
    states["25.5"] = 0
    states["26.0"] = 0
    states["15.5"] = 0


def belman_it(v_estados: dict, v_estados_prev: dict, coste_on: float, coste_off: float, p_on: dict, p_off: dict,
              tolerancia: float, final_state):
    """one belman iteration for a set of given states"""
    control = True
    for i in range((25 - 16) * 2 + 1):
        # print(i)
        if (i / 2 + 16) == 22.0:
            v_estados[str(i / 2 + 16)] = 0
        else:
            encender = coste_on
            apagar = coste_off
            for p in p_on:
                encender += p_on[str(i / 2 + 16)][p]*v_estados_prev[p]
            #print("encender:", i/2 + 16, " | ", encender)
            for p in p_off:
                apagar += p_off[str(i / 2 + 16)][p]*v_estados_prev[p]
            #print("apagar  :", i/2 + 16, " | ", apagar)
            v_estados[str(i / 2 + 16)] = min(round(encender, 2), round(apagar, 2))


    for i in range((25 - 16) * 2 + 1):
        if v_estados[str(i / 2 + 16)] - v_estados_prev[str(i / 2 + 16)] > tolerancia:
            control = False
        v_estados_prev[str(i / 2 + 16)] = v_estados[str(i / 2 + 16)]
    return control


def main():
    FINAL, P_ON, P_OFF, MAX_IT, TOLERANCE, COSTE_ON, COSTE_OFF = init()
    stop = False
    v_prev_estados = {}
    v_estados = {}

    v_states_init(v_estados)
    v_states_init(v_prev_estados)

    it = 0
    while (not stop) and (it < MAX_IT):
        stop = belman_it(v_estados, v_prev_estados, COSTE_ON, COSTE_OFF, P_ON, P_OFF, TOLERANCE, FINAL)
        #print(it)
        it += 1
        #print("v_estados: ", v_estados)
        #print("v_prev_estados: ", v_prev_estados)

    print("***====================***")
    print("Política óptima:")
    for i in range((25 - 16) * 2 + 1):
        # print(i)
        encender = COSTE_ON
        apagar = COSTE_OFF
        for p in P_ON:
            encender += P_ON[str(i / 2 + 16)][p]*v_prev_estados[p]
            apagar += P_OFF[str(i / 2 + 16)][p]*v_prev_estados[p]
        encender, apagar = round(encender, 2), round(apagar, 2)
        if encender < apagar:
            print(i / 2 + 16, " : ", "on ", "coste:", encender)
        else:
            print(i / 2 + 16, " : ", "off", "coste:", apagar)
    print("***====================***")
    print("nº de iteraciones:", it)


if __name__ == "__main__":
    main()
