import pygame
import sys

pygame.font.init()

screen_width, screen_height = 500, 600

Window = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Sudoku game project ")

font = pygame.font.SysFont("comicsans", 40)
font1 = pygame.font.SysFont("comicsans", 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


x = 0
z = 0
diff = 500 / 9
defaultgrid =[
    [0, 2, 6, 0, 0, 0, 8, 1, 0],
    [3, 0, 0, 7, 0, 8, 0, 0, 6],
    [4, 0, 0, 0, 5, 0, 0, 0, 7],
    [0, 5, 0, 1, 0, 7, 0, 9, 0],
    [0, 0, 3, 9, 0, 5, 1, 0, 0],
    [0, 4, 0, 3, 0, 2, 0, 5, 0],
    [1, 0, 0, 0, 3, 0, 0, 0, 2],
    [5, 0, 0, 2, 0, 4, 0, 0, 0],
    [0, 3, 8, 0, 0, 0, 4, 6, 0],
]


def cord(pos):
    global x
    x = pos[0]//diff
    global z
    z = pos[1]//diff
 
def mouse_click_inside_grid(pos):
    grid_start_x = 0
    grid_start_y = int(screen_height * 0.05)
    grid_end_x = 9 * diff
    grid_end_y = 9 * diff + grid_start_y
    
    if grid_start_x <= pos[0] <= grid_end_x and grid_start_y <= pos[1] <= grid_end_y:
        return True
    else:
        return False


def highlightbox():
    for k in range(2):
        pygame.draw.line(Window, BLACK, (x * diff, (z + k)*diff + int(screen_height * 0.05)), (x * diff + diff, (z + k)*diff + int(screen_height * 0.05)), 3)
        pygame.draw.line(Window, BLACK, ((x + k)* diff, z * diff + int(screen_height * 0.05)), ((x + k) * diff, z * diff + diff + int(screen_height * 0.05)), 3) 

def drawlines():
    for i in range(9):
        for j in range(9):
            if defaultgrid[i][j] != 0:
                pygame.draw.rect(Window, (255, 255, 0), (i * diff, j * diff + int(screen_height * 0.05), diff + 1, diff + 1))
                text1 = font.render(str(defaultgrid[i][j]), 1, BLACK)
                text_width, text_height = text1.get_size()
                Window.blit(text1, (i * diff + (diff - text_width) / 2, j * diff + (diff - text_height) / 2 + int(screen_height * 0.05)))
    for l in range(10):
        if l % 3 == 0:
            thick = 3
        else:
            thick = 1
        pygame.draw.line(Window, BLACK, (0, l * diff + int(screen_height * 0.05)), (500, l * diff + int(screen_height * 0.05)), thick)
        pygame.draw.line(Window, BLACK, (l * diff, int(screen_height * 0.05)), (l * diff, 500 + int(screen_height * 0.05)), thick)

def fillvalue(value):
    text1 = font.render(str(value), 1, BLACK)
    Window.blit(text1, (x * diff + 15, z * diff + 15 + int(screen_height * 0.05)))   

def raiseerror():
    text1 = font.render("wrong!", 1, BLACK)
    Window.blit(text1, (int(screen_width * 0.05), int(screen_height * 0.9))) 
def raiseerror1():
    text1 = font.render("wrong ! enter a valid key for the game", 1, BLACK)
    text_width, text_height = text1.get_size()
    Window.blit(text1, (int(screen_width * 0.05), int(screen_height * 0.9 - text_height))) 

def validvalue(m, k, l, value):
    for it in range(9):
        if m[k][it]== value:
            return False
        if m[it][l]== value:
            return False
    it = k//3
    jt = l//3
    for k in range(it * 3, it * 3 + 3):
        for l in range (jt * 3, jt * 3 + 3):
            if m[k][l]== value:
                return False
    return True

def solvegame(defaultgrid, i, j):
     
    while defaultgrid[i][j]!= 0:
        if i<8:
            i+= 1
        elif i == 8 and j<8:
            i = 0
            j+= 1
        elif i == 8 and j == 8:
            return True
    pygame.event.pump()   
    for it in range(1, 10):
        if validvalue(defaultgrid, i, j, it)== True:
            defaultgrid[i][j]= it
            global x, z
            x = i
            z = j
            Window.fill(WHITE)
            drawlines()
            highlightbox()
            pygame.display.update()
            pygame.time.delay(20)
            if solvegame(defaultgrid, i, j)== 1:
                return True
            else:
                defaultgrid[i][j]= 0
            Window.fill(WHITE)
         
            drawlines()
            highlightbox()
            pygame.display.update()
            pygame.time.delay(20)   
    return False 

def gameresult():
    text1 = font1.render("Game finished, Returning to the menu in 5 Seconds", 1, BLACK)
    text_width, text_height = text1.get_size()
    text_x = int((screen_width - text_width) / 2)
    text_y = int(screen_height * 0.95 - text_height)
    Window.blit(text1, (text_x, text_y))

def save_history(seconds, grid):
    with open('./SudokuHistory.txt', 'a+') as f:
        f.write(f'; {seconds}\n')
        for row in grid:
            f.write(' '.join(map(str, row)) + '\n')


def startgame():
    global flag,flag1,flag2,rs,value,defaultgrid,x,z,error
    flag=True  
    flag1 = 0
    flag2 = 0
    rs = 0
    value = 0
    error = 0
    start_ticks = pygame.time.get_ticks()  

    while flag:
        Window.fill(WHITE)
        pygame.draw.rect(Window, WHITE, (0, screen_height - 100, screen_width, 100))
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000 
        font = pygame.font.SysFont(None, 40)  
        if seconds <= 60:
            timer_surface = font.render(f'Time: {seconds} s', True, BLACK)
        else:
            minutes = seconds // 60
            seconds_remainder = seconds % 60
            if minutes <= 120:
                timer_surface = font.render(f'Time: {minutes} m {seconds_remainder} s', True, BLACK)
            else:
                timer_surface = font.render(f'Time: 120+ M', True, BLACK)
        timer_rect = timer_surface.get_rect(bottomleft=(10, screen_height - 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False   
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag1 = 1
                pos = pygame.mouse.get_pos()
                if mouse_click_inside_grid(pos):
                    cord(pos)
                else:
                    pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    flag = False
                if event.key == pygame.K_LEFT:
                    if x > 0:
                        x -= 1
                        flag1 = 1
                if event.key == pygame.K_RIGHT:
                    if x < 8:
                        x += 1
                        flag1 = 1
                if event.key == pygame.K_UP:
                    if z > 0:
                        z -= 1
                        flag1 = 1
                if event.key == pygame.K_DOWN:
                    if z < 8:
                        z += 1
                        flag1 = 1   
                if event.key == pygame.K_1:
                    value = 1
                if event.key == pygame.K_2:
                    value = 2   
                if event.key == pygame.K_3:
                    value = 3
                if event.key == pygame.K_4:
                    value = 4
                if event.key == pygame.K_5:
                    value = 5
                if event.key == pygame.K_6:
                    value = 6
                if event.key == pygame.K_7:
                    value = 7
                if event.key == pygame.K_8:
                    value = 8
                if event.key == pygame.K_9:
                    value = 9 
                if event.key == pygame.K_RETURN:
                    flag2 = 1  
                if event.key == pygame.K_r:
                    rs = 0
                    error = 0
                    flag2 = 0
                    defaultgrid=[
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]
                    ]
                if event.key == pygame.K_d:
                    rs = 0
                    error = 0
                    flag2 = 0
                    defaultgrid  =[
    [0, 2, 6, 0, 0, 0, 8, 1, 0],
    [3, 0, 0, 7, 0, 8, 0, 0, 6],
    [4, 0, 0, 0, 5, 0, 0, 0, 7],
    [0, 5, 0, 1, 0, 7, 0, 9, 0],
    [0, 0, 3, 9, 0, 5, 1, 0, 0],
    [0, 4, 0, 3, 0, 2, 0, 5, 0],
    [1, 0, 0, 0, 3, 0, 0, 0, 2],
    [5, 0, 0, 2, 0, 4, 0, 0, 0],
    [0, 3, 8, 0, 0, 0, 4, 6, 0],
]
        if flag2 == 1:
            if solvegame(defaultgrid , 0, 0)== False:
                error = 1
            else:
                rs = 1
                save_history(seconds, defaultgrid)
                gameresult()     
                pygame.time.delay(5000)
                flag = False  
                defaultgrid  =[
                            [0, 2, 6, 0, 0, 0, 8, 1, 0],
                            [3, 0, 0, 7, 0, 8, 0, 0, 6],
                            [4, 0, 0, 0, 5, 0, 0, 0, 7],
                            [0, 5, 0, 1, 0, 7, 0, 9, 0],
                            [0, 0, 3, 9, 0, 5, 1, 0, 0],
                            [0, 4, 0, 3, 0, 2, 0, 5, 0],
                            [1, 0, 0, 0, 3, 0, 0, 0, 2],
                            [5, 0, 0, 2, 0, 4, 0, 0, 0],
                            [0, 3, 8, 0, 0, 0, 4, 6, 0],
                            ]
            flag2 = 0   
        if value != 0:           
            fillvalue(value)
            if validvalue(defaultgrid , int(x), int(z), value)== True:
                defaultgrid[int(x)][int(z)]= value
                flag1 = 0
            else:
                defaultgrid[int(x)][int(z)]= 0
                raiseerror1()  
            value = 0   
        
        if error == 1:
            raiseerror() 
        drawlines()
        if flag1 == 1:
            highlightbox()      
        clock.tick(60)
        Window.blit(timer_surface, timer_rect)
        pygame.display.update() 


def draw_instructions():
    ins_flag = True
    while ins_flag:
        Window.fill(WHITE)
        text1 = font.render("Instructions", 1, BLACK)
        Window.blit(text1, (int(screen_width * 0.05), int(screen_height * 0.05)))
        text2 = font1.render("1. Use arrow keys to move around the grid", 1, BLACK)
        Window.blit(text2, (int(screen_width * 0.05), int(screen_height * 0.15)))
        text3 = font1.render("2. Use numbers 1-9 to fill in the grid", 1, BLACK)
        Window.blit(text3, (int(screen_width * 0.05), int(screen_height * 0.2)))
        text4 = font1.render("3. Press 'Enter' to check the solution", 1, BLACK)
        Window.blit(text4, (int(screen_width * 0.05), int(screen_height * 0.25)))
        text5 = font1.render("4. Press 'R' to reset the grid", 1, BLACK)
        Window.blit(text5, (int(screen_width * 0.05), int(screen_height * 0.3)))
        text6 = font1.render("5. Press 'D' to reset the grid to default", 1, BLACK)
        Window.blit(text6, (int(screen_width * 0.05), int(screen_height * 0.35)))
        text7 = font1.render("6. Press 'ESC' to go back to the main menu", 1, BLACK)
        Window.blit(text7, (int(screen_width * 0.05), int(screen_height * 0.4)))
        clock.tick(60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ins_flag = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.K_ESCAPE or event.type == pygame.KEYDOWN:
                ins_flag = False

def draw_history():
    try:
        with open('./SudokuHistory.txt', 'r') as f:
            history = f.readlines()
    except FileNotFoundError:
        history = []
    
    scroll_y = 0
    scroll_speed = 5
    scroll_direction = 0
    
    while True:
        Window.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_UP:
                    scroll_direction = -1
                elif event.key == pygame.K_DOWN:
                    scroll_direction = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    scroll_direction = 0
        
        if scroll_direction != 0:
            scroll_y += scroll_speed * scroll_direction
            if scroll_y > 0:
                scroll_y = 0
            elif scroll_y < -((len(history) + 1) * (font1.get_height() + 10) - screen_height):
                scroll_y = -((len(history) + 1) * (font1.get_height() + 10) - screen_height)
        
        if len(history) == 0:
            text = font1.render("No History", True, BLACK)
            text_x = int(screen_width * 0.05)
            text_y = int(screen_height * 0.05) + scroll_y
            Window.blit(text, (text_x, text_y))
        else:
            for i, line in enumerate(history):
                if line.startswith(';'):
                    time_text = line.strip().replace(';', '')
                    minutes = int(time_text) // 60
                    seconds = int(time_text) % 60
                    if minutes <= 120:
                        time_text = f'{minutes}m {seconds}s'
                    else:
                        time_text = '120+'
                    text = font1.render(f'Time: {time_text}', True, BLACK)
                else:
                    grid_text = line.strip().replace(' ', '  ')
                    text = font1.render(grid_text, True, BLACK)
                
                text_x = int(screen_width * 0.05)
                text_y = int(screen_height * 0.05) + i * (text.get_height() + 10) + scroll_y
                Window.blit(text, (text_x, text_y))
        
        exit_text = font1.render("Press ESC to exit", True, BLACK)
        exit_x = int(screen_width * 0.95) - exit_text.get_width()
        exit_y = screen_height - exit_text.get_height() - int(screen_height * 0.05)
        Window.blit(exit_text, (exit_x, exit_y))
        
        pygame.display.update()
        clock.tick(60)

# Menu options
menu_options = ['Start Game', 'Instructions', 'History', 'Exit']
selected_option = 0

def draw_menu(selected_option):
    Window.fill(WHITE)
    title_font = pygame.font.SysFont("comicsans", 64)
    title_text = title_font.render("Sudoku", True, BLACK)
    title_x = screen_width // 2 - title_text.get_width() // 2
    title_y = screen_height // 2 - title_text.get_height() // 2 - (screen_height * 0.27)  # Adjust Y position as needed
    Window.blit(title_text, (title_x, title_y))

    for i, option in enumerate(menu_options):
        color = BLACK if i == selected_option else (100, 100, 100)
        text = font.render(option, True, color)
        x = screen_width // 2 - text.get_width() // 2
        y = screen_height // 2 - text.get_height() // 2 + i * (text.get_height() + 10)
        Window.blit(text, (x, y))
    pygame.display.update()


def main_menu():
    global selected_option
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[selected_option] == 'Exit':
                        running = False
                        pygame.quit()
                        sys.exit()
                    if menu_options[selected_option] == 'Start Game':
                        startgame()
                    if menu_options[selected_option] == 'Instructions':
                        draw_instructions()
                    if menu_options[selected_option] == 'History':
                        draw_history()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(menu_options):
                    x = screen_width // 2 - font.size(option)[0] // 2
                    y = screen_height // 2 - font.size(option)[1] // 2 + i * 50 + int(screen_height * 0.05)
                    if x <= mouse_pos[0] <= x + font.size(option)[0] and y <= mouse_pos[1] <= y + font.size(option)[1]:
                        selected_option = i
                        if menu_options[selected_option] == 'Exit':
                            running = False
                            pygame.quit()
                            sys.exit()
                        if menu_options[selected_option] == 'Start Game':
                            startgame()
                        if menu_options[selected_option] == 'Instructions':
                            draw_instructions()
                        if menu_options[selected_option] == 'History':
                            draw_history()
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(menu_options):
                    x = screen_width // 2 - font.size(option)[0] // 2
                    y = screen_height // 2 - font.size(option)[1] // 2 + i * 50 + int(screen_height * 0.05)
                    if x <= mouse_pos[0] <= x + font.size(option)[0] and y <= mouse_pos[1] <= y + font.size(option)[1]:
                        selected_option = i

                draw_menu(selected_option)

if __name__ == "__main__":
    main_menu()


pygame.quit()    