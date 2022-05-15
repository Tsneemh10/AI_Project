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
ANIMATION_DELAY = 0.5

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
Iterations_vertices=[]
graph_type = ''
iteration_counter=0
returnV = True
selected_search_algorithm = ''
search_algorithms = ('BFS', 'DFS', 'Iterative Deepening', 'Depth Limited', 'Uniform Cost', 'Greedy', 'A*')


class Point:
    def __init__(self, pos, label):
        self.pos = pos
        self.index = 0
        self.label = label
        self.heuristic_weight = 0


def stop_nodes():
    global draw_nodes, matrix, nodes_no, visited, temp_matrix
    draw_nodes = False
    matrix = [[0 for i in range(nodes_no)]
              for j in range(nodes_no)]
    temp_matrix = [[0 for i in range(nodes_no)]
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

        Label(self, text='Enter the start node').pack()

        self.start_node = Entry(self, width=12)
        self.start_node.focus_set()
        self.start_node.pack()

        Label(self, text='Enter the goal node').pack()

        self.goal_node = Entry(self, width=12)
        self.goal_node.focus_set()
        self.goal_node.pack()

        self.goal_node_index = 0

        self.goal_coords = [0, 0]

        tk.Button(self, text="Traverse graph", command=self.traverse_graph).pack()
        ttk.Button(self, text="Set Edge Weights", command=lambda: self.edge_weights_canvas()).pack()
        ttk.Button(self, text="Set Node Heuristic", command=lambda: self.node_heuristic_canvas()).pack()

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
                                                fill="Blue", font=('Helvetica 15'))

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
                    self.canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], fill="black", width=2, arrow=tk.LAST, arrowshape=(15, 15, 10))
                    click = 0
                    matrix[index1][index2] = 1
                    # matrix[index2][index1] = 1

    def bfs(self, start):

        global nodes_no, visited, matrix, visited_nodes, nodes
        visited = [False] * nodes_no
        q = [start]

        # Set source as visited
        visited[start] = True
        visited_nodes.append(nodes[start].pos)

        while q:
            vis = q[0]

            # Print current node
            print(vis, end=' ')
            q.pop(0)

            # For every adjacent vertex to
            # the current vertex
            for i in range(nodes_no):
                if (matrix[vis][i] == 1 and
                        (not visited[i])):
                    # Push the adjacent node
                    # in the queue
                    q.append(i)
                    visited_nodes.append(nodes[i].pos)
                    # set
                    visited[i] = True


    def DFS(self, start):

        global nodes_no, visited, dfs_counter, matrix, visited_nodes, nodes

        if dfs_counter == 0:
            dfs_counter = 1
            visited_nodes.append(nodes[start].pos)

        visited[start] = True

        for i in range(nodes_no):
            if matrix[start][i] == 1 and (visited[i] == False):
                visited_nodes.append(nodes[i].pos)
                self.DFS(i)

    def Iterative_deepening_preparation(self, start):

        global nodes_no, visited, dfs_counter, matrix, visited_nodes, nodes, iteration_counter, temp_matrix, returnV, Iterations_vertices



        if (iteration_counter == 0):
            for i in range(nodes_no):
                for j in range(nodes_no):
                    temp_matrix[i][j]= 0

        if (iteration_counter==0):
            Iterations_vertices.append(start)


        if (iteration_counter!=0):


            if (iteration_counter==1):
                for i in range(nodes_no):
                    temp_matrix[start][i]= matrix[start][i]
                    if  temp_matrix[start][i]==1:
                        Iterations_vertices.append(i)

            else:
                for i in range(len(Iterations_vertices)):
                    for j in range(nodes_no):
                        temp_matrix[Iterations_vertices[i]][j]= matrix[Iterations_vertices[i]][j]
                        if(temp_matrix[Iterations_vertices[i]][j]==1):
                            Iterations_vertices.append(j)


        iteration_counter += 1
        # self.Iterative_DFS(start)
        # for i in range(len(visited_nodes)):
        #     point = visited_nodes[i]
        #     self.rect = self.canvas.create_oval(point[0], point[1], point[0] + 15, point[1] + 15, fill="Black")



        # if(iteration_counter!=0):
        #     if (returnV):
                # for i in range(len(visited_nodes)):
                #     point = visited_nodes[i]
                #     self.rect = self.canvas.create_oval(point[0], point[1], point[0] + 15, point[1] + 15, fill="Black")
                #     time.sleep(ANIMATION_DELAY)
                #     self.canvas.update_idletasks()
                #self.traverse_graph()

        # if(returnV):
        #     self.Iterative_deepening_preparation()




    def Iterative_DFS(self, start):

        global nodes_no, visited, dfs_counter, temp_matrix, visited_nodes, nodes, returnV
        print("H")
        if dfs_counter == 0:
            visited_nodes.append(nodes[start].pos)
            dfs_counter = 1

        visited[start] = True

        for i in range(nodes_no):
            if temp_matrix[start][i] == 1 and (visited[i] == False):
                print (i)
                visited_nodes.append(nodes[i].pos)
                self.Iterative_DFS(i)

        return True


    def Perform_steps(self):
        global returnV, visited, dfs_counter
        self.Iterative_deepening_preparation(start=start)
        self.Iterative_DFS(start)
        print(temp_matrix)
        print (visited_nodes)
        for i in range(len(visited_nodes)):
            point = visited_nodes[i]

            if point == self.goal_coords:
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
            visited[i]= False
        visited_nodes.clear()
        dfs_counter=0





    def traverse_graph(self):

        global visited_nodes, selected_search_algorithm, start , returnV

        if len(self.start_node.get()) != 0:
            start = ord(self.start_node.get()) - ord('@') - 1
            self.goal_node_index = ord(self.goal_node.get()) - ord('@') - 1
            self.goal_coords = nodes[self.goal_node_index].pos



        if selected_search_algorithm.get() == 'DFS':
            self.DFS(start=start),

        elif selected_search_algorithm.get() == 'BFS':
            self.bfs(start=start),
        elif selected_search_algorithm.get() == 'Iterative Deepening':
            # if (returnV):
            self.Perform_steps(),


        # print (visited_nodes)
        # for i in range(len(visited_nodes)):
        #     point = visited_nodes[i]
        #
        #     if point == self.goal_coords:
        #         time.sleep(ANIMATION_DELAY)
        #         self.rect = self.canvas.create_oval(point[0], point[1], point[0] + 15, point[1] + 15, fill="Green")
        #         returnV = False
        #         return
        #
        #     # point1 = [ (point[0] + (point[0]+15))/2, (point[1] + (point[1]+15))/2]
        #     self.rect = self.canvas.create_oval(point[0], point[1], point[0] + 15, point[1] + 15, fill="Red")
        #     time.sleep(ANIMATION_DELAY)
        #     self.canvas.update_idletasks()


            # max = len(visited_nodes)

            # if i != max-1:
            #     point2_temp = visited_nodes[i + 1]
            #     point2 = [(point2_temp[0] + point2_temp[0] + 15) / 2, (point2_temp[1] + point2_temp[1] + 15) / 2]
            #     self.canvas.create_line(point1[0], point1[1], point2[0], point2[1], fill="red", width=2)
            #     time.sleep(0.5)
            #     self.canvas.update_idletasks()


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

    def node_heuristic_canvas(self):
        window = tk.Toplevel()
        canvas = tk.Canvas(window, height=200, width=200)
        canvas.pack()

        for j in nodes:
            print(j.pos)
            print(j.heuristic_weight)

    def on_button_release(self, event):
        pass


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()