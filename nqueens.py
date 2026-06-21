import time
import tkinter as tk
from tkinter import messagebox, ttk

class Nqueens:
    def __init__(self, n): # self refers to the current object (instance) of the class

        # ai performance metrics
        self.iteration = 0 #node expansion
        self.recursivecall = 0
        self.runtime = 0
        self.solutions_found = 0
        self.backtrack = 0 # no of times queen was removed
        self.steps = 0
        
        self.user_steps = 0
        self.user_startTime = None
        self.user_runtime = 0

        self.boardsize = n
        self.highlight = None
        self.lockboard = False

        # board representation (2d array)
        self.boardmatrix = [[0 for col in range(n)] for row in range(n)]

        self.window = tk.Tk()
        self.window.title(f"{n}-Queens Game")
        self.window.configure(bg="#1a1a2e")
        self.window.resizable(False, False)

        self.window_width = 1100
        self.windowheight = 620
        self.cellsize = self.windowheight // n 
        # makes sure each cell is the same size

        # Main container
        mainframe = tk.Frame(self.window, bg="#1a1a2e")
        mainframe.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel
        left_panel = tk.Frame(mainframe, bg="#16213e", relief="flat", bd=0)
        left_panel.pack(side="left", padx=(0, 20), pady=10)
        
        self.canvas = tk.Canvas(left_panel, width=600, height=self.windowheight, 
                                bg="#0f3460", highlightthickness=2, highlightbackground="#e94560")
        self.canvas.pack(padx=15, pady=15)

        self.nqueens_board()
        self.canvas.bind("<Button-1>", self.detect_clicks)
        self.canvas.bind("<Motion>", self.highlight_box)
        self.canvas.bind("<Leave>", self.remove_highlight)

        # Button frame
        buttonframe = tk.Frame(self.window, bg="#1a1a2e")
        buttonframe.pack(pady=10)

        button_style = {
            "font": ("Segoe UI", 15, "bold"),
            "bg": "#e94560",
            "fg": "white",
            "relief": "flat",
            "cursor": "hand2",
            "padx": 20,
            "pady": 10,
            "bd": 0
        }

        self.ai_solve_button = tk.Button(buttonframe, text="AI Solve", **button_style, 
                                         command=self.nqueens_solver, activebackground="#c73652")
        self.ai_solve_button.pack(side="left", padx=5, pady=20)

        self.reset_button = tk.Button(buttonframe, text="Reset Board", **button_style, 
                                      command=self.reset_board, activebackground="#c73652")
        self.reset_button.pack(side="left", padx=5, pady=20)

        self.check_button = tk.Button(buttonframe, text="Check Answer", **button_style, 
                                      command=self.check_solution, activebackground="#c73652")
        self.check_button.pack(side="left", padx=5, pady=20)

        self.changeSize_button = tk.Button(buttonframe, text="Change Size", **button_style, 
                                           command=self.change_Boardsize, activebackground="#c73652")
        self.changeSize_button.pack(side="left", padx=5, pady=20)

        # Right panel - Metrics
        metrics_frame = tk.Frame(mainframe, bg="#16213e", width=350, height=self.windowheight)
        metrics_frame.pack(side="right", fill="y", padx=(10, 0), pady=10)
        metrics_frame.pack_propagate(False)

        # Title with accent line
        title_container = tk.Frame(metrics_frame, bg="#16213e")
        title_container.pack(pady=(20, 10))
        
        metrics_title = tk.Label(title_container, text="Performance Metrics", 
                                 font=("Segoe UI", 20, "bold"), bg="#16213e", fg="#e94560")
        metrics_title.pack()
        
        accent_line = tk.Frame(metrics_frame, height=3, bg="#e94560", width=200)
        accent_line.pack(pady=(0, 15))

        # AI Metrics section
        ai_section = tk.LabelFrame(metrics_frame, text="AI Performance", 
                                   font=("Segoe UI", 14, "bold"), bg="#16213e", fg="#ffffff",
                                   relief="flat", bd=2, highlightbackground="#2a2a4a")
        ai_section.pack(fill="x", padx=15, pady=(0, 15))
        
        self.iter_label = self.create_metric_label(ai_section, "Iterations", "0")
        self.recursive_label = self.create_metric_label(ai_section, "Recursive Calls", "0")
        self.backtrack_label = self.create_metric_label(ai_section, "Backtracks", "0")
        self.accuracy_label = self.create_metric_label(ai_section, "Accuracy", "0%")
        self.steps_label = self.create_metric_label(ai_section, "Steps Taken", "0")
        self.runtime_label = self.create_metric_label(ai_section, "Runtime", "0.0000s")

        # User Metrics section
        user_section = tk.LabelFrame(metrics_frame, text="User Performance", 
                                     font=("Segoe UI", 14, "bold"), bg="#16213e", fg="#ffffff",
                                     relief="flat", bd=2, highlightbackground="#2a2a4a")
        user_section.pack(fill="x", padx=15, pady=(0, 15))
        
        self.user_steps_label = self.create_metric_label(user_section, "Steps", "0")
        self.user_runtime_label = self.create_metric_label(user_section, "Runtime", "0.0000s")

        # Status indicator
        self.status_frame = tk.Frame(metrics_frame, bg="#16213e")
        self.status_frame.pack(pady=(10, 20))
        self.status_indicator = tk.Label(self.status_frame, text="● Ready", 
                                         font=("Segoe UI", 12, "bold"), 
                                         bg="#16213e", fg="#00d2ff")
        self.status_indicator.pack()

        self.window.mainloop()

    def create_metric_label(self, parent, label_text, initial_value):
        """Helper to create consistent metric labels"""
        frame = tk.Frame(parent, bg="#16213e")
        frame.pack(fill="x", padx=10, pady=5)
        
        label = tk.Label(frame, text=f"{label_text}:", font=("Segoe UI", 11), 
                         bg="#16213e", fg="#a8b2d1")
        label.pack(side="left")
        
        value_label = tk.Label(frame, text=initial_value, font=("Segoe UI", 11, "bold"), 
                               bg="#16213e", fg="#00d2ff")
        value_label.pack(side="right")
        
        return value_label

    def nqueens_board(self):
        # to formulate the grid/board
        self.canvas.delete("all")
        
        padding = 2
        for row in range(self.boardsize):
            for col in range(self.boardsize):
                x1 = col * self.cellsize + padding
                y1 = row * self.cellsize + padding
                x2 = x1 + self.cellsize - padding * 2
                y2 = y1 + self.cellsize - padding * 2

                if self.highlight == (row, col):
                    colour = "#00d2ff"
                elif (row + col) % 2 == 0:
                    colour = "#1a1a3e"
                else:
                    colour = "#2a2a5e"
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=colour, outline="")

                if self.boardmatrix[row][col] == 1:
                    font_size = self.cellsize // 2
                    for offset in range(3, 0, -1):
                        self.canvas.create_text(x1 + self.cellsize // 2, y1 + self.cellsize // 2, 
                                               text="♕", font=("Segoe UI", font_size + offset), 
                                               fill=f"#{'e94560' if offset == 1 else '2a2a5e'}")
                    self.canvas.create_text(x1 + self.cellsize // 2, y1 + self.cellsize // 2, 
                                           text="♕", font=("Segoe UI", font_size), fill="#e94560")

    def detect_clicks(self, event):
        if self.lockboard:
            return

        # detect the square that has been clicked (pixel pos divide cell size)
        row = event.y // self.cellsize
        col = event.x // self.cellsize

        if row < 0 or row >= self.boardsize or col < 0 or col >= self.boardsize:
            return

        if self.boardmatrix[row][col] == 0:
            self.boardmatrix[row][col] = 1
        else:
            self.boardmatrix[row][col] = 0
        
        self.user_steps += 1
        self.user_steps_label.config(text=str(self.user_steps))

        if self.user_startTime is None:
            self.user_startTime = time.time()

        self.nqueens_board()

    def highlight_box(self, event):
        row = event.y // self.cellsize
        col = event.x // self.cellsize

        if row < 0 or row >= self.boardsize or col < 0 or col >= self.boardsize:
            self.highlight = None
            self.nqueens_board()
            return
        
        if self.highlight != (row, col):
            self.highlight = (row, col)
            self.nqueens_board()
    
    def remove_highlight(self, event):
        self.highlight = None
        self.nqueens_board()

    def valid_pos(self, row, col):
        # check if column is occupied first (check if there's already a queen placed)
        for i in range(row):
            if self.boardmatrix[i][col] == 1:
                return False
            
        # check upper left diagonal
        i = row - 1
        j = col - 1

        while i >= 0 and j >= 0:
            if self.boardmatrix[i][j] == 1:
                return False
            i -= 1
            j -= 1

        # check upper right diagonal
        i = row - 1
        j = col + 1

        while i >= 0 and j < self.boardsize:
            if self.boardmatrix[i][j] == 1:
                return False
            i -= 1
            j += 1
        
        return True
           
    def nqueens_solver(self):
        self.lockboard = True
        self.status_indicator.config(text="● Solving...", fg="#f9a825")

        self.ai_solve_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.check_button.config(state="disabled")
        self.changeSize_button.config(state="disabled")

        self.iteration = 0
        self.recursivecall = 0
        self.backtrack = 0
        self.runtime = 0
        self.accuracy = 0
        self.steps = 0

        self.iter_label.config(text="0")
        self.recursive_label.config(text="0")
        self.backtrack_label.config(text="0")
        self.runtime_label.config(text="0.0000s")
        self.accuracy_label.config(text="0%")
        self.steps_label.config(text="0")

        self.boardmatrix = [[0 for col in range(self.boardsize)] for row in range(self.boardsize)]
        self.nqueens_board()

        if self.boardsize in (2, 3):
            messagebox.showerror("Note", f"There are actually no solutions for this specific board size! You may proceed to choose another boardsize or try to play it and understand why!")
            self.lockboard = False
            self.status_indicator.config(text="● No solution", fg="#e94560")
            
            self.ai_solve_button.config(state="normal")
            self.reset_button.config(state="normal")
            self.check_button.config(state="normal")
            self.changeSize_button.config(state="normal")
            return

        start_timer = time.time()
        
        def backtracking(row):
            self.recursivecall += 1 #checks how many time recursion goes deeper
            if row == self.boardsize:
                return True
            for col in range(self.boardsize):
                self.iteration += 1 # everytime a column is tested in a row
                if self.valid_pos(row, col):
                    self.boardmatrix[row][col] = 1
                    self.steps += 1
                    self.nqueens_board()
                    self.window.update()
                    self.window.after(0)
                    if backtracking(row + 1):
                        return True
                    self.boardmatrix[row][col] = 0
                    self.backtrack += 1 # increment backtrack when a queen is removed / no of undo
                    self.steps += 1
                    self.nqueens_board()
                    self.window.update()
                    self.window.after(0)
            return False
        
        found_solution = backtracking(0)
        self.accuracy = 100 if found_solution else 0
        end_timer = time.time()
        self.runtime = end_timer - start_timer

        self.iter_label.config(text=str(self.iteration))
        self.recursive_label.config(text=str(self.recursivecall))
        self.backtrack_label.config(text=str(self.backtrack))
        self.runtime_label.config(text=f"{self.runtime:.4f}s")
        self.accuracy_label.config(text=f"{self.accuracy}%")
        self.steps_label.config(text=str(self.steps))

        self.ai_solve_button.config(state="normal")
        self.reset_button.config(state="normal")
        self.check_button.config(state="normal")
        self.changeSize_button.config(state="normal")
        
        if found_solution:
            self.status_indicator.config(text="● Solved", fg="#00d2ff")
            messagebox.showinfo(
                f"{self.boardsize}-Queens", f"{self.boardsize}-Queens is solved!\n\n")
        else:
            self.status_indicator.config(text="● Failed", fg="#e94560")

    def reset_board(self):
        self.boardmatrix = [[0 for j in range(self.boardsize)] for i in range(self.boardsize)]
        self.lockboard = False

        self.user_runtime = 0
        self.user_startTime = None
        self.user_steps = 0

        self.user_runtime_label.config(text="0.0000s")
        self.user_steps_label.config(text="0")
        self.status_indicator.config(text="● Ready", fg="#00d2ff")

        self.nqueens_board()

    def change_Boardsize(self):
        self.window.destroy()
        entrypage()    

    def check_solution(self):
        if self.boardsize in (2, 3):
            messagebox.showerror("Note", f"There are actually no solutions for this board size as queens are either on the same diagonal or column! Please proceed to change to another board size!")
            return

        queens = sum(sum(row) for row in self.boardmatrix)
        if queens > self.boardsize:
            messagebox.showwarning("Check", f"Queens exceeded ({queens}), only {self.boardsize} queens are required.")
            return
        if queens == 0:
            messagebox.showwarning("Check", "No queens have been placed. Please place queens first")
            return
        if queens < self.boardsize:
            messagebox.showwarning("Check", f"Only ({queens}) queen was placed, {self.boardsize} queens are required")
            return 

        # Verify each queen position is valid
        for row in range(self.boardsize):
            for col in range(self.boardsize):
                if self.boardmatrix[row][col] == 1:
                    # Temporarily remove queen to avoid self check
                    self.boardmatrix[row][col] = 0
                    if not self.valid_pos(row, col):
                        self.boardmatrix[row][col] = 1
                        messagebox.showerror("Check", "Invalid arrangement! Queens are attacking each other.")
                        self.status_indicator.config(text="● Invalid", fg="#e94560")
                        return
                    self.boardmatrix[row][col] = 1
        
        if not self.lockboard and self.user_startTime is not None:
            self.user_runtime = time.time() - self.user_startTime
            self.user_runtime_label.config(text=f"{self.user_runtime:.4f}s")
            self.lockboard = True  
            self.status_indicator.config(text="● Valid Solution", fg="#00d2ff")
            messagebox.showinfo("Check", "Correct! Your solution is valid. Please reset the board to play again.")
        else:
            self.status_indicator.config(text="● Valid Solution", fg="#00d2ff")
            messagebox.showinfo("Check", "Correct! Your solution is valid. Please reset the board to play again.")

# --------------------------------------------------

def entrypage():

    frame = tk.Tk()
    frame.title("N-Queens Game")
    frame.geometry("800x500")
    frame.resizable(False, False)
    frame.configure(bg="#1a1a2e")

    style = ttk.Style()
    style.theme_use("clam")

    def start_game():
        
        try:
            n = int(entrySize.get())
            if n < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Input is invalid. Please enter a positive integer.")
            return

        frame.destroy()
        Nqueens(n)

    # Main container
    main_container = tk.Frame(frame, bg="#1a1a2e")
    main_container.pack(fill="both", expand=True, padx=40, pady=40)

    # Title section
    title_frame = tk.Frame(main_container, bg="#1a1a2e")
    title_frame.pack(pady=(0, 30))

    title_label = tk.Label(
        title_frame, text="N-Queens Solver",
        font=("Segoe UI", 36, "bold"), bg="#1a1a2e", fg="#e94560")
    title_label.pack()

    subtitle_label = tk.Label(
        title_frame, text="Place N queens on an N x N board so no two attack each other",
        font=("Segoe UI", 13), bg="#1a1a2e", fg="#a8b2d1")
    subtitle_label.pack(pady=(5, 0))

    # Input section
    input_frame = tk.Frame(main_container, bg="#16213e", relief="flat", bd=0)
    input_frame.pack(pady=20, padx=30, fill="x")
    input_frame.configure(highlightbackground="#2a2a4a", highlightthickness=2)

    input_inner = tk.Frame(input_frame, bg="#16213e")
    input_inner.pack(pady=25, padx=20)

    tk.Label(input_inner, text="Board Size (n):", font=("Segoe UI", 18), 
             bg="#16213e", fg="#ffffff").pack(side="left", padx=(0, 15))

    entrySize = tk.Entry(input_inner, font=("Segoe UI", 18), justify="center", 
                         bd=2, relief="flat", width=8, bg="#1a1a2e", fg="#00d2ff")
    entrySize.pack(side="left", padx=(0, 20))

    entrySize.bind("<Return>", lambda e: start_game())

    startButton = tk.Button(input_inner, text="Start Game", font=("Segoe UI", 18, "bold"),
                            bg="#e94560", fg="white", relief="flat", cursor="hand2",
                            padx=30, pady=8, activebackground="#c73652", command=start_game)
    startButton.pack(side="left")

    frame.mainloop()

if __name__ == "__main__":
    entrypage()