#EN TERMINAL

import numpy as np #biblioteca que proporciona soporte con matrices y amplia funciones para operar con ellas

# Tablero de juego 6x6
board_size = 6 #establezco el tamaño del tablero 
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

def print_board(cat_position, mouse_position): #imprime estado actual del tablero
    printed_board = np.zeros((board_size, board_size)) # ceros para casillas vacias
    printed_board[cat_position[0], cat_position[1]] = 1 #posicion gato
    printed_board[mouse_position[0], mouse_position[1]] = 2 #posicion raton



    for row in printed_board: #Esto proporciona una representación visual del estado actual del tablero con las posiciones del gato y del ratón marcadas.
        print(" ".join(map(str, row)))

def play_game():
    cat_position = (0, 0) #posicion inicial del gato
    mouse_position = (board_size - 1, board_size - 1) #posicion inicial del raton
    
    for turn in range(20): #un bucle for que itera cinco veces. Cada iteración del bucle representa un turno en el juego
        print("Tablero - Gato=1 Raton=2:") #imprime encabezado
        print_board(cat_position, mouse_position) #llama a la funcion imprime posicion del gato y raton

        cat_position = best_move(cat_position, mouse_position, 3) #Llama a la función best_move para determinar el mejor movimiento posible para el gato dado su posición actual (cat_position), la posición actual del ratón (mouse_position), y una profundidad de búsqueda de 3 niveles.
        print(f"\nTurno {turn + 1}: El gato se encuentra en {cat_position}")
        
        if cat_position == mouse_position: #cuando coincidan gato y raton el mensaje que debe poner
            print("Raton lento, el gato te atrapó")
            return
        
        valid_moves = get_new_positions(mouse_position, movements)
        print(f"El ratón está en {mouse_position}. Movimientos válidos: {list(movements.keys())}")
        
        while True:
            move_input = input("Elige la direcciòn (arriba, abajo, izquierda, derecha) pulsa Enter: ").lower()
            if move_input in movements:
                mouse_position = (mouse_position[0] + movements[move_input][0], mouse_position[1] + movements[move_input][1])
                if is_valid_move(mouse_position):
                    break
                else:
                    print("Movimiento inválido. Inténtalo de nuevo.")
            else:
                print("Entrada no válida. Inténtalo de nuevo.")
        
        print(f"El ratón se mueve a {mouse_position}")
        
        if cat_position == mouse_position:
            print("Raton lento, el gato te atrapó")
            return
    
    print("El ratón se ha escapado ¡Gato lento!")

play_game()

