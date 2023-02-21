import functools

from itertools import product, chain
from collections import defaultdict

# Genera todos los campos disponibles para X(Player)
ONLY_X = { ''.join(k): 3**k.count('X') for k in product('X-', repeat=3) } #product es una funcion de itertools q realiza el bucle for anidado
ONLY_X['XXX'] = 3**9
del ONLY_X['---']

# Genera todos los campos disponibles para O(IA)
ONLY_O = { ''.join(k): -3**k.count('O') for k in product('O-', repeat=3) }
ONLY_O['OOO'] = -3**9
del ONLY_O['---']

# Crea un dic que devuelve 0 para todo
VALUE_TABLE = defaultdict(lambda: 0)

# Agrega los valores generados antes
VALUE_TABLE.update(ONLY_X)
VALUE_TABLE.update(ONLY_O)

# Por definición, esta no es una línea abierta
VALUE_TABLE['---'] = 0


# Tamaño de la segunda tabla para la función heurística
SUB_BOARD_SIZE = 5


def valor_linea(line):
    '''
    Obtiene el valor de la línea.
    '''
    return VALUE_TABLE[line]


@functools.lru_cache(maxsize=None)
def Valores_lineas(board):
    '''
    Esta función itera sobre todas las líneas posibles de un tablero y devuelve
    los valores de cada línea.

    El lru_cache memoriza.Asi Evitamos Crear Varios Tables Ya Que se ejecuta una vez por tablero.   

    Suma de todos los valores de línea.    
    '''
    
    result = 0
    iterators = [ board.rows, board.cols, board.diags ]
    combined = chain(*iterators)
    for line in combined:
        line_len = len(line)
        if line_len < 3:
            continue
        for i in range(line_len - 2):
            sub_line = line[i:i+3]
            result += valor_linea(sub_line)
    return result


def heuristic(game):
    '''
    Devuelve el valor heurístico de algún juego.

    Toma una parte del tablero original y aplica la misma función del
    utilidad en ella.
        
    '''
    x, y = game.last
    board = game.segundotablero(x, y, SUB_BOARD_SIZE)
    return Valores_lineas(board)


def utility(game):
    '''
     Calcula el valor heurístico.

    Itera sobre las filas, columnas y diagonales. En el orden respectivo.    
    Suma de todos los valores de línea dividida por el número total de jugadas.    
    '''
    result = Valores_lineas(game.board)
    return result / game.plays

