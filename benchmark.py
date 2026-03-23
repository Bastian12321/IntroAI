import time
from game import Game, Board
import expectimax
import mcts


def fresh_game():
    """Create a Game without triggering pretty_print spam."""
    g = Game.__new__(Game)
    g.board = Board()
    g.score = 0
    g.won = False
    g.game_over = False
    return g


def run_benchmark(ai_player, num_games=10, label="AI"):
    wins = 0
    scores = []
    max_tiles = []
    move_times = []

    for game_num in range(1, num_games + 1):
        game = fresh_game()

        while True:
            if not game.board.can_move():
                break

            t0 = time.perf_counter()
            move = ai_player.move_ai(game.board)
            move_times.append(time.perf_counter() - t0)

            if move is None:
                break

            result = game.play_turn(move)
            # play_turn returns False (no move) or True (moved/game over)
            if not result:
                # No valid move found — try remaining directions
                stuck = True
                for fallback in ("w", "a", "s", "d"):
                    if fallback != move and game.play_turn(fallback):
                        stuck = False
                        break
                if stuck:
                    break

            if game.game_over:
                break

        max_exp = game.board.max_exponent()
        max_tile = 2 ** max_exp if max_exp > 0 else 0
        won = max_tile >= 2048

        if won:
            wins += 1

        scores.append(game.score)
        max_tiles.append(max_tile)

        status = "WIN!" if won else f"max={max_tile}"
        print(f"  [{label}] Game {game_num:2d}: score={game.score:>7,}  {status}")

    return {
        "label": label,
        "wins": wins,
        "num_games": num_games,
        "win_rate": wins / num_games * 100,
        "avg_score": sum(scores) / len(scores),
        "avg_max_tile": sum(max_tiles) / len(max_tiles),
        "avg_move_ms": sum(move_times) / len(move_times) * 1000,
        "max_tiles": max_tiles,
        "scores": scores,
    }


def tile_bar(max_tiles, tile):
    count = sum(1 for t in max_tiles if t == tile)
    return f"{'#' * count:<20}  ({count})"


def print_results(results):
    sep = "=" * 58
    print(f"\n{sep}")
    print(f"{'  BENCHMARK RESULTS':^58}")
    print(sep)

    for r in results:
        print(f"\n  >> {r['label']}")
        print(f"  {'-' * 52}")
        print(f"  Win rate      :  {r['win_rate']:5.1f}%   ({r['wins']}/{r['num_games']})")
        print(f"  Avg score     :  {r['avg_score']:>10,.1f}")
        print(f"  Avg max tile  :  {r['avg_max_tile']:>10,.0f}")
        print(f"  Avg move time :  {r['avg_move_ms']:>10.3f} ms")

        all_tiles = sorted(set(r["max_tiles"]), reverse=True)
        print(f"\n  Tile distribution:")
        for tile in all_tiles:
            bar = tile_bar(r["max_tiles"], tile)
            print(f"    {tile:>5}  {bar}")

    print(f"\n{sep}\n")

    # Head-to-head summary
    if len(results) == 2:
        a, b = results
        print("  Head-to-head summary")
        print(f"  {'-' * 52}")
        winner = a["label"] if a["win_rate"] >= b["win_rate"] else b["label"]
        faster = a["label"] if a["avg_move_ms"] <= b["avg_move_ms"] else b["label"]
        higher = a["label"] if a["avg_score"] >= b["avg_score"] else b["label"]
        print(f"  More wins    ->  {winner}")
        print(f"  Higher score ->  {higher}")
        print(f"  Faster moves ->  {faster}")
        print()


if __name__ == "__main__":
    NUM_GAMES = 10

    players = [
        (expectimax.ExpectiMax(), "Expectimax")
        (mcts.MCTS(250, 5),             "MCTS-50"),
        (mcts.MCTS(500, 5),             "MCTS-100"),
        (mcts.MCTS(750, 5),             "MCTS-250"),
    ]

    all_results = []
    for player, label in players:
        print(f"\nRunning {NUM_GAMES} games -- {label} ...")
        result = run_benchmark(player, num_games=NUM_GAMES, label=label)
        all_results.append(result)

    print_results(all_results)