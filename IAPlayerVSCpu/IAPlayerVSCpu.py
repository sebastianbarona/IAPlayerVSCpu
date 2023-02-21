from tkinter import messagebox
from traceback import print_tb
from turtle import xcor
from ia.board import Board
from ia.heuristic import utility, heuristic
from ia.gamestate import GameState
from ia.minimax import MiniMax
from ia.heuristic4 import heuristic4
from cgitb import text
from functools import partial

from tkinter import *

tamano=0
turno=1;
board = Board(10, 10)
game = GameState(board, False)

                                                   

class MainFrame(Frame):
    def __init__(self, parent, *args, **kwargs,):
        super().__init__(parent, *args, **kwargs)
        b=""
        global turno
        global game

        for r in range(10): 
            for c in range(9,-1,-1):
                verr = 0 + c
                verc = 9 - r
                b = f'{verr} {verc}'                 
                new_button = Button(self, text=str(b), borderwidth=1, height=2, width=4, font=1, fg="white" ,bg='#17202A')
                new_button.grid(row=r, column=c)
                new_button["command"] = partial(self.press, new_button, verr, verc,turno)                 

        if turno == 1:
           turno=0;
           x, y = minimax.search(game,tamano)    
           game = game.next(x, y, 'X',tamano)
           print(game)
           print()    
            
           new_button = Button(self, borderwidth=1, height=2, width=4, font=1,bg='#17202A' )
           new_button.configure( text="X",fg="#E74C3C",font=2)
           new_button.grid(row=x, column=y)
           


         ##print("0 1 2 3 4 5 6 7 8 9")

    def press(self, btn, row ,col,turn):
        global turno
        global game
        
        if turno == 0:
            x = row
            y = col
            btn.configure( text="O",fg="#14AAF5")
        
            if len(datosrepetidos) == 0:            
               game = game.next(x, y, 'O', tamano)  
               turno = 1
            else:
                if datosrepetidos.count([x,y]):            
                   print("Casilla Ocupada, Volver A Digitar")
                else:
                  game = game.next(x, y, 'O', tamano)       
                  datosrepetidos.append([x,y])
                  turno=1;

            print(game)
            print()    
            

        else:
            print(row, col)        
            btn.configure( text="X",fg="#E74C3C",font=2)
            turno=0;
            print(game)
            print()    
            x, y = minimax.search(game,tamano)    
            game = game.next(x, y, 'X',tamano)
            
            datosrepetidos.append([x,y])
            print(game)
    
            print(f'Turno player ({x}, {y})')

        if game.over:
           if turno == 1:                                 
                messagebox.showinfo("Winner", "Player") # t�tulo, mensaje
  
                Button(self.app, text = "Aceptar").pack()
                        
                print('Game Over :C')
                self.MainFrame.destroy()
           else:
                messagebox.showinfo("Winner", "IA") # t�tulo, mensaje
  
                Button(self.app, text = "Aceptar").pack()
                        
                print('Game Over :C')
                self.MainFrame.destroy()
          
        else:
               turno=0;
               x, y = minimax.search(game,tamano)    
               game = game.next(x, y, 'X',tamano)
               print(game)
               print()    
            
               new_button = Button(self, borderwidth=1, height=2, width=4, font=1,bg='#17202A' )
               new_button.configure( text="X",fg="#E74C3C",font=2)
               new_button.grid(row=x, column=y)

               if game.over:
                   if turno == 1:                                 
                        messagebox.showinfo("Winner", "Player") # t�tulo, mensaje
  
                        Button(self.app, text = "Aceptar").pack()
                        
                        print('Game Over :C')
                        self.MainFrame.destroy()
                   else:
                        messagebox.showinfo("Winner", "IA") # t�tulo, mensaje
  
                        Button(self.app, text = "Aceptar").pack()
                        
                        print('Game Over :C')
                        self.MainFrame.destroy()
         
           
        
        

    def iniciar():
        root = Tk()
        MainFrame(root).pack(side="top", fill="both", expand=True)
        root.mainloop()
        

class GUI:
    def __init__(self):    
        self.app = Tk()
        self.app.resizable(width=False, height=False)
        self.app.title("TRIQUI")

        self.miimagen=PhotoImage(file="triqui.png")

        self.primer_frame = Frame(self.app,height=600,width=1030,bg="BLACK",)
        self.primer_frame.pack()

        self.fondo=Label(self.primer_frame,image=self.miimagen)
        self.fondo.place(x=0,y=10)

        menu=Button(self.fondo,text="Modo 3",height=3,width=55, command=lambda: self.selectMode(3))
        menu.place(x=300,y=445)

        menu=Button(self.fondo,text="Modo 4",height=3,width=55, command=lambda: self.selectMode(4))
        menu.place(x=300,y=245)

    
    def mainloop(self):
        self.app.mainloop()

        
    def selectMode(self,value):
        print(value)
        global tamano
        tamano = value        
        self.app.destroy()
                

    def mainloop(self):
        self.app.mainloop()

GUI().mainloop()

#tamanon = int(input("Digite si desea jugar 3 o 4 en raya\n"))
## Empty board


if tamano == 3:
   minimax = MiniMax(utility, heuristic, 2)
else:    
   minimax = MiniMax(utility, heuristic4, 2)

datosrepetidos = []

print('IA Analizando')

MainFrame.iniciar()              
                
                     
            
