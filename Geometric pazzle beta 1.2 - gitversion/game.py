import pygame
import random
import time
import os
from puzzle_generator import generate_puzzle_pieces
from ui_elements import Button

class Game:
    def __init__(self, screen, width, height, difficulty, original_image):
        self.screen = screen
        self.width = width
        self.height = height
        self.difficulty = difficulty
        self.original_image = original_image
        self.background_color = (40, 44, 52)
        
        # Области игры
        self.control_panel = pygame.Rect(20, 100, 300, 680)
        self.puzzle_area = pygame.Rect(350, 100, 800, 600)
        self.movement_boundaries = pygame.Rect(350, 100, 800, 600)
        
        # Игровое состояние
        self.pieces = []
        self.state = "playing"  # playing, win
        self.hints_enabled = False
        self.already_saved = False  # Флаг чтобы избежать дублирования сохранения
        
        # Таймер
        self.start_time = time.time()
        self.elapsed_time = 0
        
        # Создание UI элементов
        self.create_ui_elements()
        
        # Шрифты
        self.font_large = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 32)
        self.font_small = pygame.font.SysFont('Arial', 24)
        self.font_tiny = pygame.font.SysFont('Arial', 18)
        
        # Запуск игры
        self.start_new_game()
        
    def create_ui_elements(self):
        button_width, button_height = 260, 50
        panel_center_x = self.control_panel.centerx
        
        # Кнопки управления игрой
        self.shuffle_button = Button(
            panel_center_x - button_width//2, 400, button_width, button_height,
            "Shuffle Pieces", (0, 150, 136), self.shuffle_pieces
        )
        
        self.hint_button = Button(
            panel_center_x - button_width//2, 470, button_width, button_height,
            "Toggle Hints", (255, 193, 7), self.toggle_hints
        )
        
        self.menu_button = Button(
            panel_center_x - button_width//2, 540, button_width, button_height,
            "Main Menu", (121, 85, 72), lambda: "menu"
        )
        
        self.game_buttons = [self.shuffle_button, self.hint_button, self.menu_button]
        
    def start_new_game(self):
        """Начинает новую игру с выбранными настройками"""
        if self.original_image is not None:
            self.pieces = generate_puzzle_pieces(
                self.original_image, 
                self.difficulty, 
                self.movement_boundaries,
                self.puzzle_area
            )
            self.state = "playing"
            self.hints_enabled = False
            self.already_saved = False  # Сбрасываем флаг при новой игре
            self.start_time = time.time()
            print(f"Game started! Difficulty: {self.difficulty}")
            
    def shuffle_pieces(self):
        """Перемешивает фрагменты, которые еще не на своих местах"""
        if self.state == "playing":
            pieces_to_shuffle = [piece for piece in self.pieces if not piece.is_correct]
            
            for piece in pieces_to_shuffle:
                max_x = self.movement_boundaries.width - piece.rect.width
                max_y = self.movement_boundaries.height - piece.rect.height
                
                new_x = random.randint(
                    self.movement_boundaries.left, 
                    self.movement_boundaries.left + max_x
                )
                new_y = random.randint(
                    self.movement_boundaries.top, 
                    self.movement_boundaries.top + max_y
                )
                
                piece.rect.topleft = (new_x, new_y)
                piece.is_dragging = False
            
            # После перемешивания перемещаем все несобранные кусочки в конец списка (наверх)
            for piece in pieces_to_shuffle:
                if piece in self.pieces:
                    self.pieces.remove(piece)
                    self.pieces.append(piece)
            
            print(f"Shuffled {len(pieces_to_shuffle)} pieces")
            
    def toggle_hints(self):
        """Включает/выключает подсказки"""
        self.hints_enabled = not self.hints_enabled
        for piece in self.pieces:
            piece.show_hint = self.hints_enabled
            
    def format_time(self, seconds):
        """Форматирует время в формат MM:SS"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
        
    def save_to_history(self):
        """Сохраняет текущую игру в историю (только один раз)"""
        if self.already_saved:
            return  # Уже сохранили, не сохраняем снова
            
        try:
            from history import HistoryScreen
            # Создаем временный экземпляр HistoryScreen для доступа к методам
            temp_history = HistoryScreen(self.screen, self.width, self.height)
            
            # Получаем количество кусочков
            pieces_count = len(self.pieces)
            
            # Добавляем попытку в историю (передаем оригинальное изображение)
            temp_history.add_attempt(
                difficulty=self.difficulty,
                time_elapsed=self.elapsed_time,
                original_image=self.original_image,
                pieces_count=pieces_count
            )
            
            self.already_saved = True  # Помечаем как сохраненное
            print("Game saved to history")
            
        except Exception as e:
            print(f"Error saving to history: {e}")
        
    def handle_event(self, event):
        if self.state == "playing":
            # Обрабатываем фрагменты в обратном порядке (чтобы верхние были первыми)
            for i, piece in enumerate(reversed(self.pieces)):
                if piece.handle_event(event, self.pieces):
                    # Если фрагмент начали перетаскивать, перемещаем его в конец списка (наверх)
                    if piece.is_dragging:
                        self.pieces.remove(piece)
                        self.pieces.append(piece)
                    break
                    
            # Обработка кнопок управления
            for button in self.game_buttons:
                result = button.handle_event(event)
                if result:
                    return result
                    
        elif self.state == "win":
            # В режиме победы обрабатываем только кнопку меню
            result = self.menu_button.handle_event(event)
            if result:
                return result
                
        return None
        
    def update(self):
        if self.state == "playing":
            # Обновление таймера
            self.elapsed_time = time.time() - self.start_time
            
            # Проверка победы
            all_correct = all(piece.is_correct for piece in self.pieces)
            if all_correct and len(self.pieces) > 0:
                self.state = "win"
                # Автоматически сохраняем в историю при победе (только один раз)
                if not self.already_saved:
                    self.save_to_history()
                
    def draw(self):
        # Очистка экрана
        self.screen.fill(self.background_color)
        
        if self.state == "playing":
            self.draw_game()
        elif self.state == "win":
            self.draw_win_screen()
            
    def draw_game(self):
        # Панель управления
        self.draw_control_panel()
        
        # Область сборки пазла
        pygame.draw.rect(self.screen, (25, 25, 35), self.puzzle_area)
        pygame.draw.rect(self.screen, (80, 80, 100), self.puzzle_area, 2)
        
        # Заголовок области сборки
        puzzle_text = self.font_medium.render("Puzzle Board", True, (200, 200, 200))
        self.screen.blit(puzzle_text, (self.puzzle_area.centerx - puzzle_text.get_width()//2, 70))
        
        # Отрисовка фрагментов пазла - ВСЕГДА рисуем несобранные поверх собранных
        # Сначала рисуем собранные кусочки
        for piece in self.pieces:
            if piece.is_correct:
                piece.draw(self.screen)
        
        # Затем рисуем несобранные кусочки (они будут поверх)
        for piece in self.pieces:
            if not piece.is_correct:
                piece.draw(self.screen)
            
        # Отрисовка кнопок управления
        for button in self.game_buttons:
            button.draw(self.screen)
        
    def draw_control_panel(self):
        """Рисует левую панель управления"""
        pygame.draw.rect(self.screen, (30, 30, 40), self.control_panel, border_radius=15)
        pygame.draw.rect(self.screen, (70, 70, 90), self.control_panel, 3, border_radius=15)
        
        # Заголовок панели управления
        title_text = self.font_medium.render("GAME INFO", True, (220, 220, 240))
        self.screen.blit(title_text, (self.control_panel.centerx - title_text.get_width()//2, 110))
        
        # Блок сложности
        diff_bg = pygame.Rect(self.control_panel.left + 20, 150, 260, 50)
        pygame.draw.rect(self.screen, (35, 35, 45), diff_bg, border_radius=8)
        pygame.draw.rect(self.screen, (70, 70, 90), diff_bg, 2, border_radius=8)
        
        diff_text = self.font_small.render(f"DIFFICULTY: {self.difficulty.upper()}", True, (255, 255, 255))
        self.screen.blit(diff_text, (self.control_panel.centerx - diff_text.get_width()//2, 165))
        
        # Блок таймера
        time_bg = pygame.Rect(self.control_panel.left + 20, 210, 260, 60)
        pygame.draw.rect(self.screen, (35, 35, 45), time_bg, border_radius=10)
        pygame.draw.rect(self.screen, (70, 70, 90), time_bg, 2, border_radius=10)
        
        time_text = self.font_medium.render(self.format_time(self.elapsed_time), True, (255, 255, 255))
        time_label = self.font_tiny.render("TIME ELAPSED", True, (180, 180, 200))
        
        self.screen.blit(time_text, (self.control_panel.centerx - time_text.get_width()//2, 220))
        self.screen.blit(time_label, (self.control_panel.centerx - time_label.get_width()//2, 250))
        
        # Блок прогресса
        pieces_correct = sum(1 for piece in self.pieces if piece.is_correct)
        pieces_total = len(self.pieces)
        
        progress_bg = pygame.Rect(self.control_panel.left + 20, 280, 260, 60)
        pygame.draw.rect(self.screen, (35, 35, 45), progress_bg, border_radius=10)
        pygame.draw.rect(self.screen, (70, 70, 90), progress_bg, 2, border_radius=10)
        
        progress_text = self.font_medium.render(f"{pieces_correct}/{pieces_total}", True, (255, 255, 255))
        progress_label = self.font_tiny.render("PIECES PLACED", True, (180, 180, 200))
        
        self.screen.blit(progress_text, (self.control_panel.centerx - progress_text.get_width()//2, 290))
        self.screen.blit(progress_label, (self.control_panel.centerx - progress_label.get_width()//2, 320))
        
        # Блок подсказок
        hint_bg = pygame.Rect(self.control_panel.left + 20, 350, 260, 40)
        pygame.draw.rect(self.screen, (35, 35, 45), hint_bg, border_radius=8)
        pygame.draw.rect(self.screen, (70, 70, 90), hint_bg, 2, border_radius=8)
        
        if self.hints_enabled:
            hint_text = self.font_small.render("HINTS: ENABLED", True, (255, 193, 7))
        else:
            hint_text = self.font_small.render("HINTS: DISABLED", True, (150, 150, 150))
        self.screen.blit(hint_text, (self.control_panel.centerx - hint_text.get_width()//2, 360))
        
    def draw_win_screen(self):
        # Сначала рисуем обычный игровой экран
        self.draw_control_panel()
        pygame.draw.rect(self.screen, (25, 25, 35), self.puzzle_area)
        pygame.draw.rect(self.screen, (80, 80, 100), self.puzzle_area, 2)
        
        # Отрисовка всех кусочков (собранный пазл)
        for piece in self.pieces:
            piece.draw(self.screen)
        
        # Полупрозрачный оверлей
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Окно победы
        win_width, win_height = 500, 350
        win_x = self.width//2 - win_width//2
        win_y = self.height//2 - win_height//2
        
        win_rect = pygame.Rect(win_x, win_y, win_width, win_height)
        pygame.draw.rect(self.screen, (50, 50, 65), win_rect, border_radius=20)
        pygame.draw.rect(self.screen, (100, 100, 140), win_rect, 3, border_radius=20)
        
        # Текст победы
        congrats = self.font_large.render("Congratulations!", True, (76, 175, 80))
        self.screen.blit(congrats, (win_rect.centerx - congrats.get_width()//2, win_y + 50))
        
        success = self.font_medium.render("Puzzle Completed!", True, (255, 255, 255))
        self.screen.blit(success, (win_rect.centerx - success.get_width()//2, win_y + 120))
        
        # Время
        time_text = self.font_medium.render(f"Time: {self.format_time(self.elapsed_time)}", True, (255, 255, 255))
        self.screen.blit(time_text, (win_rect.centerx - time_text.get_width()//2, win_y + 180))
        
        # Сложность
        diff_text = self.font_small.render(f"Difficulty: {self.difficulty.upper()}", True, (200, 200, 220))
        self.screen.blit(diff_text, (win_rect.centerx - diff_text.get_width()//2, win_y + 230))
        
        # Только кнопка меню
        menu_button_rect = pygame.Rect(win_rect.centerx - 130, win_y + 280, 260, 50)
        self.menu_button.rect = menu_button_rect
        self.menu_button.draw(self.screen)