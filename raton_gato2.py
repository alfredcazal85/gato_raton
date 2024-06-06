#CON INTERFAZ GRAFICA
import numpy as np #biblioteca que proporciona soporte con matrices y amplia funciones para operar con ellas
import tkinter as tk #AGREGUEes una biblioteca estándar que proporciona herramientas para crear aplicaciones gráficas de forma sencilla

# Tablero de juego 6x6
board_size = 8 #establezco el tamaño del tablero 
board = np.zeros((board_size, board_size)) #crea la matriz y las llena de ceros para que sepamos donde estan los jugadores

# Posiciones iniciales
cat_position = (0, 0)  # gato empieza en la posición (1, 1) => índice (0, 0)
mouse_position = (board_size - 1, board_size - 1)  # para que el raton siempre este en el extremo inferior derecho, le pone en negativo porque el tablero es positivo

# Movimiento del gato y ratón: arriba, abajo, izquierda, derecha, y la cantidad de celdas que quiero que se muevan
movements = {"arriba": (-1, 0), "abajo": (1, 0), "izquierda": (0, -1), "derecha": (0, 1)}

def is_valid_move(position):
    x, y = position #la posicion de entrada donde esta uno de los personajes, y hace que se encuentren dentro del tablero
    return 0 <= x < board_size and 0 <= y < board_size #verifica que las coordenadas esten dentro del tamaño del tablero

def get_new_positions(position, movements): #funcion que calcula la nueva posicion de los personajes siguiendo reglas
    new_positions = [] #la nueva posicion almacenada, esta lista esta vacia
    for move in movements.values(): #recorre movimientos posibles
        new_position = (position[0] + move[0], position[1] + move[1]) #establece las nuevas posiciones desde la anterior
        if is_valid_move(new_position): #calcula nueva posicion de todas las posibilidades y con las condiciones
            new_positions.append(new_position) #agrega la nueva posicion
    return new_positions

def minimax(position, depth, is_maximizing, mouse_position): #toma posicion del gato, la profundidad del tablero, el turno de quien es, y la posicion del raton
    if depth == 0 or position == mouse_position: #determina la profundidad maxima en el arbol de busqueda y ve si coincide con la del raton
        return evaluate(position, mouse_position) #hace evaluaciones de las posiciones del gato o raton donde se exploran los nodos del árbol de juego para determinar el mejor movimiento para el gato o el ratón, dependiendo de si es el turno del gato (maximizando) o del ratón (minimizando)
    if is_maximizing: #el gato intentará maximizar su evaluación, lo que significa que buscará el movimiento que maximice su puntaje de evaluación.
        max_eval = float('-inf')
        for new_position in get_new_positions(position, movements):
            eval = minimax(new_position, depth - 1, False, mouse_position)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for new_position in get_new_positions(mouse_position, movements):
            eval = minimax(position, depth - 1, True, new_position)
            min_eval = min(min_eval, eval)
        return min_eval

def evaluate(cat_position, mouse_position): #calcula una puntuación heurística para evaluar la posición relativa del gato y el ratón en el tablero
    return - (abs(cat_position[0] - mouse_position[0]) + abs(cat_position[1] - mouse_position[1])) #representa distancia en filas y columnas entre los personajes

def best_move(cat_position, mouse_position, depth): #que se encarga de encontrar el mejor movimiento posible para el gato dado su estado actual, la posición del ratón y la profundidad actual en el árbol de búsqueda.
    best_value = float('-inf')
    best_move = None
    for move, delta in movements.items():
        new_position = (cat_position[0] + delta[0], cat_position[1] + delta[1])
        if is_valid_move(new_position):
            move_value = minimax(new_position, depth - 1, False, mouse_position)
            if move_value > best_value:
                best_value = move_value
                best_move = new_position
    return best_move #establece el mejor movimiento para el gato hasta la actualidad del juego

def draw_board(canvas, cat_position, mouse_position): 
    canvas.delete("all")
    cell_size = 50
    for i in range(board_size):
        for j in range(board_size):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
            if (i, j) == cat_position:
                canvas.create_oval(x1, y1, x2, y2, fill="orange")
            elif (i, j) == mouse_position:
                canvas.create_oval(x1, y1, x2, y2, fill="gray") 

def move_mouse(direction):
    global mouse_position
    new_position = (mouse_position[0] + movements[direction][0], mouse_position[1] + movements[direction][1])
    if is_valid_move(new_position):
        mouse_position = new_position
        draw_board(canvas, cat_position, mouse_position)
        if cat_position == mouse_position:
            result_label.config(text="Raton lento, el gato te atrapó")
        else:
            move_cat()

def move_cat():
    global cat_position
    cat_position = best_move(cat_position, mouse_position, 3)
    draw_board(canvas, cat_position, mouse_position)
    if cat_position == mouse_position:
        result_label.config(text="Raton lento, el gato te atrapó")

def start_game():
    global cat_position, mouse_position
    cat_position = (0, 0)
    mouse_position = (board_size - 1, board_size - 1)
    result_label.config(text="")
    draw_board(canvas, cat_position, mouse_position)

# Configurar la ventana principal
root = tk.Tk()
root.title("Juego de Gato y Ratón")

canvas = tk.Canvas(root, width=board_size * 50, height=board_size * 50)
canvas.pack()

control_frame = tk.Frame(root)
control_frame.pack()

btn_up = tk.Button(control_frame, text="Arriba", command=lambda: move_mouse("izquierda"))
btn_up.grid(row=0, column=1)

btn_left = tk.Button(control_frame, text="Izquierda", command=lambda: move_mouse("arriba"))
btn_left.grid(row=1, column=0)

btn_down = tk.Button(control_frame, text="Abajo", command=lambda: move_mouse("derecha"))
btn_down.grid(row=1, column=1)

btn_right = tk.Button(control_frame, text="Derecha", command=lambda: move_mouse("abajo"))
btn_right.grid(row=1, column=2)

result_label = tk.Label(root, text="")
result_label.pack()

start_button = tk.Button(root, text="Reiniciar partida", command=start_game)
start_button.pack()

start_game()
root.mainloop() 