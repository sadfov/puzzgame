import pygame
import sys
import os
from game import Game
from menu import MainMenu
from preparation import PreparationScreen
from history import HistoryScreen

def main():
    # Инициализация Pygame
    pygame.init()
    
    # Настройки окна
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Geometric Puzzles")
    
    # Состояния приложения
    current_screen = "menu"  # menu, preparation, game, history
    game = None
    menu = MainMenu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    preparation = None
    history = None
    
    # Главный игровой цикл
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Обработка событий в зависимости от текущего экрана
            if current_screen == "menu":
                result = menu.handle_event(event)
                if result == "start":
                    preparation = PreparationScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                    current_screen = "preparation"
                elif result == "history":
                    history = HistoryScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                    current_screen = "history"
                elif result == "exit":
                    running = False
                elif result == "instruction":
                    menu.toggle_instructions()
                    
            elif current_screen == "preparation":
                result = preparation.handle_event(event)
                if result == "start_game":
                    game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 
                               preparation.difficulty, preparation.original_image)
                    current_screen = "game"
                elif result == "back":
                    current_screen = "menu"
                    
            elif current_screen == "game":
                result = game.handle_event(event)
                if result == "menu":
                    current_screen = "menu"
                    game = None
                    
            elif current_screen == "history":
                result = history.handle_event(event)
                if result == "back":
                    current_screen = "menu"
                elif result == "view_attempt":
                    # Просмотр конкретной попытки
                    pass
        
        # Обновление состояния в зависимости от текущего экрана
        if current_screen == "menu":
            menu.update()
        elif current_screen == "preparation":
            preparation.update()
        elif current_screen == "game":
            game.update()
        elif current_screen == "history":
            history.update()
        
        # Отрисовка
        screen.fill((40, 44, 52))  # Очистка экрана
        
        if current_screen == "menu":
            menu.draw()
        elif current_screen == "preparation":
            preparation.draw()
        elif current_screen == "game":
            game.draw()
        elif current_screen == "history":
            history.draw()
            
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()