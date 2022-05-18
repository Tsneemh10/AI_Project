from tkinter import *

root = Tk()
root.title('test_window')

main_frame = Frame(root)

frame_2 = Frame(main_frame)
frame_2.grid(row=0, column=1)

Canvas(main_frame, width=800, height=600, background="grey").grid(row=0, column=0)

Button(frame_2, text="Lock nodes").grid(row=0, column=0)

Label(frame_2, text=' ').grid(row=1, column=0)  # spacer_1

Label(frame_2, text='Enter the start node').grid(row=2, column=0)

Entry(frame_2, width=12).grid(row=2, column=1)

Label(frame_2, text='Enter the goal node').grid(row=3, column=0)

Entry(frame_2, width=12).grid(row=3, column=1)

Label(frame_2, text=' ').grid(row=4, column=0)  # spacer_2

Button(frame_2, text="Traverse graph").grid(row=5, column=0)
Button(frame_2, text="Set Edge Weights").grid(row=6, column=0)
Button(frame_2, text="Set Node Heuristic").grid(row=7, column=0)
Label(frame_2, text='Select the desired graph type').grid(row=8, column=0)

main_frame.pack()

root.mainloop()
