

class Board(object):
    def __init__(self, width, height):
        super(Board, self).__init__()
        self.board = '-' * (width * height)
        self.width = width
        self.height = height

    def row(self, i):
        start = i * self.width
        end = start + self.width
        return self.board[start:end]

    @property
    def rows(self):
        '''
        Generador para todas las filas de tablero.
        '''
        for i in range(self.height):
            yield self.row(i)

    def col(self, i):
        '''
        Returns the ith column of the board.
        '''
        start = i
        end = (self.width * self.height)
        step = self.width
        return self.board[start:end:step]

    @property
    def cols(self):
        '''
        Generador para todas las columnas de tablero.
        '''
        for i in range(self.width):
            yield self.col(i)#yield me retorna valores mediante se obtienen

    def ldiag(self, i):
        '''        
        Devuelve la i diagonal izquierda.
        . Tenga en cuenta que el recuento del índice comienza en la parte superior izquierda.
        
        '''
        h = self.height
        w = self.width
        mx = max(i - h + 1, 0)
        mn = min(i + 1, w)
        gen = ( self.board[(i - q) * w + q] for q in range(mx, mn) )
        return ''.join(gen)

    def rdiag(self, i):
        '''
        Devuelve la i diagonal derecha.
        . Tenga en cuenta que el recuento del índice comienza en la parte superior derecha.
        '''
        h = self.height
        w = self.width
        mx = max(i - h + 1, 0)
        mn = min(i + 1, w)
        gen = ( self.board[(h - i + q - 1) * w + q] for q in range(mx, mn) )
        return ''.join(gen)

    @property
    def diags(self):
        '''
        Generador para todas las diagonales.
        '''
        total = self.height + self.width - 1
        for i in range(total):
            yield self.rdiag(i)
        for i in range(total):
            yield self.ldiag(i)

    def get(self, x, y):
        '''
        Obtiene la coordenada.
            X para el player, O para la IA, - para vacio.
        '''
        return self.board[y * self.width + x]

    def set(self, x, y, val):
        '''
        Mandar el valor a la coordenada.
        '''
        s = y * self.width + x
        self.board = self.board[:s] + val.upper() + self.board[s + 1:]

    def __str__(self):
        '''
        pintar board
        '''
        rows = []
        for row in self.rows:
            line = ' '.join( str(i) for i in row )
            line = line.strip()
            rows.append(line)
        return '\n'.join(rows[::-1])

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.board)

    def __eq__(self, b):
        return self.board == b.board

    def __hash__(self):
        '''
        Se utiliza en la memorización.        
        '''
        return hash(self.board)
