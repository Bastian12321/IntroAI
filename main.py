from game import Game
import tkinter as tk
import ai

game = Game()
computer = ai.AI()
cells = []
window = None
ai_running = True


def update_ui():
    for r in range(4):
        for c in range(4):
            value = game.board.grid[r][c]
            text = str(value) if value != 0 else ""
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
        ai_running = False  # stop AI if player presses a key
        moved = game.play_turn(key_map[key])

        if moved:
            update_ui()

        check_game_end()


def check_game_end():
    if game.won:
        print("You win!")
        window.after(800, window.destroy)
        return True

    if game.game_over:
        print("Game over!")
        window.after(800, window.destroy)
        return True

    return False


def run_ai():
    global ai_running

    if not ai_running:
        return

    if check_game_end():
        return

    move = computer.move_ai(game.board)

    if move in ("w", "a", "s", "d"):
        moved = game.play_turn(move)

        if moved:
            update_ui()

    if check_game_end():
        return

    window.after(50, run_ai)


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

    window.after(500, run_ai)  # start AI after window opens
    window.mainloop()


main()