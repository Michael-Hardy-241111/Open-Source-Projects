from game import Game
from difficulty import difficulty

def print_board(game: Game):
    """
    Prints the current state of the game board.
    """
    print("+", " -" * game.board.cols, sep="")
    for row in game.board.cells:
        print("|", end=" ")
        row_display = []
        for cell in row:
            if cell.is_opened:
                if cell.is_mine:
                    row_display.append("*")
                elif cell.adjacent_mines > 0:
                    row_display.append(str(cell.adjacent_mines))
                else:
                    row_display.append(" ")
            elif cell.is_flagged == 1:
                row_display.append("F")
            elif cell.is_flagged == 2:
                row_display.append("?")
            else:
                row_display.append("#")
        print(" ".join(row_display))
    print()

def start_cli():
    """
    Main function to handle command-line interaction.
    """
    print("欢迎来到扫雷游戏！")
    print("请选择难度: 1~3")
    level = int(input("请输入难度等级: "))
    if 1 <= level <= 3:
        print("无效难度，请输入1~3。")
        return
    rows, cols, num_mines = difficulty[level]
    game = Game(rows, cols, num_mines)
    while not game.is_game_over:
        print_board(game)
        action = input("请输入操作 (o 行 列 打开 / f 行 列 标记): ").strip().split()
        if len(action) != 3:
            print("无效输入，请重试！")
            continue
        cmd, row, col = action[0], int(action[1]), int(action[2])
        if cmd == "o":
            result = game.open_cell(row, col)
            if result == 2:
                print("游戏结束！你踩到了地雷！")
                break
            elif result == 3:
                print("恭喜你！你赢了！")
                break
        elif cmd == "f":
            game.flag_cell(row, col)
        else:
            print("无效操作，请输入 'o' 或 'f'。")
    print("最终棋盘状态：")
    print_board(game)
    return
