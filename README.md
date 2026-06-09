# ♟️ Chess

A desktop chess game built with Python and Tkinter.

---

## 👤 Built By

**Ankit** — Core application, UI, board rendering, piece management, and turn system.

**Claude (AI)** — Move validation logic, castling logic.

---

## ✅ What Ankit Built

### 🖼️ Application & UI
- Main window setup with `tkinter` (`600x600`, dark theme `#2e2e2e`, non-resizable)
- Canvas-based chessboard (`480x480`) with proper padding
- Board drawn using alternating light (`#f0d9b5`) and dark (`#b58863`) squares
- Piece images loaded from `pieces\` folder using `Pillow`, resized to `60x60` with LANCZOS, converted to RGBA for transparency

### 📋 Board State
- `notaion` — 8×8 nested list representing the full board state
  - Uppercase = White pieces (`P R N B Q K`)
  - Lowercase = Black pieces (`p r n b q k`)
- `piece` dict — maps piece characters to `ImageTk.PhotoImage` objects

### 🔄 Turn System
- list for mutable turn state inside functions
- `turn()` — toggles and returns the current turn
- Turn alternates correctly on every valid move

### 🖱️ Click & Selection System
- `on_click(event)` — handles all mouse clicks on the board
- First click selects a friendly piece (validated by case: upper = white, lower = black)
- Second click attempts to move the selected piece to the target square
- `highlight()` — draws a gold (`#FFD700`) border around the selected piece
- `selected` global tracks the currently selected square

### 🎨 Rendering
- `draw_board()` — redraws all 64 squares with correct colors
- `draw_pieces()` — redraws all pieces from current `notaion` state
- Board and pieces are fully redrawn after every valid move

---

## 🤖 What Claude Added

### ♟️ Move Validation (`valid_moves`)
Pure logic layer — no UI changes. Returns a list of legal `(row, col)` destinations for any piece.

| Piece | Logic |
|-------|-------|
| **Pawn (P/p)** | Forward push, double push from starting rank, diagonal captures only |
| **Knight (N/n)** | All 8 L-shaped jumps, ignores blocking pieces |
| **Bishop (B/b)** | Slides diagonally until blocked or captures |
| **Rook (R/r)** | Slides along ranks/files until blocked or captures |
| **Queen (Q/q)** | Combines bishop + rook sliding |
| **King (K/k)** | One step in any direction |

Helper functions:
- `is_friendly(p, r, c)` — checks if target square holds a same-color piece
- `slide(r, c, dr, dc, p)` — generic sliding logic used by bishop, rook, queen

### 🏰 Castling
- `castle_rights` dict — tracks 4 castling rights: white kingside (`K`), white queenside (`Q`), black kingside (`k`), black queenside (`q`)
- `valid_moves` appends castling destinations `(7,6)`, `(7,2)`, `(0,6)`, `(0,2)` to the king when:
  - King and rook have not yet moved
  - All squares between them are empty
- `do_castle()` — moves the rook to its correct square when king moves 2 squares
- `update_castle_rights()` — revokes rights the moment a king or rook first moves

---

## 📁 Project Structure

```
Chess/
├── main.py
├── README.md
└── pieces/
    ├── wP.png  wR.png  wN.png  wB.png  wQ.png  wK.png
    └── bP.png  bR.png  bN.png  bB.png  bQ.png  bK.png
```

---

## ▶️ How to Run

```bash
pip install pillow
python main.py
```

> Requires Python 3.x and piece images in a `pieces\` subfolder.

---

