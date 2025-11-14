import pygame
import random
from puzzle_piece import PuzzlePiece

def generate_puzzle_pieces(image, difficulty, movement_boundaries, puzzle_area):
    pieces = []
    
    # Определяем размер сетки в зависимости от сложности
    if difficulty == "easy":
        rows, cols = 3, 3
    elif difficulty == "medium":
        rows, cols = 4, 4
    elif difficulty == "hard":
        rows, cols = 5, 5
    else:  # ultra
        rows, cols = 10, 10
        
    # Размеры исходного изображения
    img_width, img_height = image.get_size()
    
    # Размеры одного фрагмента
    piece_width = img_width // cols
    piece_height = img_height // rows
    
    # Создаем фрагменты
    for row in range(rows):
        for col in range(cols):
            # Создаем поверхность для фрагмента
            piece_surface = pygame.Surface((piece_width, piece_height), pygame.SRCALPHA)
            
            # Вычисляем область для вырезания из исходного изображения
            source_rect = pygame.Rect(
                col * piece_width,
                row * piece_height,
                piece_width,
                piece_height
            )
            
            # Копируем часть изображения на поверхность фрагмента
            piece_surface.blit(image, (0, 0), source_rect)
            
            # Правильная позиция фрагмента в области сборки
            original_x = puzzle_area.left + col * piece_width
            original_y = puzzle_area.top + row * piece_height
            
            # Случайная начальная позиция ВНУТРИ области сборки пазла
            max_x = puzzle_area.width - piece_width
            max_y = puzzle_area.height - piece_height
            
            start_x = random.randint(puzzle_area.left, puzzle_area.left + max_x)
            start_y = random.randint(puzzle_area.top, puzzle_area.top + max_y)
            
            # Создаем объект фрагмента
            piece = PuzzlePiece(
                image=piece_surface,
                start_pos=(start_x, start_y),
                correct_pos=(original_x, original_y),
                piece_size=(piece_width, piece_height),
                movement_boundaries=movement_boundaries,
                puzzle_area=puzzle_area
            )
            
            pieces.append(piece)
    
    return pieces