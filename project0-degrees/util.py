class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self, frontier=None):
        self.frontier = frontier if frontier is not None else []

    def add(self, node):
        return StackFrontier(self.frontier + [node])

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            return node, StackFrontier(self.frontier[:-1])


class QueueFrontier():
    def __init__(self, frontier=None):
        self.frontier = frontier if frontier is not None else []

    def add(self, node):
        return QueueFrontier(self.frontier + [node])

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            return node, QueueFrontier(self.frontier[1:])
