import os
import sys

rows = 5
cols = 5

orbs_grid = [[0 for _ in range(cols)] for _ in range(rows)]

occupied = [['n' for _ in range(cols)] for _ in range(rows)]

def check_treshold(row, col, player):
    if row in [0, rows - 1] and col in [0, cols - 1] and orbs_grid[row][col] == 2:
        explode(row, col, 'corner', player)
    elif (row in [0, rows - 1] or col in [0, cols - 1]) and orbs_grid[row][col] == 3:
        explode(row, col, 'edge', player)
    elif orbs_grid[row][col] == 4:
        explode(row, col, 'middle', player)


def explode(row, col, position, player):
    orbs_grid[row][col] = 0
    occupied[row][col] = 'n'
    if position == 'corner':
        if row == 0 and col == 0:
            orbs_grid[row + 1][col] += 1
            occupied[row + 1][col] = player
            check_treshold(row + 1, col, player)
            orbs_grid[row][col + 1] += 1
            occupied[row][col + 1] = player
            check_treshold(row, col + 1, player)
        elif row == 0 and col == cols - 1:
            orbs_grid[row + 1][col] += 1
            occupied[row + 1][col] = player
            check_treshold(row + 1, col, player)
            orbs_grid[row][col - 1] += 1
            occupied[row][col - 1] = player
            check_treshold(row, col - 1, player)
        elif row == rows - 1 and col == 0:
            orbs_grid[row - 1][col] += 1
            occupied[row - 1][col] = player
            check_treshold(row - 1, col, player)
            orbs_grid[row][col + 1] += 1
            occupied[row][col + 1] = player
            check_treshold(row, col + 1, player)
        elif row == rows - 1 and col == cols - 1:
            orbs_grid[row - 1][col] += 1
            occupied[row - 1][col] = player
            check_treshold(row - 1, col, player)
            orbs_grid[row][col - 1] += 1
            occupied[row][col - 1] = player
            check_treshold(row, col - 1, player)
    elif position == 'edge':
        if row == 0:
            orbs_grid[row][col - 1] += 1
            occupied[row][col - 1] = player
            check_treshold(row, col - 1, player)
            orbs_grid[row][col + 1] += 1
            occupied[row][col + 1] = player
            check_treshold(row, col + 1, player)
            orbs_grid[row + 1][col] += 1
            occupied[row + 1][col] = player
            check_treshold(row + 1, col, player)
        elif row == rows - 1:
            orbs_grid[row][col - 1] += 1
            occupied[row][col - 1] = player
            check_treshold(row, col - 1, player)
            orbs_grid[row][col + 1] += 1
            occupied[row][col + 1] = player
            check_treshold(row, col + 1, player)
            orbs_grid[row - 1][col] += 1
            occupied[row - 1][col] = player
            check_treshold(row - 1, col, player)
        elif col == 0:
            orbs_grid[row + 1][col] += 1
            occupied[row + 1][col] = player
            check_treshold(row + 1, col, player)
            orbs_grid[row][col + 1] += 1
            occupied[row][col + 1] = player
            check_treshold(row, col + 1, player)
            orbs_grid[row - 1][col] += 1
            occupied[row - 1][col] = player
            check_treshold(row - 1, col, player)
        elif col == cols - 1:
            orbs_grid[row + 1][col] += 1
            occupied[row + 1][col] = player
            check_treshold(row + 1, col, player)
            orbs_grid[row][col - 1] += 1
            occupied[row][col - 1] = player
            check_treshold(row, col - 1, player)
            orbs_grid[row - 1][col] += 1
            occupied[row - 1][col] = player
            check_treshold(row - 1, col, player)
    else:
        orbs_grid[row + 1][col] += 1
        occupied[row + 1][col] = player
        check_treshold(row + 1, col, player)
        orbs_grid[row - 1][col] += 1
        occupied[row - 1][col] = player
        check_treshold(row - 1, col, player)
        orbs_grid[row][col + 1] += 1
        occupied[row][col + 1] = player
        check_treshold(row, col + 1, player)
        orbs_grid[row][col - 1] += 1
        occupied[row][col - 1] = player
        check_treshold(row, col - 1, player)



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

print_grid()

current_player = 'p1'

while True:
    turn(current_player)
    if current_player == 'p1':
        current_player = 'p2'
    else:
        current_player = 'p1'