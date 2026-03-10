current_player = 'p1'
no_of_turns = 0
rows = 9
cols = 6

orbs_grid = [[0 for _ in range(cols)] for _ in range(rows)]

occupied = [['n' for _ in range(cols)] for _ in range(rows)]

def check_treshold(row, col, player, animate_callback=None):
    if row in [0, rows - 1] and col in [0, cols - 1] and orbs_grid[row][col] >= 2:
        explode(row, col, player, animate_callback)
    elif (row in [0, rows - 1] or col in [0, cols - 1]) and orbs_grid[row][col] >= 3:
        explode(row, col, player, animate_callback)
    elif orbs_grid[row][col] >= 4:
        explode(row, col, player, animate_callback)


def explode(row, col, player, animate_callback):
    orbs_grid[row][col] = 0
    occupied[row][col] = 'n'

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for drow, dcol in directions:
        n_row = row + drow
        n_col = col + dcol
        if 0 <= n_row < rows and 0 <= n_col < cols:
            orbs_grid[n_row][n_col] += 1
            occupied[n_row][n_col] = player

    if animate_callback:
        animate_callback()

    for drow, dcol in directions:
        n_row = row + drow
        n_col = col + dcol

        if 0 <= n_row < rows and 0 <= n_col < cols:
            check_treshold(n_row, n_col, player, animate_callback)
    
"""
def turn(player):
    while True:
        row = int(input("row: "))
        col = int(input("col: "))

        if not(0 <= row < rows and 0 <= col < cols and (player == occupied[row][col] or occupied[row][col] == 'n')):
            print("Invalid input, try again")
            continue
        break

    orbs_grid[row][col] += 1
    occupied[row][col] = player

    check_treshold(row, col, player)

    os.system('clear')
    print_grid()

def print_grid():
    for i in range(rows):
        for j in range(cols):
            print(f" {occupied[i][j]}:{orbs_grid[i][j]} |", end = "")
        print()
"""


def isCompleted():
    if no_of_turns <= 2:
        return False
    
    p1_present = False
    p2_present = False

    for i in range(rows):
        for j in range(cols):
            if occupied[i][j] == 'p1':
                p1_present = True
            elif occupied[i][j] == 'p2':
                p2_present = True
    return not(p1_present and p2_present)

"""
while True:
    if current_player == 'p1':
        turn(current_player)
    else:
        b_row, b_col = bot.get_best_move(orbs_grid, occupied, 'p2')

        orbs_grid[b_row][b_col] += 1
        occupied[b_row][b_col] = 'p2'

        check_treshold(b_row, b_col, 'p2')
        os.system('clear')
        print_grid()
    no_of_turns += 1

    if isCompleted():
        print(f"Game Over! {current_player} WINS")

    if current_player == 'p1':
        current_player = 'p2'
    else:
        current_player = 'p1'

"""