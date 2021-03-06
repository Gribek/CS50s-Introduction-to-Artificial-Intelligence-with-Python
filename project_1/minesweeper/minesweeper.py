import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells if len(self.cells) == self.count else set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells if self.count == 0 else set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)

        # Add a new sentence to the AI's knowledge base
        self.new_sentence(cell, count)

        # Search for new inferences that can be draw from
        # the current AI's knowledge base
        while True:

            # Set flag as false, knowledge base not changed
            knowledge_changed = False

            # Keep looking for additional safe cells or mines
            while True:
                new_mines_found = self.safe_fields_and_mines_check()

                # Break if no mines have been found
                if not new_mines_found:
                    break

            # Add new sentence to knowledge base if possible
            # Iterate through current AI's knowledge base
            current_knowledge = self.knowledge[:]
            for sentence in current_knowledge:
                if not sentence.cells:  # Skip if empty set
                    continue
                for other_sentence in current_knowledge:

                    # Check if subset
                    if sentence.cells < other_sentence.cells:

                        # Calculate difference between sets
                        new_cells = other_sentence.cells - sentence.cells

                        # Check if set is not already in knowledge base
                        if new_cells in (s.cells for s in self.knowledge):
                            continue

                        # Create new Sentence and add it to knowledge base
                        new_count = other_sentence.count - sentence.count
                        self.knowledge.append(Sentence(new_cells, new_count))

                        # Set flag as true
                        knowledge_changed = True

            # Break if knowledge base has not been changed
            if not knowledge_changed:
                break

    def new_sentence(self, cell, count):
        """
        Add a new sentence to the AI's knowledge base.
        """
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if i < 0 or j < 0 or i >= self.height or j >= self.width:
                    continue
                if (i, j) == cell:
                    continue
                if (i, j) in self.safes:
                    continue
                if (i, j) in self.mines:
                    count -= 1
                    continue
                cells.add((i, j))
        self.knowledge.append(Sentence(cells, count))

    def safe_fields_and_mines_check(self):
        """
        Mark any additional cells as safe or as mines if it can be
        concluded based on the AI's knowledge base. Return true if
        new mines have been found, else false.
        """
        # Initially set new_data flag as false
        new_data = False

        # Look for safe cells
        for sentence in self.knowledge:
            for safe_cell in sentence.known_safes().copy():
                self.mark_safe(safe_cell)

        # Look for mine cells
        for sentence in self.knowledge:
            new_mines = sentence.known_mines().copy()
            if new_mines:
                new_data = True
            for mine_cell in new_mines:
                self.mark_mine(mine_cell)

        return new_data

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Get set of available moves
        save_moves = self.safes - self.moves_made

        # Return arbitrary safe move if the one exist else None
        return save_moves.pop() if save_moves else None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Get a list of all cells in the game
        possible_moves = [(i, j) for i in range(0, self.height) for j in
                          range(0, self.width)]

        # Create a set of moves without those already made and mines
        available_moves = set(possible_moves) - self.moves_made - self.mines

        # Return arbitrary move if the one exist else None
        return available_moves.pop() if available_moves else None
