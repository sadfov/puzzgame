import pygame
from ui_elements import Button, InfoButton

class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.background_color = (40, 44, 52)
        
        # Создание UI элементов
        self.create_ui_elements()
        
        # Шрифты
        self.font_large = pygame.font.SysFont('Arial', 64, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 32)
        self.font_small = pygame.font.SysFont('Arial', 24)
        self.font_tiny = pygame.font.SysFont('Arial', 18)
        
        # Всплывающие подсказки
        self.show_instructions = False
        self.instructions_text = [
            "HOW TO PLAY:",
            "1. Click 'Start' to begin",
            "2. Select difficulty and image", 
            "3. Drag pieces to solve puzzle",
            "",
            "CONTROLS:",
            "- Drag & drop puzzle pieces",
            "- Use hints for guidance",
            "- Shuffle pieces if stuck"
        ]
        
    def create_ui_elements(self):
        button_width, button_height = 300, 60
        
        # Центрируем кнопки по горизонтали
        center_x = self.width // 2
        
        # Основные кнопки меню
        self.start_button = Button(
            center_x - button_width//2, 280, button_width, button_height,
            "START", (76, 175, 80), lambda: "start"
        )
        
        self.history_button = Button(
            center_x - button_width//2, 360, button_width, button_height,
            "HISTORY", (156, 39, 176), lambda: "history"
        )
        
        self.instruction_button = Button(
            center_x - button_width//2, 440, button_width, button_height,
            "INSTRUCTIONS", (33, 150, 243), lambda: "instruction"
        )
        
        self.exit_button = Button(
            center_x - button_width//2, 520, button_width, button_height,
            "EXIT", (244, 67, 54), lambda: "exit"
        )
        
        # Кнопка закрытия инструкций (появляется только при открытых инструкциях)
        self.close_instructions_button = Button(
            center_x - 100, 600, 200, 50,
            "CLOSE", (121, 85, 72), self.toggle_instructions
        )
        
        self.buttons = [
            self.start_button, self.history_button, 
            self.instruction_button, self.exit_button
        ]
        
    def handle_event(self, event):
        if self.show_instructions:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Закрыть инструкции кликом в любом месте
                self.show_instructions = False
                return None
            if self.close_instructions_button.handle_event(event):
                return None
        else:
            for button in self.buttons:
                result = button.handle_event(event)
                if result:
                    return result
        return None
        
    def toggle_instructions(self):
        self.show_instructions = not self.show_instructions
        
    def update(self):
        # Обновление анимаций или других динамических элементов
        pass
        
    def draw(self):
        # Очистка экрана
        self.screen.fill(self.background_color)
        
        # Красивый заголовок с тенью
        title_shadow = self.font_large.render("GEOMETRIC PUZZLES", True, (20, 20, 30))
        title_text = self.font_large.render("GEOMETRIC PUZZLES", True, (255, 255, 255))
        self.screen.blit(title_shadow, (self.width//2 - title_text.get_width()//2 + 4, 154))
        self.screen.blit(title_text, (self.width//2 - title_text.get_width()//2, 150))
        
        # Подзаголовок
        subtitle = self.font_medium.render("Challenge Your Mind", True, (180, 180, 200))
        self.screen.blit(subtitle, (self.width//2 - subtitle.get_width()//2, 220))
        
        # Отрисовка кнопок
        for button in self.buttons:
            button.draw(self.screen)
        
        # Всплывающие инструкции
        if self.show_instructions:
            self.draw_instructions_popup()
                
    def draw_instructions_popup(self):
        """Рисует всплывающее окно с инструкциями"""
        popup_width, popup_height = 500, 400
        popup_x = self.width//2 - popup_width//2
        popup_y = self.height//2 - popup_height//2
        
        # Полупрозрачный фон
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Фон попапа
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.screen, (50, 50, 65), popup_rect, border_radius=20)
        pygame.draw.rect(self.screen, (100, 100, 140), popup_rect, 3, border_radius=20)
        
        # Заголовок
        title = self.font_medium.render("Game Instructions", True, (255, 255, 255))
        self.screen.blit(title, (popup_rect.centerx - title.get_width()//2, popup_y + 30))
        
        # Разделительная линия
        pygame.draw.line(self.screen, (100, 100, 140), 
                        (popup_x + 50, popup_y + 80), 
                        (popup_x + popup_width - 50, popup_y + 80), 2)
        
        # Текст инструкций
        for i, line in enumerate(self.instructions_text):
            if line == "":
                continue
                
            if i == 0:  # Заголовок HOW TO PLAY
                text_color = (255, 193, 7)
                text_size = self.font_small
                y_offset = 100
            elif i == 5:  # Заголовок CONTROLS
                text_color = (255, 193, 7)
                text_size = self.font_small
                y_offset = 240
            else:
                text_color = (220, 220, 240)
                text_size = self.font_tiny
                y_offset = 120 if i < 5 else 260
                
            text_surf = text_size.render(line, True, text_color)
            self.screen.blit(text_surf, (popup_rect.centerx - text_surf.get_width()//2, 
                                       popup_y + y_offset + (i if i < 5 else i-5) * 25))
        
        # Кнопка закрытия
        self.close_instructions_button.draw(self.screen)