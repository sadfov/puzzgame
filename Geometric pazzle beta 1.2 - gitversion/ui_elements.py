import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action
        self.is_hovered = False
        self.font = pygame.font.SysFont('Arial', 20)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                result = self.action()
                return result
        return None
        
    def draw(self, surface):
        # Цвет кнопки с эффектом наведения
        color = self.color
        if self.is_hovered:
            color = tuple(min(c + 30, 255) for c in self.color)
            
        # Рисуем кнопку с закругленными углами
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=10)
        
        # Текст кнопки
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class InfoButton:
    def __init__(self, x, y, width, height, text, color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action
        self.is_hovered = False
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                result = self.action()
                return result
        return None
        
    def draw(self, surface):
        # Круглая кнопка с эффектом наведения
        color = self.color
        if self.is_hovered:
            color = tuple(min(c + 40, 255) for c in self.color)
            
        # Рисуем круглую кнопку
        pygame.draw.circle(surface, color, self.rect.center, self.rect.width//2)
        pygame.draw.circle(surface, (255, 255, 255), self.rect.center, self.rect.width//2, 2)
        
        # Текст кнопки (знак вопроса)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)