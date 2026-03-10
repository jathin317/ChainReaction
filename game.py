import pygame
import sys
import logic
import bot

pygame.init()

height = 540
width = 360
blocksize = 60


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chain Reaction")

def delay():
    pygame.event.pump()
    draw_board()
    pygame.time.delay(150)

last_move = None
def draw_board():
    screen.fill((0, 0, 0))
    for x in range(0, width, blocksize):
        for y in range(0, height, blocksize):
            rect = pygame.Rect(x, y, blocksize, blocksize)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)

    if last_move:
        r, c = last_move
        highlight_rect = pygame.Rect(c * blocksize, r * blocksize, blocksize, blocksize)
        pygame.draw.rect(screen, (255, 255, 255), highlight_rect, 3)

    for i in range(logic.rows):
        for j in range(logic.cols):
            if logic.orbs_grid[i][j] > 0:
                color = (255, 0, 0) if logic.occupied[i][j] == 'p1' else (0, 255, 0)
                cx = (j * blocksize) + (blocksize // 2)
                cy = (i * blocksize) + (blocksize // 2)
                r = 12

                if logic.orbs_grid[i][j] == 1:
                    pygame.draw.circle(screen, color, (cx, cy), r)
                elif logic.orbs_grid[i][j] == 2:
                    pygame.draw.circle(screen, color, (cx - 8, cy), r)
                    pygame.draw.circle(screen, color, (cx + 8, cy), r)
                elif logic.orbs_grid[i][j] >= 3:
                    pygame.draw.circle(screen, color, (cx - 8, cy + 6), r)
                    pygame.draw.circle(screen, color, (cx + 8, cy + 6), r)
                    pygame.draw.circle(screen, color, (cx, cy - 8), r)

    pygame.display.update()

running = True
game_over = False

draw_board()

while running:
    #Human Turn(P1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and logic.current_player == 'p1' and not game_over:
            x, y = event.pos
            col, row = x // blocksize, y // blocksize
            
            if logic.occupied[row][col] in ['p1', 'n']:
                last_move = (row, col)
                print(f"Human: {row, col}")

                logic.orbs_grid[row][col] += 1
                logic.occupied[row][col] = 'p1'
                
                # Trigger logic explosions and pass the drawing callback!
                logic.check_treshold(row, col, 'p1', animate_callback=delay)
                
                logic.no_of_turns += 1
                logic.current_player = 'p2'
                draw_board()
                
                if logic.isCompleted():
                    print("Game Over! P1 Wins!")
                    game_over = True

    #Bot Turn (P2)
    if logic.current_player == 'p2' and not game_over:
        pygame.display.set_caption("Chain Reaction - Bot is thinking...")
        
        b_row, b_col = bot.get_best_move(logic.orbs_grid, logic.occupied, 'p2')

        last_move = (b_row, b_col)
        print(f"Bot: {b_row, b_col}")
        
        logic.orbs_grid[b_row][b_col] += 1
        logic.occupied[b_row][b_col] = 'p2'

        draw_board()
        pygame.time.delay(500)
        

        logic.check_treshold(b_row, b_col, 'p2', animate_callback=delay)
        
        logic.no_of_turns += 1
        logic.current_player = 'p1'
        pygame.display.set_caption("Chain Reaction - Your Turn")
        draw_board()
        
        if logic.isCompleted():
            print("Game Over! Bot Wins!")
            game_over = True

pygame.quit()
sys.exit()