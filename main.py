import time
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
# this is in python 3.4. For python 2.x import Tkinter
from queue import PriorityQueue
from collections import defaultdict
draw_nodes = True
draw_nodes_flag = True

# Constants
HEIGHT = 800
WIDTH = 800
NODE_SPACE_ALLOWANCE = 20
EDGE_COLOR = "Yellow"
EDGE_SIZE = 2
NODE_LABEL_COLOR = "White"
NODE_COLOR = "Red"
NODE_MARK_COLOR = "Green"
ANIMATION_DELAY = 0.2

# Global variables
i = 0
result = []
calling_counter = 0
start = 0
goal = 0
placeNodes = True
setNodesRelation = False

setGoal = False
setStart = False
displayResult = False
nodes = []
pos1 = [0, 0]
pos2 = [0, 0]
click = 0

index1 = 0
index2 = 0

matrix = []
temp_matrix = []

nodes_no = 0
visited = []

dfs_counter = 0
visited_nodes = []
Iterations_vertices = []
graph_type = ''
iteration_counter = 0
returnV = True
selected_search_algorithm = ''
search_algorithms = ('BFS', 'DFS', 'Iterative Deepening', 'Uniform Cost', 'Greedy', 'A*')
flag_continue_dfs = True
temp_expanded = []
temp_visited_nodes_indices = []
goal_nodes_list = []


class Point:
    def __init__(self, pos, label):
        self.pos = pos
        self.index = 0
        self.label = label
        self.heuristic_weight = -1


def increase_animation():
    global ANIMATION_DELAY
    if ANIMATION_DELAY <= 3:
        ANIMATION_DELAY = ANIMATION_DELAY + 0.2
    print(ANIMATION_DELAY)


def decrease_animation():
    global ANIMATION_DELAY
    print(ANIMATION_DELAY)

    if ANIMATION_DELAY >= 0.3:
        ANIMATION_DELAY = ANIMATION_DELAY - 0.2


def stop_nodes():
    global draw_nodes, matrix, nodes_no, visited, temp_matrix, draw_nodes_flag, dfs_counter
    draw_nodes = False
    if draw_nodes_flag:
        matrix = [[0 for i in range(nodes_no)]
                  for j in range(nodes_no)]
        temp_matrix = [[0 for i in range(nodes_no)]
                  for j in range(nodes_no)]
        visited = [False] * nodes_no
        draw_nodes_flag = False


def is_connected():
    flag_all = 1
    for i in range(len(matrix)):
        flag_row = 0
        for j in range(len(matrix)):
            flag_row = flag_row or matrix[i][j]
        flag_all = flag_all and flag_row
    if flag_all >= 1:
        return False

    else:
        messagebox.showwarning("Error", "Please draw a connected graph!!!")
        return True


def convert(matrix_1):
    adjList = defaultdict(list)
    for i in range(len(matrix_1)):
        for j in range(len(matrix_1[i])):
            if matrix_1[i][j] > 0:
                tuple_1 = (chr(ord('A') + j), matrix[i][j])
                adjList[chr(ord('A') + i)].append(tuple_1)
    return adjList


class ExampleApp(tk.Tk):

    def __init__(self):

        global graph_type, selected_search_algorithm

        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.title("AI search algorithms")

        main_frame = Frame(self)

        frame_2 = Frame(main_frame)
        frame_2.grid(row=0, column=1)

        self.canvas = tk.Canvas(main_frame, width=800, height=600, cursor="cross", relief="groove", borderwidth=5)
        # self.canvas.pack(side="top", fill="both", expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.grid(row=0, column=0)

        ttk.Button(frame_2, text="Lock nodes", command=stop_nodes).grid(row=0, column=0)

        Label(frame_2, text=' ').grid(row=1, column=0)  # spacer_1

        Label(frame_2, text='Enter the start node').grid(row=2, column=0)

        self.start_node = Entry(frame_2, width=12)
        self.start_node.focus_set()
        self.start_node.grid(row=2, column=1)

        Label(frame_2, text='Enter the goal node').grid(row=3, column=0)

        self.goal_node = Entry(frame_2, width=12)
        self.goal_node.focus_set()
        self.goal_node.grid(row=3, column=1)

        Label(frame_2, text='Example for multiple goals: A-B-C').grid(row=4, column=0)

        Label(frame_2, text=' ').grid(row=5, column=0)  # spacer_2

        self.goal_node_index = []

        self.goal_coords = [0, 0]

        ttk.Button(frame_2, text="Set Edge Weights", command=lambda: self.edge_weights_canvas()).grid(row=6, column=0)
        ttk.Button(frame_2, text="Set Node Heuristic", command=lambda: self.node_heuristic_canvas()).grid(row=7, column=0)


        Label(frame_2, text='Select the desired graph type').grid(row=8, column=0)

        graph_type = StringVar()
        graph_type.set("Undirected")

        tk.Radiobutton(frame_2, text="Undirected", variable=graph_type, value="Undirected").grid(row=9, column=0)
        tk.Radiobutton(frame_2, text="Directed", variable=graph_type, value="Directed").grid(row=10, column=0)

        Label(frame_2, text='Select the desired search algorithm').grid(row=11, column=0)

        selected_search_algorithm = StringVar()
        selected_search_algorithm.set('BFS')

        OptionMenu(frame_2, selected_search_algorithm, *search_algorithms).grid(row=12, column=0)

        Label(frame_2, text=' ').grid(row=13, column=0)  # spacer_3

        tk.Button(frame_2, text="Traverse graph", command=self.traverse_graph).grid(row=14, column=0)

        Label(frame_2, text=' ').grid(row=15, column=0)  # spacer_4

        tk.Button(frame_2, text="Reset graph", command=self.reset_graph).grid(row=16, column=0)

        Label(frame_2, text='  ').grid(row=17, column=0)
        Label(frame_2, text='Animation delay').grid(row=18, column=0)
        ttk.Button(frame_2, text="+", command=lambda: increase_animation()).grid(row=19, column=0)
        ttk.Button(frame_2, text="-", command=lambda: decrease_animation()).grid(row=20, column=0)

        self.rect = None
        self.center = [0, 0]

        main_frame.pack()

    def on_button_press(self, event):
        global draw_nodes, i, nodes, pos1, pos2, click, index1, index2, nodes_no, matrix
        # save mouse drag start position
        self.center[0] = event.x
        self.center[1] = event.y
        oval_lower = [self.center[0] + 15, self.center[1] + 15]

        if draw_nodes:
            node_flag = True
            for j in range(len(nodes)):
                if ((event.x >= nodes[j].pos[0]) and (event.y >= nodes[j].pos[1])) and ((event.x <= nodes[j].pos[0]+15) and (event.y <= nodes[j].pos[1]+15)):
                    node_flag = False
                    break

            if node_flag:
                self.rect = self.canvas.create_oval(self.center[0], self.center[1], oval_lower[0],
                                                    oval_lower[1], fill="Black")
                self.rect = self.canvas.create_text(self.center[0], self.center[1] - 10, text=chr(ord("A") + i),
                                                    fill="Blue", font='Helvetica 25')

                nodes.append(Point([event.x, event.y], chr(ord("A") + i)))
                i = i + 1
                nodes_no += 1

        else:

            for i in range(len(nodes)):
                if ((event.x >= nodes[i].pos[0]) and (event.y >= nodes[i].pos[1])) and ((event.x <= nodes[i].pos[0]+15) and (event.y <= nodes[i].pos[1]+15)):
                    if click == 0:
                        pos1 = [(nodes[i].pos[0]+nodes[i].pos[0]+15)/2, (nodes[i].pos[1]+nodes[i].pos[1]+15)/2]
                        click = 1
                        index1 = i
                        break

                    if click == 1:
                        temp_position=[(nodes[i].pos[0] + nodes[i].pos[0] + 15) / 2,
                                    (nodes[i].pos[1] + nodes[i].pos[1] + 15) / 2]
                        if pos1 != temp_position:

                            pos2 = [(nodes[i].pos[0] + nodes[i].pos[0] + 15) / 2,
                                    (nodes[i].pos[1] + nodes[i].pos[1] + 15) / 2]
                            click = 2
                            index2 = i
                            break

            if click == 2:
                if graph_type.get() == "Undirected":
                    self.canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], fill="black", width=2)
                    click = 0
                    matrix[index1][index2] = 1
                    matrix[index2][index1] = 1
                else:
                    self.canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], fill="black", width=2, arrow=tk.LAST, arrowshape=(15, 15, 10))
                    click = 0
                    matrix[index1][index2] = 1
                    # matrix[index2][index1] = 1

    def reset_graph(self):
        global draw_nodes, nodes, visited_nodes, nodes_no, i, index1, index2, draw_nodes_flag, dfs_counter, matrix, visited_nodes, temp_matrix, visited, flag_continue_dfs, Iterations_vertices, iteration_counter, temp_expanded, temp_visited_nodes_indices

        self.canvas.delete('all')

        draw_nodes = draw_nodes_flag = True
        nodes_no = i = index1 = index2 = 0
        nodes.clear()
        visited_nodes.clear()
        dfs_counter = 0
        matrix = [[0 for i in range(nodes_no)]
                  for j in range(nodes_no)]
        temp_matrix = [[0 for i in range(nodes_no)]
                       for j in range(nodes_no)]
        visited = [False] * nodes_no
        flag_continue_dfs = True
        Iterations_vertices.clear()
        iteration_counter = 0
        temp_expanded.clear()
        temp_visited_nodes_indices.clear()

    def apply_another_algorithm(self):

        global visited_nodes, dfs_counter, temp_matrix, visited, flag_continue_dfs, iteration_counter
        print(visited_nodes)

        for i in range(len(visited_nodes)):
            point = visited_nodes[i]
            self.rect = self.canvas.create_oval(point[0], point[1], point[0] + 15, point[1] + 15, fill="Black")
            self.canvas.update_idletasks()
        time.sleep(1)

        visited_nodes.clear()
        dfs_counter = 0
        temp_matrix = [[0 for i in range(nodes_no)]
                       for j in range(nodes_no)]
        visited = [False] * nodes_no
        flag_continue_dfs = True
        Iterations_vertices.clear()
        iteration_counter = 0
        temp_expanded.clear()
        temp_visited_nodes_indices.clear()

    def bfs_matrix(self):
        global visited_nodes, goal_nodes_list
        visited = set()
        expanded = []
        queue = [self.start_node.get()]

        while queue:
            path = queue.pop(0)
            current = path[-1]

            temp_row = ord(current) - ord('@') - 1

            if current not in expanded:
                expanded.append(path[-1])
                visited_nodes.append(nodes[temp_row].pos)

            if current not in visited:
                visited.add(current)

            if current in goal_nodes_list:
                print('path: ', path, 'expanded: ', expanded)
                return path, expanded

            length = len(matrix[temp_row])
            for neighbor in range(length):
                if neighbor not in visited and matrix[temp_row][neighbor] > 0:
                    j = chr(neighbor + ord('A'))
                    if j not in visited:
                        appends = path + j[0]
                        queue.append(appends)

    def dfs_matrix(self, start, goal, path, expanded=[]):
        global nodes_no, visited, dfs_counter, matrix, visited_nodes, nodes

        if dfs_counter == 0:
            dfs_counter = 1
            visited_nodes.append(nodes[start].pos)

        if start not in path:
            path = path + [start]

        if start not in expanded:
            expanded.append(start)
            visited_nodes.append(nodes[start].pos)

        if start in goal:
            temp_string = str('')
            for x in path:
                temp_string = temp_string + chr(ord('A') + x)
            return temp_string, [chr(ord('A') + x) for x in expanded]

        for neighbor in range(len(matrix[start])):
            if neighbor not in expanded and matrix[start][neighbor] > 0:
                output = self.dfs_matrix(neighbor, goal, path, expanded)
                if output is not None:
                    return output

    def Iterative_deepening_preparation(self, start):

        global nodes_no, visited, dfs_counter, matrix, visited_nodes, nodes, iteration_counter, temp_matrix, returnV, Iterations_vertices

        if iteration_counter == 0:
            for i in range(nodes_no):
                for j in range(nodes_no):
                    temp_matrix[i][j] = 0

        if iteration_counter == 0:
            Iterations_vertices.append(start)

        if iteration_counter != 0:

            if iteration_counter == 1:
                for i in range(nodes_no):
                    temp_matrix[start][i] = matrix[start][i]
                    if temp_matrix[start][i] > 0:
                        Iterations_vertices.append(i)

            else:
                for i in range(len(Iterations_vertices)):
                    for j in range(nodes_no):
                        temp_matrix[Iterations_vertices[i]][j] = matrix[Iterations_vertices[i]][j]
                        if temp_matrix[Iterations_vertices[i]][j] > 0:
                            Iterations_vertices.append(j)

        iteration_counter += 1

    def Iterative_DFS(self, start, goal):
        global nodes_no, visited, dfs_counter, temp_matrix, visited_nodes, nodes, returnV, flag_continue_dfs, temp_visited_nodes_indices

        if dfs_counter == 0:
            visited_nodes.append(nodes[start].pos)
            temp_visited_nodes_indices.append(start)

            dfs_counter = 1

        visited[start] = True
        if start in goal:
            flag_continue_dfs = False
            return

        for i in range(nodes_no):
            if temp_matrix[start][i] > 0 and (visited[i] is False):
                visited_nodes.append(nodes[i].pos)
                temp_visited_nodes_indices.append(i)
                self.Iterative_DFS(i, goal=self.goal_node_index)

        return True

    def perform_steps(self):
        global returnV, visited, dfs_counter, flag_continue_dfs, start, temp_expanded, temp_visited_nodes_indices
        self.Iterative_deepening_preparation(start=start)
        self.Iterative_DFS(start, goal=self.goal_node_index)
        print (temp_visited_nodes_indices)
        for i in range(len(visited_nodes)):
            point = visited_nodes[i]

            if point in self.goal_coords:
                time.sleep(ANIMATION_DELAY)
                self.rect = self.canvas.create_oval(point[0], point[1], point[0] + 15, point[1] + 15, fill="Green")
                # returnV = False
                return

            # point1 = [ (point[0] + (point[0]+15))/2, (point[1] + (point[1]+15))/2]
            self.rect = self.canvas.create_oval(point[0], point[1], point[0] + 15, point[1] + 15, fill="Red")
            time.sleep(ANIMATION_DELAY)
            self.canvas.update_idletasks()

        time.sleep(ANIMATION_DELAY)

        for i in range(len(visited_nodes)):
            point = visited_nodes[i]
            self.rect = self.canvas.create_oval(point[0], point[1], point[0] + 15, point[1] + 15, fill="Black")

        for i in range(nodes_no):
            visited[i] = False
        visited_nodes.clear()
        dfs_counter = 0
        if flag_continue_dfs:
            self.perform_steps()

    def uniform_cost(self):
        global visited_nodes, goal_nodes_list

        visited = set()
        expanded = []
        queue = PriorityQueue()
        queue.put((0, self.start_node.get()))

        while queue:
            cost, solution_path = queue.get()
            current = solution_path[-1]
            temp_row = ord(current) - ord('@') - 1
            if current not in visited:
                visited.add(current)
                expanded.append(current)
                visited_nodes.append(nodes[temp_row].pos)

                if current in goal_nodes_list:
                    return solution_path, expanded

            length = len(matrix[temp_row])

            for neighbor in range(length):
                if matrix[temp_row][neighbor] > 0:
                    j = chr(neighbor + ord('A'))
                    if j not in visited:
                        total_cost = cost + matrix[temp_row][neighbor]
                        queue.put((total_cost, solution_path + j))

    def greedy(self):
        global visited_nodes, nodes, goal_nodes_list

        visited = set()
        expanded = []
        queue = PriorityQueue()
        queue.put((0, self.start_node.get()))

        while queue:
            cost, solution_path = queue.get()
            current = solution_path[-1]
            temp_row = ord(current) - ord('@') - 1
            if current not in visited:
                visited.add(current)
                expanded.append(current)
                visited_nodes.append(nodes[temp_row].pos)

                if current in goal_nodes_list:
                    return solution_path, expanded

                length = len(matrix[temp_row])

                for neighbor in range(length):
                    if neighbor not in visited and matrix[temp_row][neighbor] > 0:  # TODO review not in visited condition
                        j = chr(neighbor + ord('A'))
                        print(j in visited)
                        temp_list = [x.heuristic_weight for x in nodes if x.label == j]
                        print('temp_list: ', temp_list)
                        print('expected:', temp_list[0], 'actual: ', nodes[neighbor].heuristic_weight)
                        total_cost = nodes[neighbor].heuristic_weight
                        queue.put((total_cost, solution_path + j))

    def astar(self, graph, start, goal):
        global nodes, visited_nodes

        visited = []
        path = []
        prev = {}
        queue = PriorityQueue()
        queue.put((0, start, None))

        while queue:
            cost, node, prev_n = queue.get()
            if node not in visited:
                visited.append(node)
                visited_nodes.append(nodes[ord(node) - ord('@') - 1].pos)
                prev[node] = prev_n

                if node in goal:
                    while prev[node] is not None:
                        path += [node]
                        node = prev[node]
                    path += [start]
                    temp_path_String=str('')
                    for i in path[::-1]:
                        temp_path_String= temp_path_String+ i

                    return temp_path_String, visited
                for i, c in graph[node]:
                    if i not in visited:
                        total_cost = cost + c
                        h1 = nodes[ord(i) - ord('@') - 1].heuristic_weight
                        total = total_cost + h1 - nodes[ord(node) - ord('@') - 1].heuristic_weight
                        queue.put((total, i, node))

    def check_heuristic_weight(self):
        global nodes
        for j in nodes:
            if j.heuristic_weight < 0:
                messagebox.showwarning("Error", "Some Nodes have a wrong heuristic value")
                return False
        return True

    def traverse_graph(self):

        global visited_nodes, selected_search_algorithm, start, returnV, temp_visited_nodes_indices, matrix, goal_nodes_list

        solution_path = None
        expanded = None

        if graph_type == 'Undirected':
            returnV = is_connected()
            if returnV:
                return

        if len(self.start_node.get()) == 0 or len(self.goal_node.get()) == 0:
            messagebox.showwarning("Error", "Please make sure that you entered the start and the goal nodes!!!")
            return

        goal_nodes_list = self.goal_node.get().split('-')

        if len(self.start_node.get()) != 0:
            start = ord(self.start_node.get()) - ord('@') - 1
            flag1 = flag2 = True

            for i in range(len(nodes)):
                if self.start_node.get() == nodes[i].label:
                    flag1 = False
                    break

            for j in range(len(goal_nodes_list)):
                flag2 = True
                for k in range(len(nodes)):
                    if goal_nodes_list[j] == nodes[k].label:
                        flag2 = False
                        break

            print(flag1, flag2)
            if flag1 or flag2:
                messagebox.showwarning("Error", "Please make sure that your start and goal nodes are correct!!!")
                return

            self.goal_node_index = [ord(x) - ord('@') - 1 for x in goal_nodes_list]

            self.goal_coords = [nodes[x].pos for x in self.goal_node_index]

        if selected_search_algorithm.get() == 'DFS':
            self.apply_another_algorithm()
            # self.dfs(start=start)
            solution_path, expanded = self.dfs_matrix(start=start, goal=self.goal_node_index, path=[], expanded=[])

        elif selected_search_algorithm.get() == 'BFS':
            self.apply_another_algorithm()
            solution_path, expanded = self.bfs_matrix()
        elif selected_search_algorithm.get() == 'Iterative Deepening':
            self.apply_another_algorithm()
            # if (returnV):
            self.perform_steps()
            solution_path, expanded = self.dfs_matrix(start=start, goal=self.goal_node_index, path=[], expanded=[])
            expanded.clear()
            for i in range(len(temp_visited_nodes_indices)):
                if temp_visited_nodes_indices[i] in self.goal_node_index:
                    expanded.append(chr(ord('A')+temp_visited_nodes_indices[i]))
                    break
                else:
                    expanded.append(chr(ord('A') + temp_visited_nodes_indices[i]))

        elif selected_search_algorithm.get() == 'Uniform Cost':
            self.apply_another_algorithm()
            solution_path, expanded = self.uniform_cost()
        elif selected_search_algorithm.get() == 'Greedy':
            if not self.check_heuristic_weight():
                return
            self.apply_another_algorithm()
            solution_path, expanded = self.greedy()
        elif selected_search_algorithm.get() == 'A*':
            if not self.check_heuristic_weight():
                return
            self.apply_another_algorithm()
            AdjList = convert(matrix)
            solution_path, expanded = self.astar(graph=AdjList, start=self.start_node.get(), goal=goal_nodes_list)

        for i in range(len(visited_nodes)):
            point = visited_nodes[i]

            if point in self.goal_coords:
                time.sleep(ANIMATION_DELAY)
                self.rect = self.canvas.create_oval(point[0], point[1], point[0] + 15, point[1] + 15, fill="Green")
                returnV = False

                temp = str('')

                for j in range(len(expanded)):
                    if j == len(expanded) - 1:
                        temp = temp + expanded[j]
                        break
                    temp = temp + expanded[j] + ' -> '

                temp_2 = 'Solution Path: ' + solution_path + '\n\n' + 'Visited Nodes: ' + temp
                messagebox.showinfo("Solution Path & Visited Nodes", temp_2)
                return

            self.rect = self.canvas.create_oval(point[0], point[1], point[0] + 15, point[1] + 15, fill="Red")
            time.sleep(ANIMATION_DELAY)
            self.canvas.update_idletasks()

    def edge_weights_canvas(self):

        offset = 0
        edges = []

        if graph_type.get() == "Undirected":
            for (row, matrix2) in enumerate(matrix):
                for column in range(offset, len(matrix2)):
                    if matrix2[column]:
                        start = chr(row + ord('A'))
                        end = chr(column + ord('A'))
                        edges.append(start + '-' + end)
                offset += 1
        else:
            for (row, matrix2) in enumerate(matrix):
                for (column, value) in enumerate(matrix2):
                    if value:
                        start = chr(row + ord('A'))
                        end = chr(column + ord('A'))
                        edges.append(start + '-' + end)

        if not edges:
            messagebox.showwarning("Error", "Create some edges first")
            return

        window = tk.Toplevel()
        frame = Frame(window)

        edge = StringVar()
        edge.set(edges[0])

        OptionMenu(frame, edge, *edges).grid(row=0, column=0)

        Label(frame, text='').grid(row=1, column=0)  # spacer_1

        Label(frame, text='Input the desired Edge Weight').grid(row=2, column=0)
        weight = Text(frame, width=15, height=1)
        weight.grid(row=2, column=1)

        Label(frame, text='').grid(row=3, column=0)  # spacer_2

        ttk.Button(frame, text="Submit", command=lambda: self.set_edge_weight(edge=edge.get(), weight=int(weight.get("1.0", "end-1c")))).grid(row=4, column=0)

        frame.pack()

    def set_edge_weight(self, edge, weight):
        if weight <= 0:
            messagebox.showwarning("Error", "Weight needs to be a positive number")
            return

        temp = edge.split('-')

        start = ord(temp[0]) - ord('A')
        end = ord(temp[1]) - ord('A')

        if graph_type.get() == "Undirected":
            matrix[start][end] = weight
            matrix[end][start] = weight

        else:
            matrix[start][end] = weight

        pos_1 = nodes[start].pos
        pos_2 = nodes[end].pos
        point = ((pos_1[0] + pos_2[0]) / 2, (pos_1[1] + pos_2[1]) / 2)
        self.canvas.create_text(point[0], point[1] - 5, text=weight,
                                fill="Blue", font='Helvetica 15')

    def node_heuristic_canvas(self):
        global nodes_no

        if nodes_no == 0:
            messagebox.showwarning("Error", "Create some nodes first")
            return

        window = tk.Toplevel()
        frame = Frame(window)

        node_names = []

        for j in nodes:
            node_names.append(j.label)

        node = StringVar()
        node.set(node_names[0])

        OptionMenu(frame, node, *node_names).grid(row=0, column=0)

        Label(frame, text='').grid(row=1, column=0)  # spacer_1

        Label(frame, text='Input the desired Heuristic Weight').grid(row=2, column=0)
        heuristic_weight = Text(frame, width=15, height=1)
        heuristic_weight.grid(row=2, column=1)

        Label(frame, text='').grid(row=3, column=0)  # spacer_2

        ttk.Button(frame, text="Submit", command=lambda: self.set_node_heuristic_weight(node=node.get(), heuristic_weight=int(heuristic_weight.get("1.0", "end-1c")))).grid(row=4, column=0)
        frame.pack()

    def set_node_heuristic_weight(self, node, heuristic_weight):
        global nodes

        temp = ord(node) - ord('A')

        nodes[temp].heuristic_weight = heuristic_weight

        self.canvas.create_text(nodes[temp].pos[0] + 30, nodes[temp].pos[1] - 10, text=heuristic_weight,
                                fill="Blue", font='Helvetica 15')

        for j in nodes:
            print(j.label, ' ', j.heuristic_weight)

    def on_button_release(self, event):
        pass


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
