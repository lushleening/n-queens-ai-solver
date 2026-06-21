# N-Queens AI Solver (Tkinter Visualization)

An interactive N-Queens puzzle solver built using Python and Tkinter.  
The project demonstrates the backtracking algorithm through a visual board interface, along with real-time performance metrics for both AI and user interaction.

<img width="799" height="527" alt="image" src="https://github.com/user-attachments/assets/7e6961d5-67e8-495a-8497-0e73c31e38dd" />

<img width="1051" height="864" alt="image" src="https://github.com/user-attachments/assets/d71ebd4b-acab-4214-abe0-228722c5e5d5" />

---

## Overview

The N-Queens problem is a classic constraint satisfaction problem where N queens must be placed on an N×N chessboard such that no two queens attack each other (no shared row, column, or diagonal).

This application allows users to:
- Manually place queens on the board
- Visualize an AI backtracking solution
- Compare performance metrics between user and AI

---

## Features

### Interactive Board
- Click-based queen placement
- Hover highlighting for better UI experience
- Dynamic board rendering for different sizes (N×N)

### AI Solver (Backtracking)
- Automatically solves the N-Queens problem
- Visual step-by-step solving process
- Uses recursive backtracking algorithm

### User Play Mode
- Manually place queens on the board
- Check if the solution is valid
- Track user steps and runtime

### Performance Metrics
- AI:
  - Recursive calls
  - Iterations
  - Backtracks
  - Runtime
  - Steps taken
- User:
  - Steps
  - Runtime

---

## How It Works

The AI uses a **backtracking algorithm**:
1. Place a queen in a row
2. Check if the position is safe
3. Move to the next row recursively
4. If no valid position is found, backtrack

This continues until all queens are placed or all possibilities are exhausted.

---

## Validations & Edge Cases

- Prevents placing more than N queens
- Detects invalid configurations (attacking queens)
- Handles board sizes with no solution (N = 2, 3)
- Prevents invalid user inputs
- Ensures empty board safety checks

---

## Used :

- Python
- Tkinter (GUI)
- Time module (performance tracking)
