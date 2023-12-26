import random as rand

CELL_UNKNOWN = 0
CELL_EMPTY = 1
CELL_SHIP = 2

ORIENTATION_UNKNOWN = 0
ORIENTATION_HORIZONTAL = 1
ORIENTATION_VERTICAL = 2

class Cell:
    _value: int
    orientation: int

    def __init__(self, value):
        self.value = value
        self.orientation = ORIENTATION_UNKNOWN
    
    def __str__(self):
        return "(" + str(self.value) + "," + str(self.orientation) + ")"

class BattleshipBot:
    len_x: int
    len_y: int
    board: list[list[int]]
    num_ships: int
    num_ships_found: int
    
    def __init__(self, len_x, len_y, num_ships):
        self.len_x = len_x
        self.len_y = len_y
        self.num_ships = num_ships
        self.num_ships_found = 0
        self.board = []
        
        # initialize a board of proper size with all cells being unknown
        for j in range(len_y):
            row = []
            for i in range(len_x):
                row.append(Cell(CELL_UNKNOWN))
            self.board.append(row)
    
    def __str__(self):
        s = ""

        for row in range(self.len_y):
            for col in range(self.len_x):
                s = s + " " + str(self.board[row][col])
            s = s + "\n"

        return s

    # when a ship is hit, we update which orientation we think it lays in 
    def update_orientations(self, x, y):
        # update orientation of this cell and cells near that have a hit based on nearby cells with hits
        # eg. if we previously detected a hit to the right, then we set this cell and the cell to the right's orientation to horizontal.
        # if we previously detected a hit downwards, then we set this cell and the cell to the right's orientation to vertical.
        if x-1 > 0 and self.board[y][x-1].value == CELL_SHIP:
            self.board[y][x].orientation = ORIENTATION_HORIZONTAL
            self.board[y][x-1].orientation = ORIENTATION_HORIZONTAL
        elif x+1 < self.len_x and self.board[y][x+1].value == CELL_SHIP:
            self.board[y][x].orientation = ORIENTATION_HORIZONTAL
            self.board[y][x+1].orientation = ORIENTATION_HORIZONTAL
        elif y-1 > 0 and self.board[y-1][x].value == CELL_SHIP:
            self.board[y][x].orientation = ORIENTATION_VERTICAL
            self.board[y-1][x].orientation = ORIENTATION_VERTICAL
        elif y+1 < self.len_y and self.board[y+1][x].value == CELL_SHIP:
            self.board[y][x].orientation = ORIENTATION_VERTICAL
            self.board[y+1][x].orientation = ORIENTATION_VERTICAL


    def update_board(self, x, y, val):
        self.board[y][x].value = val

        if val == CELL_SHIP:
            self.update_orientations(x, y)
            self.num_ships_found += 1

    # returns a cell that it wants to shoot
    def take_turn(self):
        if self.num_ships == self.num_ships_found:
            print("found all ships")
            return None

        # choose which action to take based on current state of the board
        if not self.search(CELL_SHIP):
            # probe if we have no information
            #print("probe")
            shot = self.probe()
            if not shot:
                print("board fully cleared.")
            return shot
        else:
            #print("focus")
            shot =  self.focus_ship()
            if not shot:
                print("board fully cleared.")
            return shot
    
    def probe(self):
        # pick a random row that can still be shot in
        valid_rows_i = self.get_shootable_row_indices()
        if not valid_rows_i:
            return None
        row_i = rand.choice(valid_rows_i)

        # shoot a random cell in the row that can still be shot
        valid_cols_i = self.get_shootable_in_row(row_i)
        col_i = rand.choice(valid_cols_i)

        return (col_i, row_i) # return in (x,y) format
    
    def focus_ship(self):
        ship_cells = self.search_all(CELL_SHIP)
        for cell in ship_cells:
            ship_x, ship_y = cell
            
            desired_shots = []
            if self.board[ship_y][ship_x].orientation == ORIENTATION_HORIZONTAL:
                desired_shots.append((ship_x-1, ship_y))
                desired_shots.append((ship_x+1, ship_y))
            elif self.board[ship_y][ship_x].orientation == ORIENTATION_VERTICAL:
                desired_shots.append((ship_x, ship_y-1))
                desired_shots.append((ship_x, ship_y+1))
            else:
                # unknown orientation, so it doesnt matter which way we shoot
                desired_shots.append((ship_x-1, ship_y))
                desired_shots.append((ship_x+1, ship_y))
                desired_shots.append((ship_x, ship_y-1))
                desired_shots.append((ship_x, ship_y+1))
            # remove shots that go out of bounds
            desired_shots = [shot for shot in desired_shots if (shot[0] > 0 and shot[1] > 0) and (shot[0] < self.len_x and shot[1] < self.len_y)]

            for shot in desired_shots:
                x, y = shot
                
                if self.board[y][x].value == CELL_UNKNOWN:
                    return (x, y)
        return self.probe() # fallback to random shooting if all adjacent cells are already known for every single ship

    # check if value exists in board
    def search(self, val: int):
        for row in range(self.len_y):
            for col in range(self.len_x):
                if self.board[row][col].value == val:
                    return (col, row) # return in (x,y) format
        return None

    def search_all(self, val: int):
        cells = []
        for row in range(self.len_y):
            for col in range(self.len_x):
                if self.board[row][col].value == val:
                    cells.append((col, row))
        return cells

    # get all rows with cells still available to shoot
    def get_shootable_row_indices(self):
        valid_rows_i = []

        for row_i in range(self.len_y):
            for col_i in range(self.len_x):
                if self.board[row_i][col_i].value == CELL_UNKNOWN:
                    valid_rows_i.append(row_i)

        return valid_rows_i

    def get_shootable_in_row(self, row_i):
        valid_cells = []

        for col_i in range(self.len_x):
            if self.board[row_i][col_i].value == CELL_UNKNOWN:
                valid_cells.append(col_i)
        
        return valid_cells


def main():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]]

    num_ship_cells = sum(x.count(1) for x in board)
    bot = BattleshipBot(10, 10, num_ship_cells)
    rand.seed(50)
    
    for i in range(1000):
        shot = bot.take_turn()
        if not shot:
            break

        x, y = shot
        if board[y][x] == 1:
            bot.update_board(x, y, CELL_SHIP)
        elif board[y][x] == 0:
            bot.update_board(x, y, CELL_EMPTY)
        print(bot)
    print("game over")

if __name__ == "__main__":
    main()