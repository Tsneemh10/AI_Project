import time
import tkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk
# this is in python 3.4. For python 2.x import Tkinter
from PIL import Image, ImageTk

draw_nodes= True

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
draw_relations = False
draw_mark_relations = False
setGoal = False
setStart = False
displayResult = False
nodes = []
pos1= [0,0]
pos2 = [0,0]
click= 0

index1= 0
index2=0

matrix= []

nodes_no=0
visited=[]

dfs_counter=0
visited_nodes=[]


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

        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.canvas = tk.Canvas(self, width=512, height=512, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)

        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        ttk.Button(self, text="Lock nodes", command= stop_nodes ).pack()

        self.entry = Entry(self, width=12 )
        self.entry.focus_set()
        self.entry.pack()
        ttk.Button(self, text="DFS", command=lambda: self.DFS( 0)).pack()
        tk.Button(self, text="Traverse graph", command=self.dfs_traversal).pack()




        self.rect = None
        self.center= [0,0]












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


        if draw_nodes == True:

            self.rect = self.canvas.create_oval(self.center[0], self.center[1], oval_lower[0],
                                                oval_lower[1], fill="Black")
            self.rect = self.canvas.create_text(self.center[0], self.center[1] - 5, text=chr(ord("A") + i),
                                                fill="Black")

            nodes.append(Point([event.x, event.y], chr(ord("A") + i)))
            i = i + 1
            nodes_no+=1

        else:

            for i in range (len(nodes)):
                if ( ( (event.x >= nodes[i].pos[0]) and (event.y >= nodes[i].pos[1]) ) and ( (event.x <= nodes[i].pos[0]+15) and (event.y <= nodes[i].pos[1]+15)) ):
                    if (click == 0):
                        pos1 = [(nodes[i].pos[0]+nodes[i].pos[0]+15)/2, (nodes[i].pos[1]+nodes[i].pos[1]+15)/2 ]
                        click = 1
                        index1 = i
                        break

                    if (click == 1 ):
                        pos2 = [(nodes[i].pos[0]+nodes[i].pos[0]+15)/2, (nodes[i].pos[1]+nodes[i].pos[1]+15)/2 ]
                        click = 2
                        index2 = i
                        break
            if (click == 2):
                self.canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], fill="black", width=2)
                click=0
                matrix[index1][index2] = 1
                matrix[index2][index1] = 1


    def DFS(self, start):


        global nodes_no, visited, dfs_counter, matrix, visited_nodes,nodes

        if(dfs_counter==0):
             string = self.entry.get()
             start = ord(string) - ord('@') - 1
             dfs_counter=1
             visited_nodes.append(nodes[start].pos)



        visited[start] = True




        for i in range(nodes_no):
            if (matrix[start][i] == 1 and (visited[i]== False)):
                visited_nodes.append(nodes[i].pos)
                self.DFS(i)

    def dfs_traversal (self):

        global visited_nodes
        print (visited_nodes)
        for node in visited_nodes:
             self.rect = self.canvas.create_oval(node[0], node[1], node[0] +15,node[1] + 15, fill="Red")
             time.sleep(1)
             self.canvas.update_idletasks()

































             # if nodes:
             #     for p, location in enumerate(nodes):
             #         if (self.oval_upper[0]  >= nodes[p].oval_lower[0]   and self.oval_upper[1]  >= nodes[p].oval_lower[1] and
             #             self.oval_upper[0] >= nodes[p].oval_lower[0] and self.oval_upper[1] >= nodes[p].oval_lower[1]  ) or (self.oval_lower)








    def on_button_release(self, event):
        pass


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()