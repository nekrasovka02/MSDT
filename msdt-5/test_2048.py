import sys
from unittest.mock import MagicMock

# Подмена pygame, чтобы избежать ошибки импорта в среде без графики
sys.modules['pygame'] = MagicMock()
sys.modules['pygame.locals'] = MagicMock()
sys.modules['pygame.sprite'] = MagicMock()
sys.modules['pygame.time'] = MagicMock()
sys.modules['pygame.display'] = MagicMock()
sys.modules['pygame.image'] = MagicMock()
sys.modules['pygame.event'] = MagicMock()
sys.modules['pygame.key'] = MagicMock()
sys.modules['pygame.font'] = MagicMock()
sys.modules['pygame.mixer'] = MagicMock()
sys.modules['pygame.Rect'] = MagicMock()
sys.modules['pygame.Surface'] = MagicMock()

import pytest
from unittest.mock import patch
from copy import deepcopy
from game_2048 import slide_row_left, move_left, move_right, move_up, move_down, add_new_tile, check_win, check_moves_available

# Параметризованный тест для slide_row_left
@pytest.mark.parametrize("input_row, expected", [
    ([2, 0, 2, 0],       [4, 0, 0, 0]),      
    ([2, 2, 0, 0],       [4, 0, 0, 0]),
    ([2, 2, 4, 0],       [4, 4, 0, 0]),
    ([2, 2, 2, 2],       [4, 4, 0, 0]),
    ([0, 0, 0, 0],       [0, 0, 0, 0]),
    ([2, 4, 2, 4],       [2, 4, 2, 4]),      
])
def test_slide_row_left(input_row, expected):
    assert slide_row_left(input_row) == expected

# Параметризованный тест для move_left на целом поле 
@pytest.mark.parametrize("input_board, expected", [
    ([[2,2,0,0], [0,2,2,0], [0,0,0,0], [2,0,0,2]],
     [[4,0,0,0], [4,0,0,0], [0,0,0,0], [4,0,0,0]]),
    ([[4,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]],
     [[4,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]),
])
def test_move_left(input_board, expected):
    assert move_left(input_board) == expected

# Тест move_right (используем инверсию)
def test_move_right():
    board = [[2,2,0,0], [0,2,2,0], [0,0,0,0], [2,0,0,2], [4,0,2,0]]
    expected = [[0,0,0,4], [0,0,0,4], [0,0,0,0], [0,0,0,4], [0,0,4,2]]
    assert move_right(board) == expected

# Тест move_up
def test_move_up():
    board = [[2,0,0,0], [2,0,0,0], [0,0,0,0], [0,0,0,0]]
    expected = [[4,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    assert move_up(board) == expected

# Тест move_down 
def test_move_down():
    board = [[2,0,0,0], [2,0,0,0], [0,0,0,0], [0,0,0,0]]
    expected = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [4,0,0,0]]
    assert move_down(board) == expected

# Тест check_win 
def test_check_win():
    board_win = [[2048,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    board_lose = [[2,4,2,4], [4,2,4,2], [2,4,2,4], [4,2,4,2]]
    assert check_win(board_win) is True
    assert check_win(board_lose) is False

# Тест check_moves_available
def test_check_moves_available():
    # есть пустая клетка
    board_with_empty = [[2,4,8,16], [32,64,128,256], [512,1024,0,0], [2,4,8,16]]
    assert check_moves_available(board_with_empty) is True
    # нет пустых, но есть соседние одинаковые
    board_no_empty_but_merge = [[2,2,4,8], [16,32,64,128], [256,512,1024,2048], [2,4,8,16]]
    assert check_moves_available(board_no_empty_but_merge) is True
    # полное поле без соседних одинаковых -> нет ходов
    board_full_stuck = [[2,4,2,4], [4,2,4,2], [2,4,2,4], [4,2,4,2]]
    assert check_moves_available(board_full_stuck) is False

# Тест add_new_tile с моком random
def test_add_new_tile():
    board = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    # Мокаем random.choice, чтобы всегда выбирать (0,0) и random.random -> 0.95 (чтобы вставилась 4)
    with patch('game_2048.random.choice', return_value=(0,0)), \
         patch('game_2048.random.random', return_value=0.95):
        add_new_tile(board)
        assert board[0][0] == 4
    # Проверим, что при random.random < 0.9 вставляется 2, иначе 4
    board = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    with patch('game_2048.random.choice', return_value=(0,0)), \
         patch('game_2048.random.random', return_value=0.85):
        add_new_tile(board)
        assert board[0][0] == 2
    board = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    with patch('game_2048.random.choice', return_value=(0,0)), \
         patch('game_2048.random.random', return_value=0.9):
        add_new_tile(board)
        assert board[0][0] == 4   # так как 0.95 > 0.9 -> 2

# Тест add_new_tile с monkeypatch
def test_add_new_tile_monkeypatch(monkeypatch):
    board = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    monkeypatch.setattr('game_2048.random.choice', lambda lst: (0,0))
    monkeypatch.setattr('game_2048.random.random', lambda: 0.95)
    add_new_tile(board)
    assert board[0][0] == 4
    