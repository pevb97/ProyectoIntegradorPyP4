from readchar import readkey, key
import os
def cargar_mapa(ruta: str) -> list:
    arc_laberinto = open(ruta).read()
    laberinto = list(arc_laberinto.split("\n"))
    for index_fila in range(0, len(laberinto)):
        laberinto[index_fila] = list(laberinto[index_fila])
    return [laberinto, datos_laberinto(laberinto)]

def pantalla_bienvenida():
    name_player = input("Ingresa tu NickName: ")
    print("Bienvenido al juego de los laberintos", name_player, "Oprime Enter para comenzar")
    while True:
        k = readkey()
        if (k in (key.ENTER, key.ENTER_2)):
            break

def captura_movimiento() -> str:
    while True:
        k = readkey()
        if (k in (key.UP, key.DOWN, key.RIGHT, key.LEFT)):
            return k
            break

def datos_laberinto(laberinto: list) -> dict:
    #Obtencion de las posiciones dentro del laberinto que tienen pared
    pos_camino = list()
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if(laberinto[fila][columna] == "."):
                pos_camino.append([fila, columna])
    
    #Obtencion de las posiciones de los bordes del laberinto
    x_borde_izq_der = range(len(laberinto))
    y_borde_izq = [0]*len(laberinto)
    y_borde_der = [len(laberinto[0])-1]*len(laberinto)

    x_borde_sup = [0]*len(laberinto[0])
    x_borde_inf = [len(laberinto)-1]*len(laberinto[0])
    y_borde_sup_inf = range(len(laberinto[0]))

    pos_borde_izq = list(zip(x_borde_izq_der, y_borde_izq))
    pos_borde_der = list(zip(x_borde_izq_der, y_borde_der))
    pos_borde_sup = list(zip(x_borde_sup, y_borde_sup_inf))
    pos_borde_inf = list(zip(x_borde_inf, y_borde_sup_inf))
    pos_bordes_laberinto = pos_borde_izq + pos_borde_der + pos_borde_sup + pos_borde_inf

    #Obtencion de las posiciones en las que existe una entrada o salida del laberinto
    pos_in_out = list()
    for i in pos_bordes_laberinto:
        if laberinto[(i[0])][(i[1])] == ".":
            pos_in_out.append(i)

    info_laberinto ={
        "pos_camino": pos_camino,
        "pos_bordes_laberinto": pos_bordes_laberinto,
        "pos_anterior_player": list(pos_in_out[0]),
        "pos_actual_player": list(pos_in_out[0]),
        "pos_out": list(pos_in_out[1]),
    }
    return info_laberinto

def update_mapa(laberinto: list, data_lab: dict):
    os.system('cls' if os.name=='nt' else 'clear')
    laberinto[data_lab.get("pos_anterior_player")[0]][data_lab.get("pos_anterior_player")[1]] = "."
    laberinto[data_lab.get("pos_actual_player")[0]][data_lab.get("pos_actual_player")[1]] = "P"
    laberinto_print = ""
    for fila in laberinto:
        laberinto_print += "\n"
        for columna in fila:
            laberinto_print += str(columna)
    print(laberinto_print)

def movimiento(mov: str, data_lab: dict) -> list:
    pos_f, pos_c = data_lab.get("pos_actual_player")
    if (mov == key.UP and ([(pos_f-1),pos_c] in data_lab.get("pos_camino"))):
        return [[(pos_f-1),pos_c], [pos_f, pos_c]]
    elif (mov == key.DOWN and ([(pos_f+1), pos_c] in data_lab.get("pos_camino"))):
        return [[(pos_f+1), pos_c], [pos_f, pos_c]]
    elif (mov == key.RIGHT and ([pos_f, (pos_c+1)] in data_lab.get("pos_camino"))):
        return [[pos_f, (pos_c+1)], [pos_f, pos_c]]
    elif (mov == key.LEFT and ([pos_f, (pos_c-1)] in data_lab.get("pos_camino"))):
        return [[pos_f, (pos_c-1)], [pos_f, pos_c]]
    else:
        return [[pos_f, pos_c], [pos_f, pos_c]]

def main():
    laberinto, data_lab = cargar_mapa("laberinto.txt")
    pantalla_bienvenida()
    while(data_lab.get("pos_actual_player") != data_lab.get("pos_out")):
        update_mapa(laberinto, data_lab)
        mov = captura_movimiento()
        data_lab["pos_actual_player"], data_lab["pos_anterior_player"] = movimiento(mov, data_lab)
    print("Has salido del laberinto")

main()
