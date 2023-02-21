import math
from copy import deepcopy

from ia.board import Board


class GameState(object):
    def __init__(self, board, over):
        super(GameState, self).__init__()
        self.board = board
        self.over = over
        self.plays = len(self.board) - self.board.board.count('-')
        self.last = (-1, -1)

    def next(self, x, y, val, modo):
        '''        
        Crea una copia del estado, aplica la siguiente jugada a esta copia y la devuelve.  
        '''
        copy = deepcopy(self)
        #print(copy)
        #print("\n")
        # Verifica posibles jugadas
        place = copy.board.get(x, y)
        if place == '-' and val != '-':
            copy.plays += 1
        if place != '-' and val == '-':
            copy.plays -= 1

        copy.board.set(x, y, val)
        copy.last = (x, y)
        copy.over = copy.over or copy._is_over(x, y,modo)
        return copy

    def _is_over(self, x, y,modo):
        '''
        Comprueba si la pieza ingresada terminó el juego.
        Se llama cada vez que se coloca una pieza en el tablero.        
        
        TRUE si la pieza terminó el juego. False en caso contrario.        
        '''
        # Tenga cuidado de no sobrepasar los bordes del tablero
        
        max_x = min(x + modo, self.board.width)
        min_x = max(x - modo, 0)
        max_y = min(y + modo, self.board.height)
        min_y = max(y - modo, 0)

        # No quedan movimientos
        if self.plays == len(self.board):
            return True

        # Row
        row = self.board.row(y)[min_x:max_x]
        if self._is_winner(row,modo):
            return True

        # Col
        col = self.board.col(x)[min_y:max_y]
        if self._is_winner(col,modo):
            return True

        # Diagonals
        ldiag = self.board.ldiag(x + y)
        if len(ldiag) >= modo and self._is_winner(ldiag,modo):
            return True
        rdiag = self.board.rdiag(x + self.board.height - 1 - y)
        if len(rdiag) >= modo and self._is_winner(rdiag,modo):
            return True

        return False

    def _is_winner(self, line,modo):
        '''
        Comprueba si hay una línea ganadora.
        Una línea es ganadora si es 'xxx' o 'ooo'. Tenga en cuenta que esto
        método acepta líneas más largas y las divide en secciones del modo seleccionado es decir hay dos modos 3 - 4
        en raya entonces se divide en secciones de 3 o 4 piezas
        cada.
        
        Verdadero si la línea tiene la línea ganadora. Falso en caso contrario. 
        '''

        lines = len(line) - 2
        for i in range(lines):
            sub_line = line[i:i+modo]
            if sub_line == 'X' * modo or sub_line == 'O' * modo:
                return True
        return False

    @property
    def moves(self):
        '''
        Devuelve un iterador de posibles movimientos.
        Todo espacio del tablero que no sea X u O se considera un Movimiento posible. 
                
        Generador de los posibles movimientos del estado actual del juego.
        '''
        for x, y in self._iter():
            if self.board.get(x, y) == '-':
                yield (x, y)  #yield me retorna valores mediante se obtienen

    @property
    def children(self):
        '''
        '''
        for m in self.moves:
            yield m  #yield me retorna valores mediante se obtienen

    def _iter(self):
        '''
        Iterador creado para generar hijos.
                
        Generador de las coordenadas de la matriz.        
        '''
        order = int(math.sqrt(len(self.board)))
        cycles = order // 2
        if order % 2 == 1: 
            yield (cycles, cycles)
            calc_n = lambda i: i * 2 + 2
            calc_c = lambda i : cycles + 1 + i
        else:
            calc_c = lambda i : cycles + i
            calc_n = lambda i: i * 2 + 1

        for i in range(cycles):
            x = calc_c(i)
            y = calc_c(i)

            n = calc_n(i)

            # left
            for _ in range(n):
                yield (x, y)  #yield me retorna valores mediante se obtienen
                x -= 1

            # down
            for _ in range(n):
                yield (x, y)  #yield me retorna valores mediante se obtienen
                y -= 1

            # right
            for _ in range(n):
                yield (x, y)  #yield me retorna valores mediante se obtienen
                x += 1

            # up
            for _ in range(n):
                yield (x, y)  #yield me retorna valores mediante se obtienen
                y += 1

    def segundotablero(self, x, y, m=5):
        '''
        Devuelve una parte de un tablero de tamaño m por m.

        Si las coordenadas están en el borde del tablero, devolverá el
        talla m situada más hacia la parte interior del tablero.
        
        Tablero parcial alrededor de la coordenada x e y con tamaño m por m.
        '''
        q = m // 2

        max_x = min(self.board.width, x + q + 1)
        max_y = min(self.board.height, y + q + 1)
        min_x = max(0, x - q - 1)
        min_y = max(0, y - q - 1)

        # bordes del tablero
        if min_x == 0:
            max_x = m
        if min_y == 0:
            max_y = m

        if max_x == self.board.width:
            min_x = self.board.width - m
        if max_y == self.board.height:
            min_y = self.board.height - m

        # obtener filas de tablero secundario
        rows = ( self.board.row(i) for i in range(min_y, max_y) )
        # filter the right cols from the rows
        sub_rows = ( row[min_x:max_x] for row in rows )

        board = Board(max_x - min_x, max_y - min_y)
        board.board =''.join(sub_rows)

        return board

    def __str__(self):
        return str(self.board)

    def __eq__(self, g):
        board = self.board == g.board
        over = self.over == g.over
        plays = self.plays == g.plays
        return board and over and plays

    def __hash__(self):
        '''
        Usado para la memoria.
        '''
        return hash(self.board)
