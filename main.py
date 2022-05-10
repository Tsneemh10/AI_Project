import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
# this is in python 3.4. For python 2.x import Tkinter
from PIL import Image, ImageTk

draw_nodes = True

# Constants
HEIGHT = 800
WIDTH = 800
NODE_SPACE_ALLOWANCE = 20
EDGE_COLOR = "Yellow"
EDGE_SIZE = 2
NODE_LABEL_COLOR = "White"
NODE_COLOR = "Red"
NODE_MARK_COLOR = "Green"

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

nodes_no = 0
visited = []

dfs_counter = 0
visited_nodes = []

graph_type = ''

selected_search_algorithm = ''
search_algorithms = ('BFS', 'DFS', 'Depth Limited', 'Uniform Cost', 'Greedy', 'A*')


class Point:
    def __init__(self, pos, label):
        self.pos = pos
        self.index = 0
        self.label = label


def stop_nodes():
    global draw_nodes, matrix, nodes_no, visited
    draw_nodes = False
    matrix = [[0 for i in range(nodes_no)]
              for j in range(nodes_no)]
    visited = [False] * nodes_no


class ExampleApp(tk.Tk):

    def __init__(self):

        global graph_type, selected_search_algorithm

        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.canvas = tk.Canvas(self, width=512, height=512, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)

        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        ttk.Button(self, text="Lock nodes", command= stop_nodes ).pack()

        self.entry = Entry(self, width=12)
        self.entry.focus_set()
        self.entry.pack()
        ttk.Button(self, text="DFS", command=lambda: self.DFS(0)).pack()
        tk.Button(self, text="Traverse graph", command=self.dfs_traversal).pack()
        ttk.Button(self, text="Set Edge Weights", command=lambda: self.edge_weights_canvas()).pack()

        Label(self, text='Select the desired graph type').pack()

        graph_type = StringVar()
        graph_type.set("Undirected")

        tk.Radiobutton(self, text="Undirected", variable=graph_type, value="Undirected").pack()
        tk.Radiobutton(self, text="Directed", variable=graph_type, value="Directed").pack()

        Label(self, text='Select the desired search algorithm').pack()

        selected_search_algorithm = StringVar()
        selected_search_algorithm.set('BFS')

        OptionMenu(self, selected_search_algorithm, *search_algorithms).pack()

        self.rect = None
        self.center = [0, 0]

    def on_button_press(self, event):
        global draw_nodes, i, nodes, pos1, pos2, click, index1, index2, nodes_no, matrix
        # save mouse drag start position
        self.center[0] = event.x
        self.center[1] = event.y
        oval_lower = [self.center[0] + 15, self.center[1] + 15]

        # for node in nodes:
        #     if ((event.x > node.pos[0] and event.x < node.pos[0] + 15) and (event.y > node.pos[1] and event.x < node.pos[1] + 15)):
        #         draw_nodes= False
        #         break
        #     else:
        #         draw_nodes= True
        #

        if draw_nodes:

            self.rect = self.canvas.create_oval(self.center[0], self.center[1], oval_lower[0],
                                                oval_lower[1], fill="Black")
            self.rect = self.canvas.create_text(self.center[0], self.center[1] - 5, text=chr(ord("A") + i),
                                                fill="Black")

            nodes.append(Point([event.x, event.y], chr(ord("A") + i)))
            i = i + 1
            nodes_no += 1

        else:

            for i in range (len(nodes)):
                if ( ( (event.x >= nodes[i].pos[0]) and (event.y >= nodes[i].pos[1]) ) and ( (event.x <= nodes[i].pos[0]+15) and (event.y <= nodes[i].pos[1]+15)) ):
                    if click == 0:
                        pos1 = [(nodes[i].pos[0]+nodes[i].pos[0]+15)/2, (nodes[i].pos[1]+nodes[i].pos[1]+15)/2 ]
                        click = 1
                        index1 = i
                        break

                    if click == 1:
                        pos2 = [(nodes[i].pos[0]+nodes[i].pos[0]+15)/2, (nodes[i].pos[1]+nodes[i].pos[1]+15)/2 ]
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
                    self.canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], fill="black", width=2, arrow=tk.LAST, arrowshape=(25, 25, 10))
                    click = 0
                    matrix[index1][index2] = 1
                    # matrix[index2][index1] = 1

    def bfs(self):
        global nodes_no, visited, dfs_counter, matrix, visited_nodes, nodes
        for c in range(nodes_no):
            if matrix[start][c] == 5:
                visited_nodes.append(nodes[c].pos)


    def DFS(self, start):

        global nodes_no, visited, dfs_counter, matrix, visited_nodes, nodes

        if dfs_counter == 0:
            string = self.entry.get()
            start = ord(string) - ord('@') - 1
            dfs_counter = 1
            visited_nodes.append(nodes[start].pos)

        visited[start] = True

        for i in range(nodes_no):
            if matrix[start][i] == 1 and (visited[i] == False):
                visited_nodes.append(nodes[i].pos)
                self.DFS(i)

    def dfs_traversal(self):

        global visited_nodes
        print (visited_nodes)
        for i in range(nodes_no):
             point = visited_nodes[i]
             point1 = [ (point[0] + (point[0]+15))/2, (point[1] + (point[1]+15))/2]
             self.rect = self.canvas.create_oval(point[0], point[1], point[0] + 15, point[1] + 15, fill="Red")
             time.sleep(0.5)
             self.canvas.update_idletasks()
             max = len(visited_nodes)

             if i != max-1:
                 point2_temp = visited_nodes[i + 1]
                 point2 = [(point2_temp[0] + point2_temp[0] + 15) / 2, (point2_temp[1] + point2_temp[1] + 15) / 2]
                 self.canvas.create_line(point1[0], point1[1], point2[0], point2[1], fill="red", width=2)
                 time.sleep(0.5)
                 self.canvas.update_idletasks()


             # if nodes:
             #     for p, location in enumerate(nodes):
             #         if (self.oval_upper[0]  >= nodes[p].oval_lower[0]   and self.oval_upper[1]  >= nodes[p].oval_lower[1] and
             #             self.oval_upper[0] >= nodes[p].oval_lower[0] and self.oval_upper[1] >= nodes[p].oval_lower[1]  ) or (self.oval_lower)


    def edge_weights_canvas(self):
        window = tk.Toplevel()
        canvas = tk.Canvas(window, height=200, width=200)
        canvas.pack()

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

        edge = StringVar()
        edge.set(edges[0])

        OptionMenu(canvas, edge, *edges).pack()
        Label(canvas, text='Input the desired Weight').pack()
        weight = Text(canvas, width=10, height=10)
        weight.pack()
        ttk.Button(canvas, text="Submit", command=lambda: self.set_edge_weight(edge=edge.get(), weight=int(weight.get("1.0", "end-1c")))).pack()

    def set_edge_weight(self, edge, weight):
        temp = edge.split('-')

        start = ord(temp[0]) - ord('A')
        end = ord(temp[1]) - ord('A')

        for j in matrix:
            print(j)

        if graph_type.get() == "Undirected":
            matrix[start][end] = weight
            matrix[end][start] = weight
        else:
            matrix[start][end] = weight

        for j in matrix:
            print(j)

    def on_button_release(self, event):
        pass


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
