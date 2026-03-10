import copy

rows = 9
cols = 6

def evaluation(orbs_grid, occupied, player):
    my_score = 0
    opponent_score = 0
    opponent = 'p1' if player == 'p2' else 'p2'

    for i in range(rows):
        for j in range(cols):
            if (i in [0, rows - 1] and j in [0, cols - 1]):
                weight = 5 # Corner
            elif (i in [0, rows - 1] or j in [0, cols - 1]):
                weight = 3 # Edge
            else:
                weight = 1 # Center
            if occupied[i][j] == player:
                my_score += orbs_grid[i][j] * weight
            elif occupied[i][j] == opponent:
                opponent_score += orbs_grid[i][j] * weight

    return my_score - opponent_score

def get_best_move(orbs_grid, occupied, player, depth = 1):
    alpha = float('-inf')
    beta = float('inf')
    best_score = float('-inf')
    best_move = (-1, -1)
    for i in range(rows):
        for j in range(cols):
            if occupied[i][j] == player or occupied[i][j] == 'n':

                new_orbs_grid = copy.deepcopy(orbs_grid)
                new_occupied = copy.deepcopy(occupied)

                new_orbs_grid[i][j] += 1
                new_occupied[i][j] = player

                bot_check_treshold(new_orbs_grid, new_occupied, i, j, player)

                score = min_value(new_orbs_grid, new_occupied, player, depth - 1, alpha, beta)

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

                    alpha = max(alpha, best_score)
    return best_move

def max_value(orbs_grid, occupied, player, depth, alpha, beta):
    if depth == 0:
        return evaluation(orbs_grid, occupied, player)
    v = float('-inf')

    for i in range(rows):
        for j in range(cols):
            if occupied[i][j] == player or occupied[i][j] == 'n':
                new_orbs_grid = copy.deepcopy(orbs_grid)
                new_occupied = copy.deepcopy(occupied)

                new_orbs_grid[i][j] += 1
                new_occupied[i][j] = player
                bot_check_treshold(new_orbs_grid, new_occupied, i, j, player)

                v = max(v, min_value(new_orbs_grid, new_occupied, player, depth - 1, alpha, beta))

                alpha = max(alpha, v)
                if alpha >= beta:
                    return v
    return v

def min_value(orbs_grid, occupied, player, depth, alpha, beta):
    if depth == 0:
        return evaluation(orbs_grid, occupied, player)
    v = float('inf')

    opponent = 'p1' if player == 'p2' else 'p2'

    for i in range(rows):
        for j in range(cols):
            if occupied[i][j] == opponent or occupied[i][j] == 'n':
                new_orbs_grid = copy.deepcopy(orbs_grid)
                new_occupied = copy.deepcopy(occupied)

                new_orbs_grid[i][j] += 1
                new_occupied[i][j] = opponent
                bot_check_treshold(new_orbs_grid, new_occupied, i, j, opponent)

                v = min(v, max_value(new_orbs_grid, new_occupied, player, depth - 1, alpha, beta))

                beta = min(beta, v)
                if alpha >= beta:
                    return v
    return v


def bot_check_treshold(orbs_grid, occupied, row, col, player):
    if row in [0, rows - 1] and col in [0, cols - 1] and orbs_grid[row][col] >= 2:
        bot_explode(orbs_grid, occupied, row, col, player)
    elif (row in [0, rows - 1] or col in [0, cols - 1]) and orbs_grid[row][col] >= 3:
        bot_explode(orbs_grid, occupied, row, col, player)
    elif orbs_grid[row][col] >= 4:
        bot_explode(orbs_grid, occupied, row, col, player)


def bot_explode(orbs_grid, occupied, row, col, player):
    orbs_grid[row][col] = 0
    occupied[row][col] = 'n'
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for drow, dcol in directions:
        n_row = row + drow
        n_col = col + dcol

        if 0 <= n_row < rows and 0 <= n_col < cols:
            orbs_grid[n_row][n_col] += 1
            occupied[n_row][n_col] = player
            bot_check_treshold(orbs_grid, occupied, n_row, n_col, player)