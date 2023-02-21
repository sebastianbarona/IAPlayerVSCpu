from math import inf as INFINITY


class MiniMax(object):
    def __init__(self, util, heur, max_prof=3):
        super(MiniMax, self).__init__()
        self.utility = util
        self.heuristic = heur
        self.max_prof = max_prof

    def _min_play(self, state, alpha, beta, prof,modo):
        #El juego terminado tiene prioridad sobre la profundidad
        if state.over:
            return self.utility(state)

        if prof >= self.max_prof:
            return self.heuristic(state)

        #traigo el estado actual de la IA que son caracter O
        states = ( state.next(x, y, 'O',modo) for x, y in state.children )
        #Se pasa al metodo Min Ya Que Se Busca Que La IA Gane         
        scores = ( self._max_play(g, alpha, beta, prof + 1,modo) for g in states )
        value = INFINITY

        for score in scores:
            value = min(value, score)
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def _max_play(self, state, alpha, beta, prof,modo):
        #El juego tiene prioridad sobre la profundidad.
        if state.over:
            return self.utility(state)

        if prof >= self.max_prof:
            return self.heuristic(state)

        #traigo el estado actual del player que son caracter X
        states = ( state.next(x, y, 'X',modo) for x, y in state.children )
        #Se pasa al metodo Min Ya Que Se Busca Que La IA Gane 
        scores = ( self._min_play(g, alpha, beta, prof + 1,modo) for g in states )

        value = -INFINITY

        for score in scores:
            value = max(value, score)
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def search(self, state,modo):
        '''
        Realiza la búsqueda de la mejor jugada del estado actual del jugador.
        '''
        best_move = None
        best_score = -INFINITY
        beta = INFINITY

        for x, y in state.children:
            copy = state.next(x, y, 'X',modo)
            score = self._min_play(copy, best_score, beta, 0,modo)
            if score > best_score:
                best_move = (x, y)
                best_score = score
        return best_move
