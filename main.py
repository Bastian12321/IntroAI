from board import Game
import tkinter as tk

game = Game()

def key_pressed(event):
    key = event.char.lower()   # makes W and w the same

    game.play_turn(key)

def main():
    window = tk.Tk()
    window.title("Key Listener")

    window.bind("<KeyPress>", key_pressed)
    window.focus_set()   # ensures window receives keyboard input

    window.mainloop()

main()