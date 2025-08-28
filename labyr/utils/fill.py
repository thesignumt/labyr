from collections import deque
from typing import TypeAlias


def fill_rect(matrix, coord1, coord2, char):
    rows, cols = len(matrix), len(matrix[0])

    def norm(idx, size):
        return idx if idx >= 0 else size + idx

    x1, y1 = norm(coord1[0], rows), norm(coord1[1], cols)
    x2, y2 = norm(coord2[0], rows), norm(coord2[1], cols)
    row_start, row_end = sorted([x1, x2])
    col_start, col_end = sorted([y1, y2])
    for i in range(row_start, row_end + 1):
        for j in range(col_start, col_end + 1):
            matrix[i][j] = char


Matrix: TypeAlias = list[list[str]]


def fill_unbound(map: Matrix, target_char: str, fill_char: str) -> Matrix:
    rows, cols = len(map), len(map[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = deque()

    # Add border cells with target_char to queue
    for r in range(rows):
        for c in range(cols):
            if (r in {0, rows - 1} or c in {0, cols - 1}) and map[r][c] == target_char:
                queue.append((r, c))
                visited[r][c] = True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c = queue.popleft()
        map[r][c] = fill_char
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and not visited[nr][nc]
                and map[nr][nc] == target_char
            ):
                queue.append((nr, nc))
                visited[nr][nc] = True

    return map
