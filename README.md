Algorithm that makes moves in [Battleship](https://en.wikipedia.org/wiki/Battleship_(game))

Employs a strategy of attacking random squares for hits, then once a hit is made, it will try to follow the ship along the vertical or horizontal axis based on previous hit information in cardianally adjacent cells. eg. if a cell and the cell directly above it are both hit, then the AI knows the ship lies vertically.

- does not have any knowledge of possible ship lengths or sunk ships
