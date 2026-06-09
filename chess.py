import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk

chessboard = tk.Tk()
chessboard.title("Chess star")
chessboard.configure(bg="#2e2e2e")
chessboard.geometry("600x600")
chessboard.resizable(False, False)

notaion = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

piece = {" ": " "}

file = {
    "p": "pieces\\bP.png", "r": "pieces\\bR.png", "n": "pieces\\bN.png",
    "b": "pieces\\bB.png", "q": "pieces\\bQ.png", "k": "pieces\\bK.png",
    "P": "pieces\\wP.png", "R": "pieces\\wR.png", "N": "pieces\\wN.png",
    "B": "pieces\\wB.png", "Q": "pieces\\wQ.png", "K": "pieces\\wK.png"
}

for key, value in file.items():
    img = Image.open(value).resize((60, 60), Image.LANCZOS).convert("RGBA")
    piece[key] = ImageTk.PhotoImage(img)

board = tk.Canvas(chessboard, width=480, height=480)
board.pack(pady=20, padx=20)

def draw_board():
    board.delete("square")
    for row in range(8):
        for col in range(8):
            color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
            x1, y1 = col * 60, row * 60
            board.create_rectangle(x1, y1, x1 + 60, y1 + 60, fill=color, tag="square")

def draw_pieces():
    board.delete("piece")
    for row in range(8):
        for col in range(8):
            pieces = notaion[row][col]
            if pieces != " ":
                x, y = col * 60 + 30, row * 60 + 30
                board.create_image(x, y, image=piece[pieces], tag="piece")

st = ["black"]

def turn():
    st[0] = "black" if st[0] == "white" else "white"
    return st[0]

def highlight(row, col):
    board.delete("select")
    x1, y1 = col * 60, row * 60
    board.create_rectangle(x1, y1, x1 + 60, y1 + 60,
                           outline="#FFD700", width=4, tag="select")

# ── castling rights ──────────────────────────────────────────────────────────
castle_rights = {
    "K": True, "Q": True, "k": True, "q": True
}

# ── en passant target square ─────────────────────────────────────────────────
en_passant_target = [None]   # (row, col) of capturable pawn, or None

# ── helpers ──────────────────────────────────────────────────────────────────
def is_friendly(p, r, c):
    t = notaion[r][c]
    return t != " " and ((p.isupper() and t.isupper()) or (p.islower() and t.islower()))

def slide(r, c, dr, dc, p):
    moves = []
    nr, nc = r + dr, c + dc
    while 0 <= nr <= 7 and 0 <= nc <= 7:
        if notaion[nr][nc] == " ":
            moves.append((nr, nc))
        elif not is_friendly(p, nr, nc):
            moves.append((nr, nc))
            break
        else:
            break
        nr += dr; nc += dc
    return moves

def find_king(color):
    k = "K" if color == "white" else "k"
    for r in range(8):
        for c in range(8):
            if notaion[r][c] == k:
                return (r, c)

def is_attacked(r, c, by_color):
    """Check if square (r,c) is attacked by any piece of by_color."""
    for row in range(8):
        for col in range(8):
            p = notaion[row][col]
            if p == " ": continue
            if by_color == "white" and not p.isupper(): continue
            if by_color == "black" and not p.islower(): continue
            if (r, c) in raw_moves(row, col):
                return True
    return False

def raw_moves(row, col):
    """Moves without check filtering (used inside is_attacked to avoid recursion)."""
    p = notaion[row][col]
    moves = []

    if p == "P":
        if row > 0 and notaion[row-1][col] == " ":
            moves.append((row-1, col))
            if row == 6 and notaion[row-2][col] == " ":
                moves.append((row-2, col))
        for dc in [-1, 1]:
            if 0 <= col+dc <= 7 and row > 0 and notaion[row-1][col+dc].islower():
                moves.append((row-1, col+dc))

    elif p == "p":
        if row < 7 and notaion[row+1][col] == " ":
            moves.append((row+1, col))
            if row == 1 and notaion[row+2][col] == " ":
                moves.append((row+2, col))
        for dc in [-1, 1]:
            if 0 <= col+dc <= 7 and row < 7 and notaion[row+1][col+dc].isupper():
                moves.append((row+1, col+dc))

    elif p in ("N", "n"):
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            nr, nc = row+dr, col+dc
            if 0 <= nr <= 7 and 0 <= nc <= 7 and not is_friendly(p, nr, nc):
                moves.append((nr, nc))

    elif p in ("B", "b"):
        for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            moves += slide(row, col, dr, dc, p)

    elif p in ("R", "r"):
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            moves += slide(row, col, dr, dc, p)

    elif p in ("Q", "q"):
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            moves += slide(row, col, dr, dc, p)

    elif p in ("K", "k"):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = row+dr, col+dc
                if 0 <= nr <= 7 and 0 <= nc <= 7 and not is_friendly(p, nr, nc):
                    moves.append((nr, nc))

    return moves

def valid_moves(row, col):
    p = notaion[row][col]
    color = "white" if p.isupper() else "black"
    enemy = "black" if color == "white" else "white"
    candidates = []

    if p == "P":
        if row > 0 and notaion[row-1][col] == " ":
            candidates.append((row-1, col))
            if row == 6 and notaion[row-2][col] == " ":
                candidates.append((row-2, col))
        for dc in [-1, 1]:
            if 0 <= col+dc <= 7 and row > 0 and notaion[row-1][col+dc].islower():
                candidates.append((row-1, col+dc))
        # en passant
        if en_passant_target[0]:
            er, ec = en_passant_target[0]
            if er == row-1 and abs(ec - col) == 1:
                candidates.append((er, ec))

    elif p == "p":
        if row < 7 and notaion[row+1][col] == " ":
            candidates.append((row+1, col))
            if row == 1 and notaion[row+2][col] == " ":
                candidates.append((row+2, col))
        for dc in [-1, 1]:
            if 0 <= col+dc <= 7 and row < 7 and notaion[row+1][col+dc].isupper():
                candidates.append((row+1, col+dc))
        # en passant
        if en_passant_target[0]:
            er, ec = en_passant_target[0]
            if er == row+1 and abs(ec - col) == 1:
                candidates.append((er, ec))

    elif p in ("N", "n"):
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            nr, nc = row+dr, col+dc
            if 0 <= nr <= 7 and 0 <= nc <= 7 and not is_friendly(p, nr, nc):
                candidates.append((nr, nc))

    elif p in ("B", "b"):
        for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            candidates += slide(row, col, dr, dc, p)

    elif p in ("R", "r"):
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            candidates += slide(row, col, dr, dc, p)

    elif p in ("Q", "q"):
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            candidates += slide(row, col, dr, dc, p)

    elif p in ("K", "k"):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = row+dr, col+dc
                if 0 <= nr <= 7 and 0 <= nc <= 7 and not is_friendly(p, nr, nc):
                    candidates.append((nr, nc))
        # castling
        if p == "K" and row == 7 and col == 4:
            if castle_rights["K"] and notaion[7][5] == " " and notaion[7][6] == " ":
                if not is_attacked(7,4,enemy) and not is_attacked(7,5,enemy) and not is_attacked(7,6,enemy):
                    candidates.append((7, 6))
            if castle_rights["Q"] and notaion[7][3] == " " and notaion[7][2] == " " and notaion[7][1] == " ":
                if not is_attacked(7,4,enemy) and not is_attacked(7,3,enemy) and not is_attacked(7,2,enemy):
                    candidates.append((7, 2))
        elif p == "k" and row == 0 and col == 4:
            if castle_rights["k"] and notaion[0][5] == " " and notaion[0][6] == " ":
                if not is_attacked(0,4,enemy) and not is_attacked(0,5,enemy) and not is_attacked(0,6,enemy):
                    candidates.append((0, 6))
            if castle_rights["q"] and notaion[0][3] == " " and notaion[0][2] == " " and notaion[0][1] == " ":
                if not is_attacked(0,4,enemy) and not is_attacked(0,3,enemy) and not is_attacked(0,2,enemy):
                    candidates.append((0, 2))

    # ── filter moves that leave own king in check ────────────────────────────
    legal = []
    for (tr, tc) in candidates:
        # simulate move
        saved = notaion[tr][tc]
        ep_captured = None
        # en passant capture simulation
        if p in ("P","p") and (tr,tc) == en_passant_target[0]:
            ep_row = tr+1 if p == "P" else tr-1
            ep_captured = notaion[ep_row][tc]
            notaion[ep_row][tc] = " "
        notaion[tr][tc] = p
        notaion[row][col] = " "
        kr, kc = find_king(color)
        if not is_attacked(kr, kc, enemy):
            legal.append((tr, tc))
        # undo
        notaion[row][col] = p
        notaion[tr][tc] = saved
        if ep_captured is not None:
            ep_row = tr+1 if p == "P" else tr-1
            notaion[ep_row][tc] = ep_captured

    return legal

def is_in_check(color):
    enemy = "black" if color == "white" else "white"
    kr, kc = find_king(color)
    return is_attacked(kr, kc, enemy)

def has_any_legal_move(color):
    for r in range(8):
        for c in range(8):
            p = notaion[r][c]
            if p == " ": continue
            if color == "white" and not p.isupper(): continue
            if color == "black" and not p.islower(): continue
            if valid_moves(r, c):
                return True
    return False

def check_game_over(color):
    """Call after a move with the color whose turn it now is."""
    if not has_any_legal_move(color):
        if is_in_check(color):
            winner = "White" if color == "black" else "Black"
            tk.messagebox.showinfo("Checkmate!", f"Checkmate! {winner} wins!")
        else:
            tk.messagebox.showinfo("Stalemate!", "Stalemate! It's a draw.")

def promote_pawn(row, col):
    """Ask player which piece to promote to."""
    p = notaion[row][col]
    color = "white" if p == "P" else "black"
    choices = ["Q", "R", "B", "N"] if color == "white" else ["q", "r", "b", "n"]
    labels = {"Q":"Queen","R":"Rook","B":"Bishop","N":"Knight",
              "q":"Queen","r":"Rook","b":"Bishop","n":"Knight"}

    win = tk.Toplevel(chessboard)
    win.title("Promote Pawn")
    win.configure(bg="#2e2e2e")
    win.resizable(False, False)
    win.grab_set()
    tk.Label(win, text="Choose promotion:", bg="#2e2e2e", fg="white",
             font=("Arial", 12)).pack(pady=10)

    chosen = [choices[0]]
    def pick(c):
        chosen[0] = c
        win.destroy()

    for ch in choices:
        tk.Button(win, text=labels[ch], width=10,
                  command=lambda c=ch: pick(c)).pack(pady=3)

    chessboard.wait_window(win)
    notaion[row][col] = chosen[0]
    # reload image if not already cached (should be)
    draw_board()
    draw_pieces()

def do_castle(row, col):
    if col == 6:
        notaion[row][5] = notaion[row][7]
        notaion[row][7] = " "
    elif col == 2:
        notaion[row][3] = notaion[row][0]
        notaion[row][0] = " "

def update_castle_rights(from_row, from_col):
    p = notaion[from_row][from_col]
    if p == "K": castle_rights["K"] = castle_rights["Q"] = False
    elif p == "k": castle_rights["k"] = castle_rights["q"] = False
    elif p == "R":
        if from_row == 7 and from_col == 7: castle_rights["K"] = False
        if from_row == 7 and from_col == 0: castle_rights["Q"] = False
    elif p == "r":
        if from_row == 0 and from_col == 7: castle_rights["k"] = False
        if from_row == 0 and from_col == 0: castle_rights["q"] = False

# ─────────────────────────────────────────────────────────────────────────────

selected = None

def on_click(event):
    global selected
    col = event.x // 60
    row = event.y // 60
    current_turn = turn()

    if row > 7 or col > 7:
        return

    if selected is None:
        if (current_turn == "white" and notaion[row][col].isupper()):
            if notaion[row][col] != " ":
                selected = (row, col)
                highlight(row, col)
        elif (current_turn == "black" and notaion[row][col].islower()):
            if notaion[row][col] != " ":
                selected = (row, col)
                highlight(row, col)
        current_turn = turn()
    else:
        if (current_turn == "white"):
            from_row, from_col = selected
            if notaion[from_row][from_col].isupper():
                moves = valid_moves(from_row, from_col)
                if (row, col) in moves:
                    update_castle_rights(from_row, from_col)
                    # en passant capture
                    if notaion[from_row][from_col] == "P" and (row, col) == en_passant_target[0]:
                        notaion[row+1][col] = " "
                    # castling
                    if notaion[from_row][from_col] == "K" and abs(col - from_col) == 2:
                        do_castle(row, col)
                    # set en passant target
                    if notaion[from_row][from_col] == "P" and from_row - row == 2:
                        en_passant_target[0] = (row, col)
                    else:
                        en_passant_target[0] = None
                    notaion[row][col] = notaion[from_row][from_col]
                    notaion[from_row][from_col] = " "
                    selected = None
                    board.delete("select")
                    draw_board()
                    draw_pieces()
                    # pawn promotion
                    if notaion[row][col] == "P" and row == 0:
                        promote_pawn(row, col)
                    check_game_over("black")

        elif (current_turn == "black"):
            from_row, from_col = selected
            if notaion[from_row][from_col].islower():
                moves = valid_moves(from_row, from_col)
                if (row, col) in moves:
                    update_castle_rights(from_row, from_col)
                    # en passant capture
                    if notaion[from_row][from_col] == "p" and (row, col) == en_passant_target[0]:
                        notaion[row-1][col] = " "
                    # castling
                    if notaion[from_row][from_col] == "k" and abs(col - from_col) == 2:
                        do_castle(row, col)
                    # set en passant target
                    if notaion[from_row][from_col] == "p" and row - from_row == 2:
                        en_passant_target[0] = (row, col)
                    else:
                        en_passant_target[0] = None
                    notaion[row][col] = notaion[from_row][from_col]
                    notaion[from_row][from_col] = " "
                    selected = None
                    board.delete("select")
                    draw_board()
                    draw_pieces()
                    # pawn promotion
                    if notaion[row][col] == "p" and row == 7:
                        promote_pawn(row, col)
                    check_game_over("white")

import tkinter.messagebox

draw_board()
draw_pieces()
board.bind("<Button-1>", on_click)
chessboard.mainloop()