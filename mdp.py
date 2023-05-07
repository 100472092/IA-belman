import json


def init():
    """reads the input file and return relevant values"""
    try:
        with open("input.json") as file:
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
              tolerancia: float):
    """one belman iteration for a set of given states"""
    control = True
    for i in range((25 - 16) * 2 + 1):
        # print(i)
        if (i / 2 + 16) == 22.0:
            v_estados[str(i / 2 + 16)] = 0
        else:

            v_estados[str(i / 2 + 16)] = min(coste_on +
                                             p_on[str(i / 2 + 16)]["up0.5"] * v_estados_prev[str(i / 2 + 16 + 0.5)] +
                                             p_on[str(i / 2 + 16)]["up1"] * v_estados_prev[str(i / 2 + 16 + 1.0)] +
                                             p_on[str(i / 2 + 16)]["s"] * v_estados_prev[str(i / 2 + 16)] +
                                             p_on[str(i / 2 + 16)]["down"] * v_estados_prev[str(i / 2 + 16 - 0.5)],
                                             coste_off +
                                             p_off[str(i / 2 + 16)]["down"] * v_estados_prev[str(i / 2 + 16 - 0.5)] +
                                             p_off[str(i / 2 + 16)]["s"] * v_estados_prev[str(i / 2 + 16)] +
                                             p_off[str(i / 2 + 16)]["up0.5"] * v_estados_prev[str(i / 2 + 16 + 0.5)]
                                             )
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
        stop = belman_it(v_estados, v_prev_estados, COSTE_ON, COSTE_OFF, P_ON, P_OFF, TOLERANCE)
        #print(it)
        it += 1
        #print("v_estados: ", v_estados)
        #print("v_prev_estados: ", v_prev_estados)

    print("***====================***")
    print("Política óptima:")
    for i in range((25 - 16) * 2 + 1):
        # print(i)
        encender = COSTE_ON + P_OFF[str(i / 2 + 16)]["up0.5"] * v_estados[str(i / 2 + 16 + 0.5)] + \
                   P_ON[str(i / 2 + 16)]["up1"] * v_estados[str(i / 2 + 16 + 1.0)] + P_ON[str(i / 2 + 16)]["s"] * \
                   v_estados[str(i / 2 + 16)] + P_ON[str(i / 2 + 16)]["down"] * v_estados[str(i / 2 + 16 - 0.5)]
        apagar = COSTE_OFF + P_OFF[str(i / 2 + 16)]["down"] * v_estados[str(i / 2 + 16 - 0.5)] + \
                 P_OFF[str(i / 2 + 16)]["s"] * v_estados[str(i / 2 + 16)] + P_OFF[str(i / 2 + 16)]["up0.5"] * \
                 v_estados[str(i / 2 + 16 + 0.5)]

        if encender < apagar:
            print(i / 2 + 16, " : ", "on")
        else:
            print(i / 2 + 16, " : ", "off")
    print("***====================***")
    print("nº de iteraciones:", it)


if __name__ == "__main__":
    main()
