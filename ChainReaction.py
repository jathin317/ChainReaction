import os

rows = 5
cols = 5

orbs_grid = [[0 for _ in range(cols)] for _ in range(rows)]

occupied = [['n ' for _ in range(cols)] for _ in range(rows)]

def turn(player):
    row = int(input("row: "))
    col = int(input("col: "))

    if not(0 <= row < rows and 0 <= col < cols):
        print("Invalid input")
        turn(player)

    orbs_grid[row][col] += 1
    occupied[row][col] = player

    os.system('clear')
    print_grid()
    if player == 'p2':
        turn('p1')
    else:
        turn('p2')



def print_grid():
    for i in range(rows):
        for j in range(cols):
            print(f" {occupied[i][j]}:{orbs_grid[i][j]} |", end = "")
        print()

print_grid()
turn('p1')