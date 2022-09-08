import numpy as np
import pygame
from visualize import GUI

class Node:
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent

        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return self.position == other.position


class Astar:
    def __init__(self, start, end):
        # Set search area
        # Can use four direction search or eight direction search

        # self.search_area = [[1, 0], [0, 1], [-1, 0], [0, -1], [-1, 1], [1, 1], [1, -1], [-1, -1]]
        self.search_area = [[1, 0], [0, 1], [-1, 0], [0, -1]]

        # visualize
        self.gui = GUI()

        # map size is 25 x 25
        self.start = start
        self.end = end

        # Random factor control the number of obstacles
        self.map = self.gui.create_map(self.start, self.end, random_factor=0.1)

        # set fps
        self.FPS = 40
        self.clock = pygame.time.Clock()

        # start
        path = self.search_path(self.map, self.start, self.end)

        # draw path
        self.draw_path(path)

    # Use for checkout neighbor node not both in visited list and unvisited list
    def _checkout_node(self, neighbor, node_list):
        for node in node_list:
            if neighbor == node:
                return True

    def search_path(self, map, start, end):
        # Setup initial node
        start_node = Node(start, None)
        end_node = Node(end, None)

        # As storage unvisited node
        unvisited_list = []

        # As storage visited node
        visited_list = []

        # Append start node into the unvisited node
        unvisited_list.append(start_node)

        # Start search
        while len(unvisited_list) != 0:
            # Found current node
            current_node = unvisited_list[0]
            current_idx = 0
            for idx, node in enumerate(unvisited_list):
                if node.f < current_node.f:
                    current_node = node
                    current_idx = idx

            # Found the goal
            if current_node == end_node:
                path = []

                while current_node is not None:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]

            # Pop current node from unvisited list, append to the visited list
            self.draw(current_node)
            unvisited_list.pop(current_idx)
            visited_list.append(current_node)

            # Search for neighbors of the current node
            for area in self.search_area:
                neighbor = [current_node.position[0] + area[0], current_node.position[1] + area[1]]  # row, col
                neighbor_node = Node(neighbor, current_node)

                # Make sure not out of map range
                if neighbor[0] < 0 or neighbor[0] >= map.shape[0] or neighbor[1] < 0 or neighbor[1] >= map.shape[1]:
                    continue

                # Make sure the node walkable
                if map[neighbor[0], neighbor[1]] != 0:
                    continue

                # Make sure the node not both in unvisited list and visited node
                if self._checkout_node(neighbor_node, visited_list):
                    continue
                if self._checkout_node(neighbor_node, unvisited_list):
                    continue

                # Otherwise add to unvisited list.
                # Here have three methods can use.
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = ((neighbor_node.position[0] - end_node.position[0]) ** 2 + (
                            neighbor_node.position[1] - end_node.position[1]) ** 2)

                # neighbor_node.h = np.sqrt((neighbor_node.position[0] - end_node.position[0]) ** 2 + (
                #             neighbor_node.position[1] - end_node.position[1]) ** 2)

                # neighbor_node.h = abs(neighbor_node.position[0] - end_node.position[0]) + abs(neighbor_node.position[1] - end_node.position[1])
                neighbor_node.f = neighbor_node.g + neighbor_node.h

                unvisited_list.append(neighbor_node)

        return None

    def draw(self, current_node):
        self.gui.set_map(self.start[0], self.start[1], (255, 0, 0))  # show start node
        self.gui.set_map(self.end[0], self.end[1], (0, 255, 0))  # finish start node
        self.gui.set_map(current_node.position[0], current_node.position[1], color=(128, 128, 128))
        self.gui.show_map(self.map)
        pygame.display.update()
        self.clock.tick(self.FPS)

    def draw_path(self, path):
        for p in path[1:-1]:
            self.gui.set_map(p[0], p[1], color=(0, 0, 255))
        self.gui.set_map(self.start[0], self.start[1], (255, 0, 0))  # show start node
        self.gui.set_map(self.end[0], self.end[1], (0, 255, 0))  # finish start node
        self.gui.show_map(self.map)
        pygame.display.update()
        input()


if __name__ == '__main__':
    astar = Astar(start=[0, 0], end=[20, 23])
