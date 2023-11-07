def bfs(self, start, target):
    visited = set()
    queue = [(start, [])]

    while queue:
        current, path = queue.pop(0)

        if current == target:
            return path

        for neighbor in self.get_valid_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None