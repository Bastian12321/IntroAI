from game import Game
import tkinter as tk
import ai
import mcts

game = Game()
computer = ai.AI()
computer2 = mcts.MCTS()
cells = []
window = None
ai_running = True


def update_ui():
    for r in range(4):
        for c in range(4):
            exp = game.board.grid[r][c]
            text = str(2 ** exp) if exp != 0 else ""
            cells[r][c].config(text=text)


def key_pressed(event):
    global ai_running

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
        ai_running = False
        moved = game.play_turn(key_map[key])

        if moved:
            update_ui()


def run_ai():
    global ai_running

    if not ai_running:
        print("AI stopped. Player took control.")
        return

    move = computer2.move_ai(game.board)
    
    if move is None:
        window.after(800, window.destroy)
        return

    if move in ("w", "a", "s", "d"):
        moved = game.play_turn(move)

        if moved:
            update_ui()

    window.after(1, run_ai)


def main():
    global cells, window

    window = tk.Tk()
    window.title("2048 AI")

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
            label.grid(row=r, column=c, padx=2, pady=2)
            row.append(label)
        cells.append(row)

    update_ui()

    window.bind("<KeyPress>", key_pressed)
    window.focus_set()

    window.after(1, run_ai)
    window.mainloop()


main()