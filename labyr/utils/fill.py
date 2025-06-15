def fill_rect(
    matrix: list[list[str]], coord1: tuple[int, int], coord2: tuple[int, int], char: str
):
    x1, y1 = coord1
    x2, y2 = coord2
    row_start, row_end = sorted([x1, x2])
    col_start, col_end = sorted([y1, y2])
    for i in range(row_start, row_end + 1):
        for j in range(col_start, col_end + 1):
            matrix[i][j] = char
