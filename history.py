import pygame
import os
import json
import datetime
import shutil
from ui_elements import Button

class HistoryScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.background_color = (40, 44, 52)
        
        # Области экрана
        self.control_panel = pygame.Rect(50, 100, 350, 600)
        self.history_area = pygame.Rect(450, 100, 700, 600)
        
        # Данные истории
        self.history_data = []
        self.selected_attempt = None
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Папка для истории
        self.history_dir = "game_history"
        self.previews_dir = os.path.join(self.history_dir, "previews")
        
        # Создание UI элементов
        self.create_ui_elements()
        
        # Шрифты
        self.font_large = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 32)
        self.font_small = pygame.font.SysFont('Arial', 24)
        self.font_tiny = pygame.font.SysFont('Arial', 18)
        
        # Создаем папки если их нет
        self.create_directories()
        
        # Загрузка истории
        self.load_history()
        
    def create_directories(self):
        """Создает необходимые папки для истории"""
        os.makedirs(self.history_dir, exist_ok=True)
        os.makedirs(self.previews_dir, exist_ok=True)
        
    def create_ui_elements(self):
        button_width, button_height = 300, 50
        panel_center_x = self.control_panel.centerx
        
        # Кнопки управления
        self.back_button = Button(
            panel_center_x - button_width//2, 500, button_width, button_height,
            "BACK TO MENU", (121, 85, 72), lambda: "back"
        )
        
        self.clear_button = Button(
            panel_center_x - button_width//2, 580, button_width, button_height,
            "CLEAR HISTORY", (244, 67, 54), self.clear_history
        )
        
        self.buttons = [self.back_button, self.clear_button]
        
    def load_history(self):
        """Загружает историю попыток из файла"""
        history_file = os.path.join(self.history_dir, "history.json")
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.history_data = json.load(f)
                # Сортируем по дате (новые сверху)
                self.history_data.sort(key=lambda x: x['timestamp'], reverse=True)
                print(f"Loaded {len(self.history_data)} history entries")
            else:
                self.history_data = []
                print("No history file found")
        except Exception as e:
            print(f"Error loading history: {e}")
            self.history_data = []
            
    def save_history(self):
        """Сохраняет историю в файл"""
        history_file = os.path.join(self.history_dir, "history.json")
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history_data, f, indent=2, ensure_ascii=False)
            print("History saved successfully")
        except Exception as e:
            print(f"Error saving history: {e}")
            
    def clear_history(self):
        """Очищает историю"""
        self.history_data = []
        self.save_history()
        self.selected_attempt = None
        
        # Очищаем папку с превью
        try:
            shutil.rmtree(self.previews_dir)
            self.create_directories()
        except Exception as e:
            print(f"Error clearing previews: {e}")
            
        return "history_cleared"
        
    def get_image_hash(self, image_surface):
        """Создает простой хэш для изображения чтобы избежать дублирования"""
        # Берем небольшую выборку пикселей для хэширования
        width, height = image_surface.get_size()
        hash_pixels = []
        for x in range(0, width, width//10):
            for y in range(0, height, height//10):
                if x < width and y < height:
                    color = image_surface.get_at((x, y))
                    hash_pixels.append(sum(color[:3]))  # Сумма RGB
        
        return hash(tuple(hash_pixels))
        
    def add_attempt(self, difficulty, time_elapsed, original_image, pieces_count):
        """Добавляет новую попытку в историю"""
        try:
            # Создаем хэш изображения для уникального имени файла
            image_hash = self.get_image_hash(original_image)
            preview_filename = f"preview_{image_hash}.png"
            preview_path = os.path.join(self.previews_dir, preview_filename)
            
            # Создаем превью изображения (уменьшенная копия)
            preview_size = (100, 75)
            preview_surface = pygame.transform.scale(original_image, preview_size)
            
            # Сохраняем превью только если его еще нет
            if not os.path.exists(preview_path):
                pygame.image.save(preview_surface, preview_path)
            
            attempt = {
                'timestamp': datetime.datetime.now().isoformat(),
                'difficulty': difficulty,
                'time_elapsed': time_elapsed,
                'pieces_count': pieces_count,
                'preview_filename': preview_filename  # Сохраняем только имя файла
            }
            
            self.history_data.insert(0, attempt)  # Добавляем в начало
            if len(self.history_data) > 50:  # Ограничиваем историю 50 записями
                self.history_data = self.history_data[:50]
                
            self.save_history()
            print(f"Attempt saved to history. Image: {preview_filename}")
            
        except Exception as e:
            print(f"Error adding attempt to history: {e}")
        
    def format_timestamp(self, timestamp):
        """Форматирует timestamp в читаемый вид"""
        try:
            dt = datetime.datetime.fromisoformat(timestamp)
            return dt.strftime("%d.%m.%Y %H:%M")
        except:
            return timestamp
            
    def format_time(self, seconds):
        """Форматирует время в формат MM:SS"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
        
    def handle_event(self, event):
        # Обработка прокрутки
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset = max(0, min(self.scroll_offset - event.y * 30, self.max_scroll))
            
        # Обработка кликов по элементам истории
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.history_area.collidepoint(mouse_pos):
                # Проверяем клик по элементу истории
                rel_y = mouse_pos[1] - self.history_area.top + self.scroll_offset - 50  # Учитываем заголовок
                item_index = rel_y // 80  # Высота каждого элемента
                
                if 0 <= item_index < len(self.history_data):
                    self.selected_attempt = self.history_data[item_index]
                    print(f"Selected attempt: {self.format_timestamp(self.selected_attempt['timestamp'])}")
                    
        # Обработка кнопок
        for button in self.buttons:
            result = button.handle_event(event)
            if result:
                return result
                
        return None
        
    def update(self):
        # Обновление максимальной прокрутки
        item_height = 80
        total_height = len(self.history_data) * item_height
        self.max_scroll = max(0, total_height - self.history_area.height + 60)  # Корректировка
        
    def draw(self):
        # Очистка экрана
        self.screen.fill(self.background_color)
        
        # Заголовок
        title_shadow = self.font_large.render("GAME HISTORY", True, (20, 20, 30))
        title_text = self.font_large.render("GAME HISTORY", True, (255, 255, 255))
        self.screen.blit(title_shadow, (self.width//2 - title_text.get_width()//2 + 3, 53))
        self.screen.blit(title_text, (self.width//2 - title_text.get_width()//2, 50))
        
        # Панель управления
        self.draw_control_panel()
        
        # Область истории
        self.draw_history_area()
        
    def draw_control_panel(self):
        """Рисует левую панель управления"""
        pygame.draw.rect(self.screen, (30, 30, 40), self.control_panel, border_radius=15)
        pygame.draw.rect(self.screen, (70, 70, 90), self.control_panel, 3, border_radius=15)
        
        # Заголовок панели
        title = self.font_medium.render("History Info", True, (220, 220, 240))
        self.screen.blit(title, (self.control_panel.centerx - title.get_width()//2, 120))
        
        # Статистика
        total_attempts = len(self.history_data)
        stats_bg = pygame.Rect(self.control_panel.left + 25, 170, 300, 100)
        pygame.draw.rect(self.screen, (35, 35, 45), stats_bg, border_radius=10)
        pygame.draw.rect(self.screen, (70, 70, 90), stats_bg, 2, border_radius=10)
        
        stats_text = self.font_medium.render(f"Total: {total_attempts}", True, (255, 255, 255))
        self.screen.blit(stats_text, (self.control_panel.centerx - stats_text.get_width()//2, 190))
        
        if total_attempts > 0:
            completed_text = self.font_small.render("All attempts completed", True, (180, 180, 200))
            self.screen.blit(completed_text, (self.control_panel.centerx - completed_text.get_width()//2, 230))
        
        # Информация о выбранной попытке
        if self.selected_attempt:
            selected_bg = pygame.Rect(self.control_panel.left + 25, 290, 300, 180)
            pygame.draw.rect(self.screen, (35, 35, 45), selected_bg, border_radius=10)
            pygame.draw.rect(self.screen, (70, 70, 90), selected_bg, 2, border_radius=10)
            
            selected_title = self.font_small.render("SELECTED ATTEMPT", True, (255, 193, 7))
            self.screen.blit(selected_title, (self.control_panel.centerx - selected_title.get_width()//2, 310))
            
            # Данные выбранной попытки
            diff_text = self.font_tiny.render(f"Difficulty: {self.selected_attempt['difficulty'].upper()}", True, (255, 255, 255))
            time_text = self.font_tiny.render(f"Time: {self.format_time(self.selected_attempt['time_elapsed'])}", True, (255, 255, 255))
            pieces_text = self.font_tiny.render(f"Pieces: {self.selected_attempt['pieces_count']}", True, (255, 255, 255))
            date_text = self.font_tiny.render(f"Date: {self.format_timestamp(self.selected_attempt['timestamp'])}", True, (200, 200, 220))
            
            self.screen.blit(diff_text, (self.control_panel.centerx - diff_text.get_width()//2, 340))
            self.screen.blit(time_text, (self.control_panel.centerx - time_text.get_width()//2, 360))
            self.screen.blit(pieces_text, (self.control_panel.centerx - pieces_text.get_width()//2, 380))
            self.screen.blit(date_text, (self.control_panel.centerx - date_text.get_width()//2, 400))
            
            # Пытаемся загрузить и отобразить превью
            try:
                preview_path = os.path.join(self.previews_dir, self.selected_attempt['preview_filename'])
                if os.path.exists(preview_path):
                    preview_image = pygame.image.load(preview_path)
                    preview_rect = preview_image.get_rect()
                    preview_rect.center = (self.control_panel.centerx, 470)
                    self.screen.blit(preview_image, preview_rect)
            except Exception as e:
                print(f"Error loading preview: {e}")
        
        # Отрисовка кнопок
        for button in self.buttons:
            button.draw(self.screen)
            
    def draw_history_area(self):
        """Рисует область с историей попыток"""
        # Фон области
        pygame.draw.rect(self.screen, (25, 25, 35), self.history_area, border_radius=15)
        pygame.draw.rect(self.screen, (80, 80, 100), self.history_area, 3, border_radius=15)
        
        # Заголовок
        history_title = self.font_medium.render("Completed Puzzles", True, (200, 200, 200))
        self.screen.blit(history_title, (self.history_area.centerx - history_title.get_width()//2, 110))
        
        # Если история пуста
        if not self.history_data:
            empty_text = self.font_medium.render("No completed puzzles yet", True, (150, 150, 170))
            self.screen.blit(empty_text, (self.history_area.centerx - empty_text.get_width()//2, 
                                        self.history_area.centery))
            return
            
        # Область для прокрутки
        clip_rect = pygame.Rect(self.history_area.left + 10, self.history_area.top + 50, 
                              self.history_area.width - 20, self.history_area.height - 60)
        
        # Сохраняем текущий клип
        original_clip = self.screen.get_clip()
        self.screen.set_clip(clip_rect)
        
        # Рисуем элементы истории
        item_height = 80
        for i, attempt in enumerate(self.history_data):
            item_y = self.history_area.top + 50 + i * item_height - self.scroll_offset
            
            # Проверяем, виден ли элемент
            if item_y + item_height < clip_rect.top or item_y > clip_rect.bottom:
                continue
                
            # Фон элемента
            item_rect = pygame.Rect(self.history_area.left + 15, item_y, 
                                  self.history_area.width - 30, item_height - 5)
            
            # Подсветка выбранного элемента
            if attempt == self.selected_attempt:
                pygame.draw.rect(self.screen, (50, 50, 70), item_rect, border_radius=8)
                pygame.draw.rect(self.screen, (100, 100, 140), item_rect, 2, border_radius=8)
            else:
                pygame.draw.rect(self.screen, (35, 35, 45), item_rect, border_radius=8)
                pygame.draw.rect(self.screen, (70, 70, 90), item_rect, 1, border_radius=8)
            
            # Текст элемента
            date_text = self.font_small.render(self.format_timestamp(attempt['timestamp']), True, (255, 255, 255))
            diff_text = self.font_tiny.render(f"Difficulty: {attempt['difficulty'].upper()}", True, (200, 200, 220))
            time_text = self.font_tiny.render(f"Time: {self.format_time(attempt['time_elapsed'])}", True, (200, 200, 220))
            pieces_text = self.font_tiny.render(f"Pieces: {attempt['pieces_count']}", True, (200, 200, 220))
            
            self.screen.blit(date_text, (item_rect.left + 15, item_y + 10))
            self.screen.blit(diff_text, (item_rect.left + 15, item_y + 40))
            self.screen.blit(time_text, (item_rect.right - 150, item_y + 20))
            self.screen.blit(pieces_text, (item_rect.right - 150, item_y + 45))
        
        # Восстанавливаем клип
        self.screen.set_clip(original_clip)
        
        # Полоса прокрутки (если нужно)
        if self.max_scroll > 0:
            scroll_ratio = self.scroll_offset / self.max_scroll
            scrollbar_height = max(50, (clip_rect.height / len(self.history_data)) * clip_rect.height / item_height)
            scrollbar_y = clip_rect.top + scroll_ratio * (clip_rect.height - scrollbar_height)
            
            scrollbar_rect = pygame.Rect(clip_rect.right - 8, scrollbar_y, 6, scrollbar_height)
            pygame.draw.rect(self.screen, (100, 100, 120), scrollbar_rect, border_radius=3)