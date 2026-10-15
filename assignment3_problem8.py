"""Assignment 3, Problem 8 — 3D Squares puzzle: Python STARTER CODE.

This is an optional scaffold, not a completed solver.
Students implement successors(), uninformed_search(), heuristic(), and
informed_search(), plus the experiment in main().

Assumptions :
* 3 x 3 board containing nine square pieces, placed row by row.
* Each piece may rotate clockwise by 0, 90, 180, or 270 degrees; no flips.
* Each piece has four directed half-images ordered (N, E, S, W).
* Paired half-image IDs are (0, 1), (2, 3), (4, 5), (6, 7).
* Only internal touching edges must complement; border edges are unrestricted.

The photographed pieces have NOT been reliably transcribed. Supply verified
piece data below. Other languages and different valid formulations are allowed.
"""

from collections import deque  # Available for BFS; students may choose other methods.
import heapq                    # Available for priority-queue search.
import time
import tracemalloc

SIZE = 3
NUM_CELLS = SIZE * SIZE

# REPLACE with nine verified four-edge tuples in (N, E, S, W) order.
# Each edge must be an integer in 0..7. Example FORMAT ONLY (not puzzle data):
# PIECES = [(0, 2, 4, 6), ... nine tuples total ...]
PIECES = []


def validate_pieces(pieces):
    """Fail early if the symbolic input is incomplete or malformed."""
    if len(pieces) != NUM_CELLS:
        raise ValueError(f"Expected {NUM_CELLS} pieces; received {len(pieces)}. "
                         "Transcribe and verify the puzzle first.")
    for i, piece in enumerate(pieces):
        if len(piece) != 4 or any(type(edge) is not int or edge not in range(8)
                                  for edge in piece):
            raise ValueError(f"Piece {i} must be four integer edge IDs (0..7).")


def complements(a, b):
    """Check complementarity under the agreed encoding (0,1), (2,3), etc."""
    return (a ^ 1) == b


def rotate(piece, quarter_turns=0):
    """Return (N, E, S, W) after clockwise quarter turns."""
    r = quarter_turns % 4
    return piece[-r:] + piece[:-r] if r else piece


def oriented_piece(piece_id, rotation):
    """Return the four oriented edges of a placed piece."""
    return rotate(PIECES[piece_id], rotation)


def initial_state():
    """State = (board, unused); board entries are None or (piece_id, rotation).

    Tuples and frozensets make states immutable and suitable for visited sets.
    """
    validate_pieces(PIECES)
    board = (None,) * NUM_CELLS
    unused = frozenset(range(NUM_CELLS))
    return (board, unused)


def legal(board, cell, oriented_edges):
    """Check matches against the already-placed north and west neighbors.

    Valid when students place pieces row-major, starting at the upper left.
    Returns True for the first cell because it has no placed neighbors.
    """
    if not (0 <= cell < NUM_CELLS) or board[cell] is not None:
        return False
    row, col = divmod(cell, SIZE)

    if col > 0 and board[cell - 1] is not None:
        left_id, left_rotation = board[cell - 1]
        left_edges = oriented_piece(left_id, left_rotation)
        if not complements(left_edges[1], oriented_edges[3]):
            return False

    if row > 0 and board[cell - SIZE] is not None:
        top_id, top_rotation = board[cell - SIZE]
        top_edges = oriented_piece(top_id, top_rotation)
        if not complements(top_edges[2], oriented_edges[0]):
            return False

    return True


def verify(board):
    """Independently verify a completed arrangement and every internal edge."""
    if len(board) != NUM_CELLS or any(slot is None for slot in board):
        return False
    try:
        ids = [piece_id for piece_id, rotation in board]
        if set(ids) != set(range(NUM_CELLS)) or len(set(ids)) != NUM_CELLS:
            return False
        for cell, (piece_id, rotation) in enumerate(board):
            edges = oriented_piece(piece_id, rotation)
            row, col = divmod(cell, SIZE)
            if col + 1 < SIZE:
                right_id, right_rotation = board[cell + 1]
                right_edges = oriented_piece(right_id, right_rotation)
                if not complements(edges[1], right_edges[3]):
                    return False
            if row + 1 < SIZE:
                bottom_id, bottom_rotation = board[cell + SIZE]
                bottom_edges = oriented_piece(bottom_id, bottom_rotation)
                if not complements(edges[2], bottom_edges[0]):
                    return False
    except (IndexError, KeyError, TypeError, ValueError):
        return False
    return True


def goal(state):
    """A valid completed board, with no unused pieces."""
    board, unused = state
    return not unused and verify(board)


def next_empty_cell(state):
    """Return the first empty index, or None when the board is full."""
    board, unused = state
    return next((i for i, slot in enumerate(board) if slot is None), None)


def place(state, cell, piece_id, rotation):
    """Construct a new immutable state after a verified legal placement.

    Raises ValueError on invalid placement; students still write the
    iteration over candidate pieces/rotations in successors().
    """
    board, unused = state
    if piece_id not in unused or not legal(board, cell, oriented_piece(piece_id, rotation)):
        raise ValueError("Piece is used or does not fit at the given cell")
    updated = list(board)
    updated[cell] = (piece_id, rotation % 4)
    return (tuple(updated), unused - {piece_id})


def path_cost(state):
    """Number of placed pieces, assuming unit cost per placement."""
    return NUM_CELLS - len(state[1])


def successors(state):
    """STUDENT TODO: Return an iterable of successor states.

    Outline (incremental, row-major formulation):
      1. Find the first empty cell (or use next_empty_cell(state)).
      2. For each unused piece_id, try rotations 0, 1, 2, 3.
      3. Call oriented_piece(piece_id, rotation), then legal(board, cell, edges).
      4. For legal placements, call place(state, cell, piece_id, rotation).
      5. Yield or return the new states.

    Do not mutate the original state. Duplicate rotated orientations may be
    omitted as an optional optimization.
    """
    raise NotImplementedError("Students implement successor generation")


def uninformed_search(start):
    """STUDENT TODO: Implement BFS, DFS, or another uninformed search.

    Decide the frontier discipline (queue vs stack), expand successors,
    detect the goal, and consider repeated-state handling.
    Return a goal state, or None if no solution is found.
    """
    raise NotImplementedError("Students implement uninformed search")


def heuristic(state):
    """STUDENT TODO: Design, implement, and justify a heuristic.

    A possible direction is forward checking: can any legal candidate fill
    the next empty cell? Explain whether the heuristic is admissible if
    used with A*, and discuss whether it differentiates states at equal depth.
    """
    raise NotImplementedError("Students design their heuristic")


def informed_search(start, h):
    """STUDENT TODO: Implement A* or Greedy Best-First Search.

    Greedy priority = h(state).
    A* priority = g(state) + h(state), where each placement costs 1.
    Use heapq or another priority-queue implementation. IMPORTANT: do not
    push (priority, state) into heapq. Equal priorities can make Python
    compare states containing None and tuples, which raises TypeError.
    Use an insertion counter to make heap entries unambiguously sortable:

        from itertools import count
        tie_breaker = count()
        # heapq.heappush(frontier, (priority, next(tie_breaker), state))
        # priority, _, state = heapq.heappop(frontier)

    Explain your repeated-state handling as well.
    Return a goal state, or None if no solution is found.
    """
    raise NotImplementedError("Students implement informed search")


def measure(search_fn, *args):
    """Measure elapsed wall time and peak Python-traced allocations.

    Note: tracemalloc is NOT total process RSS. For a fair comparison, use
    the same machine, input, and reporting conventions for each approach.
    """
    tracemalloc.start()
    try:
        start_time = time.perf_counter()
        result = search_fn(*args)
        seconds = time.perf_counter() - start_time
        _, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return result, seconds, peak_bytes / (1024 * 1024)


def display_board(board):
    """Display (piece ID, clockwise rotation in degrees) for each cell."""
    for row in range(SIZE):
        cells = board[row * SIZE:(row + 1) * SIZE]
        print(" | ".join("empty" if item is None else
                         f"P{item[0]} @ {90 * item[1]}°" for item in cells))


if __name__ == "__main__":
    if not PIECES:
        print("Enter and verify all nine piece tuples in PIECES before running.")
    else:
        start = initial_state()
        # STUDENT TODO: Run both search approaches with measure(...).
        # STUDENT TODO: Check goal(result) and print results using display_board.
        # STUDENT TODO: Compare runtime and peak traced memory in the report.
