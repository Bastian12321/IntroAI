from game import Game
import tkinter as tk
import ai

game = Game()
computer = ai.AI()

def main():
    for _ in range(20):
        move = computer.move_ai(game.board)
        print(f"AI recommends move: {move}")
        game.play_turn(move)
main()

"""
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
"""
