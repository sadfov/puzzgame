import pygame
import os
from tkinter import Tk, filedialog
from ui_elements import Button

class PreparationScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.background_color = (40, 44, 52)
        
        # Настройки игры
        self.difficulty = "medium"
        self.original_image = None
        
        # Области экрана
        self.control_panel = pygame.Rect(50, 100, 350, 650)
        self.preview_area = pygame.Rect(450, 150, 500, 375)
        
        # Создание UI элементов
        self.create_ui_elements()
        
        # Шрифты
        self.font_large = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 32)
        self.font_small = pygame.font.SysFont('Arial', 24)
        self.font_tiny = pygame.font.SysFont('Arial', 18)
        
        # Загружаем изображение по умолчанию
        self.load_default_image()
        
    def create_ui_elements(self):
        button_width, button_height = 300, 50
        panel_center_x = self.control_panel.centerx
        
        # Заголовок
        self.title_text = "GAME SETUP"
        
        # Кнопки выбора сложности
        self.easy_button = Button(
            panel_center_x - button_width//2, 200, button_width, button_height,
            "Easy (3x3)", (76, 175, 80), lambda: self.set_difficulty("easy")
        )
        
        self.medium_button = Button(
            panel_center_x - button_width//2, 260, button_width, button_height,
            "Medium (4x4)", (33, 150, 243), lambda: self.set_difficulty("medium")
        )
        
        self.hard_button = Button(
            panel_center_x - button_width//2, 320, button_width, button_height,
            "Hard (5x5)", (244, 67, 54), lambda: self.set_difficulty("hard")
        )
        
        self.ultra_button = Button(
            panel_center_x - button_width//2, 380, button_width, button_height,
            "Ultra Hard (10x10)", (148, 0, 211), lambda: self.set_difficulty("ultra")
        )
        
        # Кнопки управления изображением
        self.load_button = Button(
            panel_center_x - button_width//2, 470, button_width, button_height,
            "Load Custom Image", (156, 39, 176), self.load_image_dialog
        )
        
        self.default_button = Button(
            panel_center_x - button_width//2, 530, button_width, button_height,
            "Use Default Image", (255, 152, 0), self.load_default_image
        )
        
        # Кнопки навигации
        self.start_button = Button(
            panel_center_x - button_width//2, 600, button_width, button_height,
            "START GAME", (76, 175, 80), lambda: "start_game"
        )
        
        self.back_button = Button(
            panel_center_x - button_width//2, 660, button_width, button_height,
            "BACK TO MENU", (121, 85, 72), lambda: "back"
        )
        
        self.difficulty_buttons = [
            self.easy_button, self.medium_button, self.hard_button, self.ultra_button
        ]
        
        self.control_buttons = [
            self.load_button, self.default_button, self.start_button, self.back_button
        ]
        
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        
    def load_image_dialog(self):
        root = Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title="Select Image for Puzzle",
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        root.destroy()
        
        if file_path:
            try:
                loaded_image = pygame.image.load(file_path)
                self.original_image = self.optimize_image_size(loaded_image)
                print(f"Custom image loaded: {file_path}")
            except Exception as e:
                print(f"Error loading image: {e}")
                self.load_default_image()
        
    def load_default_image(self):
        """Загружает изображение по умолчанию из папки assets"""
        try:
            # Пытаемся загрузить из папки assets
            assets_dir = "assets"
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir)
                
            default_image_path = os.path.join(assets_dir, "default_puzzle.jpg")
            
            if os.path.exists(default_image_path):
                loaded_image = pygame.image.load(default_image_path)
                self.original_image = self.optimize_image_size(loaded_image)
                print("Default image loaded from assets folder")
            else:
                # Создаем тестовое изображение если файла нет
                self.create_default_image()
                print("Created default image")
                
        except Exception as e:
            print(f"Error loading default image: {e}")
            self.create_default_image()
            
        return "default_loaded"
            
    def create_default_image(self):
        """Создает красивое изображение по умолчанию"""
        surf = pygame.Surface((800, 600))
        
        # Градиентный фон
        for y in range(600):
            r = int(50 + y * 0.2)
            g = int(100 + y * 0.15)
            b = int(150 + y * 0.1)
            pygame.draw.line(surf, (r, g, b), (0, y), (800, y))
        
        # Рисуем геометрические фигуры
        pygame.draw.circle(surf, (255, 223, 0), (200, 150), 70)  # Солнце
        pygame.draw.rect(surf, (46, 125, 50), (100, 350, 600, 200))  # Трава
        pygame.draw.polygon(surf, (139, 69, 19), [(400, 200), (300, 350), (500, 350)])  # Гора
        
        # Дерево
        pygame.draw.rect(surf, (139, 69, 19), (550, 300, 30, 100))  # Ствол
        pygame.draw.circle(surf, (34, 139, 34), (565, 280), 50)  # Крона
        
        # Добавляем текст
        font_large = pygame.font.SysFont('Arial', 80, bold=True)
        font_small = pygame.font.SysFont('Arial', 30)
        
        title = font_large.render("PUZZLE", True, (255, 255, 255))
        subtitle = font_small.render("Default Image", True, (200, 200, 220))
        
        surf.blit(title, (250, 400))
        surf.blit(subtitle, (320, 480))
        
        self.original_image = surf
        
    def optimize_image_size(self, image):
        """Оптимизирует размер изображения для пазла"""
        original_width, original_height = image.get_size()
        target_width, target_height = 800, 600
        
        ratio_original = original_width / original_height
        ratio_target = target_width / target_height
        
        if ratio_original > ratio_target:
            # Широкое изображение - обрезаем по высоте
            new_height = target_height
            new_width = int(original_width * (target_height / original_height))
            scaled = pygame.transform.scale(image, (new_width, new_height))
            crop_x = (new_width - target_width) // 2
            return scaled.subsurface((crop_x, 0, target_width, target_height))
        else:
            # Высокое изображение - обрезаем по ширине
            new_width = target_width
            new_height = int(original_height * (target_width / original_width))
            scaled = pygame.transform.scale(image, (new_width, new_height))
            crop_y = (new_height - target_height) // 2
            return scaled.subsurface((0, crop_y, target_width, target_height))
            
    def handle_event(self, event):
        # Обработка кнопок сложности
        for button in self.difficulty_buttons:
            result = button.handle_event(event)
            if result:
                return None
                
        # Обработка остальных кнопок
        for button in self.control_buttons:
            result = button.handle_event(event)
            if result:
                return result
                
        return None
        
    def update(self):
        # Обновление состояния (пока не нужно)
        pass
        
    def draw(self):
        # Очистка экрана
        self.screen.fill(self.background_color)
        
        # Заголовок
        title_shadow = self.font_large.render(self.title_text, True, (20, 20, 30))
        title_text = self.font_large.render(self.title_text, True, (255, 255, 255))
        self.screen.blit(title_shadow, (self.width//2 - title_text.get_width()//2 + 3, 53))
        self.screen.blit(title_text, (self.width//2 - title_text.get_width()//2, 50))
        
        # Панель управления
        self.draw_control_panel()
        
        # Область предпросмотра
        self.draw_preview_area()
        
    def draw_control_panel(self):
        """Рисует левую панель управления"""
        pygame.draw.rect(self.screen, (30, 30, 40), self.control_panel, border_radius=15)
        pygame.draw.rect(self.screen, (70, 70, 90), self.control_panel, 3, border_radius=15)
        
        # Заголовок панели
        title = self.font_medium.render("Game Settings", True, (220, 220, 240))
        self.screen.blit(title, (self.control_panel.centerx - title.get_width()//2, 120))
        
        # Подзаголовок сложности
        diff_label = self.font_small.render("DIFFICULTY", True, (200, 200, 220))
        self.screen.blit(diff_label, (self.control_panel.centerx - diff_label.get_width()//2, 160))
        
        # Отрисовка кнопок сложности
        for button in self.difficulty_buttons:
            button.draw(self.screen)
            
        # Отображение текущей сложности (ОТДЕЛЬНЫЙ БЛОК)
        current_diff_bg = pygame.Rect(self.control_panel.left + 25, 430, 300, 30)
        pygame.draw.rect(self.screen, (40, 40, 50), current_diff_bg, border_radius=8)
        pygame.draw.rect(self.screen, (90, 90, 110), current_diff_bg, 1, border_radius=8)
        
        current_diff = self.font_tiny.render(f"SELECTED: {self.difficulty.upper()}", True, (255, 255, 255))
        self.screen.blit(current_diff, (self.control_panel.centerx - current_diff.get_width()//2, 435))
        
        # Подзаголовок изображения
        image_label = self.font_small.render("PUZZLE IMAGE", True, (200, 200, 220))
        self.screen.blit(image_label, (self.control_panel.centerx - image_label.get_width()//2, 470))
        
        # Отрисовка остальных кнопок
        for button in self.control_buttons:
            button.draw(self.screen)
        
    def draw_preview_area(self):
        """Рисует область предпросмотра изображения"""
        # Фон области предпросмотра
        pygame.draw.rect(self.screen, (25, 25, 35), self.preview_area, border_radius=15)
        pygame.draw.rect(self.screen, (80, 80, 100), self.preview_area, 3, border_radius=15)
        
        # Заголовок предпросмотра
        preview_text = self.font_medium.render("Image Preview", True, (200, 200, 200))
        self.screen.blit(preview_text, (self.preview_area.centerx - preview_text.get_width()//2, 110))
        
        # Отображение изображения если оно есть
        if self.original_image is not None:
            # Масштабируем изображение для предпросмотра
            preview_img = pygame.transform.scale(self.original_image, (450, 337))
            img_rect = preview_img.get_rect(center=self.preview_area.center)
            self.screen.blit(preview_img, img_rect)
            
            # Информация о сложности для предпросмотра
            if self.difficulty == "easy":
                grid_size = "3x3"
            elif self.difficulty == "medium":
                grid_size = "4x4"
            elif self.difficulty == "hard":
                grid_size = "5x5"
            else:  # ultra
                grid_size = "10x10"
                
            info_text = self.font_small.render(f"Grid: {grid_size} - {self.difficulty.upper()}", True, (255, 255, 255))
            self.screen.blit(info_text, (self.preview_area.centerx - info_text.get_width()//2, 540))