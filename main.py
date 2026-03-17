from game import Game
import tkinter as tk
import ai

game = Game()
computer = ai.AI()
"""
def main():
    for _ in range(20):
        move = computer.move_ai(game.board)
        print(f"AI recommends move: {move}")
        game.play_turn(move)
main()
"""
game = Game()
cells = []


def update_ui():
    for r in range(4):
        for c in range(4):
            value = game.board.grid[r][c]
            text = str(value) if value != 0 else ""
            cells[r][c].config(text=text)


def key_pressed(event, window):
    key = event.keysym.lower()

    key_map = {
        "left": "a",
        "right": "d",
        "up": "w",
        "down": "s",
        "a": "a",
        "d": "d",
        "w": "w",
        "s": "s",
    }

    if key in key_map:
        moved = game.play_turn(key_map[key])

        if moved:
            update_ui()

        if game.won:
            print("You win!")
            window.after(800, window.destroy)  # nicer than instant close

        elif game.game_over:
            print("Game over!")
            window.after(800, window.destroy)


def main():
    global cells

    window = tk.Tk()
    window.title("2048")

    # Create grid
    for r in range(4):
        row = []
        for c in range(4):
            label = tk.Label(
                window,
                text="",
                width=6,
                height=3,
                font=("Arial", 24),
                borderwidth=2,
                relief="solid"
            )
            label.grid(row=r, column=c)
            row.append(label)
        cells.append(row)

    update_ui()

    window.bind("<KeyPress>", lambda event: key_pressed(event, window))
    window.focus_set()

    window.mainloop()


main()
