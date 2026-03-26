# Chess Game

A Python chess game implementation using Pygame with piece movement logic, move validation, and blocking detection.

## To-Do List

- [ ] Finish complete move history
- [x] Finish Queen movement logic
- [x] Finish Knight movement logic
- [x] Implement Capture Hint 
- [ ] Images over square position shift fix
- [x] King capture posibility
- [x] Implement removing duplicates in all ChessPiece types get_moves()
- [x] Bong cloud pos have no left move next to the pawn | King
  - It was because of attack_moves which give all illegal/default moves,
    better option is ofcourse get_possible_moves but the program was crashing
    because of recursion, later I found out that recursion was happening because the King was checking himself.
    BUT, the problem proceeds with behaviors of king towards one another,
    I fixed with still keeping attack_moves, but now the default function returns
    the get_possible_moves, and Pawn, and King have their own logic,
    which so far works for King class 

## Future Improvements

- [ ] Checkmate detection
- [ ] Game state saving/loading
- [ ] Move history
- [ ] !!! AI opponent
- [ ] Piece promotion (Pawn to Queen, etc.)
- [ ] En passant capture
- [x] Castling
- [ ] Turn management and turn indicator
- [ ] Capture display

## Project Structure

```
Chess/
├── main.py                # Entry point of the application
├── board.py               # Board class and game logic
├── game.py                # Game state and management
├── Pieces/                # Package containing all chess piece classes
│   ├── __init__.py        # Package initialization
│   ├── ChessPiece.py      # Base class for all pieces
│   ├── King.py            # King piece implementation
│   ├── Queen.py           # Queen piece implementation
│   ├── Rook.py            # Rook piece implementation
│   ├── Bishop.py          # Bishop piece implementation
│   ├── Knight.py          # Knight piece implementation
│   └── Pawn.py            # Pawn piece implementation
├── Materials/             # Game assets
│   ├── Pieces/            # Piece images (wk.png, bk.png, etc.)
│   ├── board.png          # Chessboard image
│   └── hint.png           # Move hint indicator
└── README.md              # This file
```

## Features

- **Complete Piece Movement**: All chess pieces (King, Queen, Rook, Bishop, Knight, Pawn) with correct movement patterns
- **Move Validation**: 
  - Detects blocking pieces (can't move through friendly pieces)
  - Allows capturing enemy pieces
  - Pawn-specific rules (forward movement, diagonal captures)
  - King check detection
- **Visual Feedback**: Hints show available moves when a piece is selected
- **Resizable Window**: Board automatically resizes to maintain a square aspect ratio
- **Piece Selection**: Click pieces to see available moves

## How to Run

1. Ensure you have Python 3.x installed
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Game Controls

- **Click a piece** to select it and view available moves (shown as hints)
- **Click an available move** to move the piece
- **Click elsewhere** to deselect

## Piece Rules

### Pawn
- Moves forward 1 square (or 2 squares on first move)
- Captures diagonally forward
- Cannot move forward if blocked

### Rook
- Moves horizontally or vertically
- Cannot move through other pieces
- Can capture at the end of its path

### Bishop
- Moves diagonally
- Cannot move through other pieces
- Can capture at the end of its path

### Queen
- Combines Rook and Bishop movement
- Moves horizontally, vertically, or diagonally
- Cannot move through other pieces
- Can capture at the end of its path

### Knight
- Moves in an L-shape: 2 squares in one direction and 1 square perpendicular (or vice versa)
- Can jump over other pieces (not blocked by pieces in the way)
- Can capture enemy pieces at its destination

### King
- Moves one square in any direction
- Cannot move to squares under attack by enemy pieces

## Technical Details

- **Language**: Python 3
- **Graphics**: Pygame
- **Architecture**: Object-oriented design with inheritance
- **Move Blocking Logic**: Distance-based calculation to detect blocking pieces
- **Attack Detection**: Pieces calculate attack moves for check detection

## Notes

- The board coordinate system uses (x, y) where x is column (0-7) and y is row (0-7)
- Moves are validated against the current board state
- Blocking logic uses squared distances to determine which pieces block paths