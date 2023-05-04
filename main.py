# CONSTANTES

C_ENCENDER = 10
C_APAGAR = 4
P_ENCENDER = {"s": 0.1, "up1": 0.2, "up0.5": 0.5, "down": 0.1}
P_APAGAR = {"s": 0.2, "up": 0.1, "down": 0.7}
P_ENCENDER_16 = {"s": 0.3, "up1": 0.2, "up0.5": 0.5, "down": 0}
P_APAGAR_16 = {"s": 0.9, "up": 0.1, "down": 0}
P_ENCENDER_25 = {"s": 0.9, "up1": 0, "up0.5": 0, "down": 0.1}
P_APAGAR_25 = {"s": 0.3, "up": 0, "down": 0.7}
P_ENCENDER_24 = {"s": 0.2, "up1": 0, "up0.5": 0.7, "down": 0.1}
TOLERANCIA = 0.00001

class Estado():
    def __init__(self, temp):
        self.temp = temp
        self.encender = P_ENCENDER
        self.apagar = P_APAGAR
        if temp == 16.0:
            self.encender = P_ENCENDER_16
            self.apagar = P_APAGAR_16
        elif temp == 24.5:
            self.encender = P_ENCENDER_24
        elif temp == 25.0:
            self.encender = P_ENCENDER_25
            self.apagar = P_APAGAR_25

    def __str__(self):
        return str(self.temp)


# Dicionarios de estabilidad y valor de estados
Vestados = {}
Vestados_anterior = {}
for i in range((25 - 16) * 2 + 1):
    Vestados[i/2 + 16] = 0
    Vestados_anterior[i/2 + 16] = 0

Vestados[26.0] = 0
Vestados[25.5] = 0
Vestados[15.5] = 0
Vestados_anterior[26.0] = 0
Vestados_anterior[25.5] = 0
Vestados_anterior[15.5] = 0

estado_estable = {}
for i in range((25 - 16) * 2 + 1):
    estado_estable[i/2 + 16] = False
estado_estable[22.0] = True

# lista de estados
estados = []
for i in range((25 - 16) * 2 + 1):
    estados.append(Estado(i/2 + 16))

"""for element in estados:
    print(element, end=", ")
print("\n")"""

def it_belman(estados: list, tolerancia: float):
    for i in range((25 - 16) * 2 + 1):
        #print(i)
        if not estado_estable[i/2 + 16]:
            Vestados[i/2 + 16] = min(C_ENCENDER +
                                         estados[i].encender["up0.5"] * Vestados_anterior[i/2 + 16 + 0.5] +
                                         estados[i].encender["up1"] * Vestados_anterior[i/2 + 16 + 1] +
                                         estados[i].encender["s"] * Vestados_anterior[i/2 + 16],
                                         C_APAGAR +
                                         estados[i].apagar["down"] * Vestados_anterior[i/2 + 16 - 0.5] +
                                         estados[i].apagar["s"] * Vestados_anterior[i/2 + 16]
                                    )
    for i in range((25 - 16) * 2 + 1):
        if Vestados[i/2 + 16] - Vestados_anterior[i/2 + 16] < tolerancia:
            estado_estable[i/2 + 16] = True
        else:
            Vestados_anterior[i / 2 + 16] = Vestados[i/2 + 16]

def final_check(estados):
    for e in estados:
        if not estado_estable[e]:
            return False
    return True

it = 0
while not final_check(estado_estable):
    print(it)
    it_belman(estados, TOLERANCIA)
    it += 1
    print("Vestados:", Vestados)
    print("Vestados:anterior: ", Vestados_anterior)

print("Política óptima:")
for i in range((25 - 16) * 2 + 1):
    #print(i)
    encender = C_ENCENDER + estados[i].encender["up0.5"] * Vestados[i/2 + 16 + 0.5] + \
               estados[i].encender["up1"] * Vestados[i/2 + 16 + 1] + estados[i].encender["s"] * Vestados[i/2 + 16]
    apagar = C_APAGAR + estados[i].apagar["down"] * Vestados[i/2 + 16 - 0.5] + \
             estados[i].apagar["s"] * Vestados[i/2 + 16]
    if encender < apagar:
        print(i/2 + 16, " : ", "enender")
    else:
        print(i/2 + 16, " : ", "apagar")