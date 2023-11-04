from collections import deque

def bfs(snake, width, height, target):
    visited = set()
    queue = deque()
    queue.append((snake.body[-1], []))

    while queue:
        current, path = queue.popleft()
        visited.add(current)

        if current == target:
            return path

        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_position = (current[0] + direction[0], current[1] + direction[1])
            if (
                0 <= new_position[0] < width
                and 0 <= new_position[1] < height
                and new_position not in visited
                and new_position not in snake.body
            ):
                new_path = path + [direction]
                queue.append((new_position, new_path))

    return None
