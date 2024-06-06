#GATO MAS AGRESIVO, AGREGUE MOVIMIENTOS DIAGONALES, AGREGUE IMAGENES A PERSONAJES, AGREGUE QUE EL RATON GANE, E IMAGEN GANO RATON
import numpy as np #libreria para trabajar matrices y numeros
import tkinter as tk #libreria para agregar la experiencia virtual y la interfaz grafica
from PIL import Image, ImageTk #agregar imagenes a la interfaz grafica

board_size = 9 # Tablero de juego columnasxfila
board = np.zeros((board_size, board_size)) #tablero vacio

cat_position = (0, 0) #posicion inicial del gato
mouse_position = (board_size - 1, board_size - 1) #hace menos uno para que este en la esquina inferior derecha sin importar el tamaño al que se cambie
mouse_won = False # variable para verificar si el ratón ganó

# Movimiento del gato y ratón
movements = {
    "arriba": (-1, 0), "abajo": (1, 0), "izquierda": (0, -1), "derecha": (0, 1),
    "diagonal arriba izquierda": (-1, -1), "diagonal arriba derecha": (-1, 1),
    "diagonal abajo izquierda": (1, -1), "diagonal abajo derecha": (1, 1)
}

turn = "mouse" #empieza el juego moviendo el raton
mouse_turns_without_caught = 0  # Contador de turnos sin el raton ser atrapado

def is_valid_move(position): #verifica si la posicion esta dentro del tablero
    x, y = position
    return 0 <= x < board_size and 0 <= y < board_size

def get_new_positions(position, movements): #Obtiene todas las posiciones posibles desde una posición dada, según los movimientos válidos.
    new_positions = []
    for move in movements.values():
        new_position = (position[0] + move[0], position[1] + move[1])
        if is_valid_move(new_position):
            new_positions.append(new_position)
    return new_positions

def minimax(cat_position, mouse_position, depth, is_maximizing): #Un algoritmo para que el gato (o ratón) tome la mejor decisión. Evalúa todas las posibles jugadas futuras hasta cierta profundidad (depth).
    if depth == 0 or cat_position == mouse_position:
        return evaluate(cat_position, mouse_position)
    if is_maximizing:
        max_eval = float('-inf')
        for new_cat_position in get_new_positions(cat_position, movements):
            eval = minimax(new_cat_position, mouse_position, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for new_mouse_position in get_new_positions(mouse_position, movements):
            eval = minimax(cat_position, new_mouse_position, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def evaluate(cat_position, mouse_position): #Calcula cuán cerca está el gato del ratón. Si están muy cerca, devuelve un valor muy alto
    distance = abs(cat_position[0] - mouse_position[0]) + abs(cat_position[1] - mouse_position[1])
    if abs(cat_position[0] - mouse_position[0]) <= 1 and abs(cat_position[1] - mouse_position[1]) <= 1:
        return float('inf')  
    return -distance

def best_move(cat_position, mouse_position, depth): #Encuentra la mejor jugada que puede hacer el gato usando el algoritmo minimax.
    if abs(cat_position[0] - mouse_position[0]) <= 1 and abs(cat_position[1] - mouse_position[1]) <= 1:
        return mouse_position
    best_value = float('-inf')
    best_move = None
    for move, delta in movements.items():
        new_position = (cat_position[0] + delta[0], cat_position[1] + delta[1])
        if is_valid_move(new_position):
            move_value = minimax(new_position, mouse_position, depth - 1, False)
            if move_value > best_value:
                best_value = move_value
                best_move = new_position
    return best_move

def draw_board(canvas, cat_position, mouse_position, mouse_caught=False, mouse_won=False): #dibuja el tablero y los personajes
    canvas.delete("all")
    cell_size = 50
    for i in range(board_size):
        for j in range(board_size):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
    x1, y1 = cat_position[0] * cell_size, cat_position[1] * cell_size
    x2, y2 = x1 + cell_size, y1 + cell_size
    if mouse_caught:
        canvas.create_image(x1, y1, anchor=tk.NW, image=cat_caught_image)
    else:
        canvas.create_image(x1, y1, anchor=tk.NW, image=cat_image)

    if not mouse_caught:
        x1, y1 = mouse_position[0] * cell_size, mouse_position[1] * cell_size
        if mouse_won:
            canvas.create_image(x1, y1, anchor=tk.NW, image=mouse_winner_image)
        else:
            canvas.create_image(x1, y1, anchor=tk.NW, image=mouse_image)
        
def move_mouse(direction): #movimientos del raton, verifica si es valido, y si el raton fue atrapado
    global mouse_position, turn, mouse_turns_without_caught, mouse_won
    if turn == "mouse":
        new_position = (mouse_position[0] + movements[direction][0], mouse_position[1] + movements[direction][1])
        if is_valid_move(new_position):
            mouse_position = new_position
            if cat_position == mouse_position:
                draw_board(canvas, cat_position, mouse_position, mouse_caught=True)
                result_label.config(text="Raton lento, el gato te atrapó")
            else:
                mouse_turns_without_caught += 1  # Incrementa el contador
                if mouse_turns_without_caught >= 10:  # Si el ratón juega 10 turnos sin ser atrapado, gana
                    mouse_won = True
                    draw_board(canvas, cat_position, mouse_position, mouse_won=True)
                    result_label.config(text="¡Gato tonto, el ratón ha ganado!")    
                else:
                    draw_board(canvas, cat_position, mouse_position)
                    turn = "cat"  
                    root.after(500, move_cat) 
                    
def skip_turn(): #permite saltar turno al raton porque en un momento con el minimax afecta el juego del gato y con esto se normaliza
    global turn
    if turn == "mouse":
        turn = "cat"
        root.after(500, move_cat)

def move_cat(): #mueve al gato segun mejor posibilidad de jugada, si el gato atrapa al raton muestra mensaje
    global cat_position, turn
    if turn == "cat":
        if abs(cat_position[0] - mouse_position[0]) <= 1 and abs(cat_position[1] - mouse_position[1]) <= 1:
            cat_position = mouse_position
        else:
            new_position = best_move(cat_position, mouse_position, 4)
            if new_position is not None:
                cat_position = new_position
        mouse_caught = cat_position == mouse_position
        draw_board(canvas, cat_position, mouse_position, mouse_caught)
        if mouse_caught:
            result_label.config(text="Raton lento, el gato te atrapó")
        turn = "mouse"

def start_game(): #configura posiciones iniciales y reinicia juego
    global cat_position, mouse_position, turn, mouse_turns_without_caught, mouse_won
    cat_position = (0, 0)
    mouse_position = (board_size - 1, board_size - 1)
    turn = "mouse" 
    mouse_turns_without_caught = 0  # Reinicia el contador
    mouse_won = False  # Reinicia el estado del ratón ganador
    result_label.config(text="")
    draw_board(canvas, cat_position, mouse_position)

# Configurar la ventana principal del juego
root = tk.Tk()
root.title("Juego de Gato y Ratón")

# Cargar las imágenes, gato, raton y gato ganador
cat_img = Image.open("cat.png") #selecciono la imagen
cat_img = cat_img.resize((50, 50), Image.Resampling.LANCZOS)
cat_image = ImageTk.PhotoImage(cat_img)

mouse_img = Image.open("mouse.png") #selecciono la imagen
mouse_img = mouse_img.resize((50, 50), Image.Resampling.LANCZOS)
mouse_image = ImageTk.PhotoImage(mouse_img)

cat_caught_img = Image.open("cat_win.png")
cat_caught_img = cat_caught_img.resize((50, 50), Image.Resampling.LANCZOS)
cat_caught_image = ImageTk.PhotoImage(cat_caught_img)

mouse_winner_img = Image.open("mouse_win.png") #selecciono la imagen del ratón ganador
mouse_winner_img = mouse_winner_img.resize((50, 50), Image.Resampling.LANCZOS)
mouse_winner_image = ImageTk.PhotoImage(mouse_winner_img)

canvas = tk.Canvas(root, width=board_size * 50, height=board_size * 50)
canvas.pack()

control_frame = tk.Frame(root) #crea tablero controles y muestra resultados del juego
control_frame.pack()

btn_up = tk.Button(control_frame, text="Arriba", command=lambda: move_mouse("izquierda"))
btn_up.grid(row=0, column=1)

btn_left = tk.Button(control_frame, text="Izquierda", command=lambda: move_mouse("arriba"))
btn_left.grid(row=1, column=0)

btn_down = tk.Button(control_frame, text="Abajo", command=lambda: move_mouse("derecha"))
btn_down.grid(row=2, column=1)

btn_right = tk.Button(control_frame, text="Derecha", command=lambda: move_mouse("abajo"))
btn_right.grid(row=1, column=2)

btn_diag_up_left = tk.Button(control_frame, text="Diagonal Arriba izquierda", command=lambda: move_mouse("diagonal arriba izquierda"))
btn_diag_up_left.grid(row=0, column=0)

btn_diag_up_right = tk.Button(control_frame, text="Diagonal Abajo izquierda", command=lambda: move_mouse("diagonal arriba derecha"))
btn_diag_up_right.grid(row=2, column=0)

btn_diag_down_left = tk.Button(control_frame, text="Diagonal Arriba derecha", command=lambda: move_mouse("diagonal abajo izquierda"))
btn_diag_down_left.grid(row=0, column=2)

btn_diag_down_right = tk.Button(control_frame, text="Diagonal Abajo Derecha", command=lambda: move_mouse("diagonal abajo derecha"))
btn_diag_down_right.grid(row=2, column=2)

btn_skip_turn = tk.Button(control_frame, text="Saltar turno", command=skip_turn)
btn_skip_turn.grid(row=1, column=1)

result_label = tk.Label(root, text="")
result_label.pack()

start_button = tk.Button(root, text="Reiniciar partida", command=start_game)
start_button.pack()

start_game() #iniciar juego
root.mainloop() 