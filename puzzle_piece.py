import pygame

class PuzzlePiece:
    def __init__(self, image, start_pos, correct_pos, piece_size, movement_boundaries, puzzle_area):
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(topleft=start_pos)
        self.correct_pos = correct_pos
        self.piece_size = piece_size
        self.movement_boundaries = movement_boundaries
        self.puzzle_area = puzzle_area
        self.is_dragging = False
        self.is_correct = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.snap_threshold = 15
        self.show_hint = False
        
        # Эффекты при наведении 
        self.is_hovered = False
        self.highlight_alpha = 30  # Полупрозрачный вместо желтого
        
    def handle_event(self, event, all_pieces):
        """Обрабатывает события. Возвращает True, если событие обработано"""
        # Если кусочек уже на своем месте, не обрабатываем события
        if self.is_correct:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                # Проверяем, что этот фрагмент самый верхний среди тех, под которыми находится курсор
                top_piece = None
                for piece in reversed(all_pieces):
                    if piece.rect.collidepoint(event.pos) and not piece.is_correct:
                        top_piece = piece
                        break
                
                if top_piece == self:
                    self.is_dragging = True
                    self.drag_offset_x = event.pos[0] - self.rect.x
                    self.drag_offset_y = event.pos[1] - self.rect.y
                    return True
                    
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                self.check_snap()
                return True
                
        elif event.type == pygame.MOUSEMOTION:
            # Проверка наведения (только если не перетаскивается другой фрагмент)
            if not any(piece.is_dragging for piece in all_pieces):
                self.is_hovered = self.rect.collidepoint(event.pos) and not self.is_correct
            else:
                self.is_hovered = False
            
            if self.is_dragging:
                new_x = event.pos[0] - self.drag_offset_x
                new_y = event.pos[1] - self.drag_offset_y
                
                # Ограничиваем перемещение границами движения
                new_x = max(self.movement_boundaries.left, min(new_x, self.movement_boundaries.right - self.rect.width))
                new_y = max(self.movement_boundaries.top, min(new_y, self.movement_boundaries.bottom - self.rect.height))
                
                self.rect.topleft = (new_x, new_y)
                return True
                
        return False
        
    def check_snap(self):
        """Проверяет, находится ли фрагмент близко к правильной позиции"""
        if self.is_correct:
            return
            
        distance_x = abs(self.rect.x - self.correct_pos[0])
        distance_y = abs(self.rect.y - self.correct_pos[1])
        
        if distance_x < self.snap_threshold and distance_y < self.snap_threshold:
            self.rect.topleft = self.correct_pos
            self.is_correct = True
            # НЕ УБИРАЕМ is_hovered - кусочек остается видимым
            
    def draw(self, surface):
        # Всегда рисуем кусочек, даже если он на своем месте
        surface.blit(self.image, self.rect)
        
        if not self.is_correct:
            # Подсказка - контур правильной позиции
            if self.show_hint and not self.is_dragging:
                hint_rect = pygame.Rect(self.correct_pos[0], self.correct_pos[1], self.rect.width, self.rect.height)
                pygame.draw.rect(surface, (255, 193, 7), hint_rect, 2)
            
            # Эффект при наведении - полупрозрачный белый вместо желтого
            if self.is_hovered or self.is_dragging:
                highlight = pygame.Surface(self.piece_size, pygame.SRCALPHA)
                alpha = 80 if self.is_dragging else self.highlight_alpha
                highlight.fill((255, 255, 255, alpha))
                surface.blit(highlight, self.rect)
                
            # Рамка вокруг фрагмента
            border_color = (200, 200, 200) if not self.is_dragging else (255, 255, 0)
            pygame.draw.rect(surface, border_color, self.rect, 1)