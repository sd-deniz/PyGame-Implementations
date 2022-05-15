import pygame as pg
from colors import Color
from enum import Enum


DISPLAY_WIDTH = 800
BOTTOM_AREA_LENGTH = 120

DISPLAY_HEIGHT = DISPLAY_WIDTH + BOTTOM_AREA_LENGTH
DISPLAY_DIMENSIONS = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

# thickness has to be an even number
GRID_LINE_THICKNESS = 2

K = 2
TILE_SIZE = 10 * K


class TileStatus(Enum):
    EMPTY = 0
    WALL = 1
    STARTING_TILE = 2
    DESTINATION_TILE = 3


class InvalidPositionValue(Exception):
    """Value should be greater than zero."""


class InvalidTileSize(Exception):
    """Value should be greater than zero."""


class InvalidGridLineThickness(Exception):
    """Grid line thickness has to be an even number"""


class Grid:
    def __init__(self, row, column):
        if row <= 0:
            raise InvalidPositionValue(f"Invalid row value {row=}")
        if column <= 0:
            raise InvalidPositionValue(f"Invalid column value: {column=}")

        self.r = row
        self.c = column
        self.grid = None

        # initialize the grid
        self.create_grid()

    def create_grid(self):
        self.grid = [[0 for _ in range(self.c)] for i in range(self.r)]

    def reset_grid(self):
        """Inplace reset. It doesn't create a brand new array"""
        for r in range(self.r):
            for c in range(self.c):
                self.grid[r][c] = 0

    def set_tile_status(self, row, column, tile_status: Enum):
        """
        tile_status: TileStatus Enum

        """
        self.grid[row][column] = tile_status

    def get_tile_status(self, row, column) -> int:
        return self.grid[row][column]


class GridVisual:
    def __init__(self, screen, tile_size: TILE_SIZE):
        """tile shape is square"""
        if tile_size <= 0:
            raise InvalidTileSize(f"Invalid tile_size value {tile_size=}")

        self.screen = screen
        self.tile_size = tile_size

        # outer frame thickness is 1*tile_size
        w, h = screen.get_size()
        self.grid_width = w
        self.grid_height = self.grid_width

        self.row = self.grid_width // self.tile_size
        self.column = self.grid_height // self.tile_size
        self.line_thickness = GRID_LINE_THICKNESS
        # hv: half thickness
        self.hv = self.line_thickness // 2

        # grid list
        self.grid = Grid(self.row, self.column)
        self.start_point: tuple = None
        self.destination_point: tuple = None

    def initialize_grid_background(self):
        # draw an empty white rectangle. The base of the grid.
        pg.draw.rect(self.screen, Color.WHITE, (0,0,self.grid_width,self.grid_height))

        # draw vertical lines
        # line thickness has to be an even number.
        # halves of a vertical line will be in the neigbooring tiles.
        if self.line_thickness%2 != 0:
            raise InvalidGridLineThickness("grid line thickness is an odd number.")

        for pos in range(self.tile_size, self.grid_width, self.tile_size):
            # vertical lines
            pg.draw.lines(self.screen, Color.GREY, closed=False,
                          points=((pos, 0), (pos, self.grid_height-self.hv)), width=self.line_thickness)

            # horizontal lines
            pg.draw.lines(self.screen, Color.GREY, closed=False,
                          points=((0, pos), (self.grid_width-self.hv, pos)), width=self.line_thickness)

    def init_grid(self):
        self.grid.reset_grid()
        self.initialize_grid_background()

    def update_tile_visual(self, row: int, column:int, color: Color):
        x, y = (row*self.tile_size+self.hv+1, column*self.tile_size+self.hv+1)
        width = self.tile_size - self.hv - 1
        pg.draw.rect(self.screen, color, (x,y,width,width))

    def update_tile(self, row: int, column: int, tile_status: Enum):
        """Updates grid list and grid visual"""
        color_map = {
            TileStatus.WALL: Color.BLACK,
            TileStatus.EMPTY: Color.WHITE,
            TileStatus.STARTING_TILE: Color.GREEN,
            TileStatus.DESTINATION_TILE: Color.BLUE
        }

        # update Grid.grid tile
        self.grid.set_tile_status(row, column, tile_status)

        # update tile visual
        self.update_tile_visual(row, column, color=color_map[tile_status])

    def update_start_tile(self, row: int, column: int):
        if self.start_point:
            # reset previous starting point
            self.update_tile(*self.start_point, tile_status=TileStatus.EMPTY)

        self.update_tile(row, column, tile_status=TileStatus.STARTING_TILE)
        self.start_point = row, column

    def update_destination_tile(self, row: int, column: int):
        if self.destination_point:
            # reset previous destionation point
            self.update_tile(*self.destination_point, tile_status=TileStatus.EMPTY)

        self.update_tile(row, column, tile_status=TileStatus.DESTINATION_TILE)
        self.destination_point = row, column


class ControlPane:
    def __init__(self, screen):
        self.screen = screen
        self.gap = TILE_SIZE * 1
        self.height = DISPLAY_WIDTH


    def draw_texts(self, screen):
        font = pg.font.SysFont("arial", 20)

        text_pos_1 = (0, self.height + 0*self.gap)
        text_pos_2 = (0, self.height + 1*self.gap)
        text_pos_3 = (0, self.height + 2*self.gap)
        text_pos_4 = (0, self.height + 3*self.gap)
        text_pos_5 = (0, self.height + 4*self.gap)

        t1_text = "How to use it ?"
        t2_text = "Hit  's'  to place a starting tile. Hit  'd'  to place a destination tile."
        t3_text = "Hit  'w'  to place a wall tile. Walls can be drawn by holding down the mouse button."
        t4_text = "Click  'left mouse button'  to delete a tile."
        t5_text = "Hit  'o'  to run the simulation. Hit  'r'  to restart."

        render_obj_ = font.render(t1_text, True, Color.WHITE)
        self.screen.blit(render_obj_, text_pos_1)

        render_obj_ = font.render(t2_text, True, Color.WHITE)
        self.screen.blit(render_obj_, text_pos_2)

        render_obj_ = font.render(t3_text, True, Color.WHITE)
        self.screen.blit(render_obj_, text_pos_3)

        render_obj_ = font.render(t4_text, True, Color.WHITE)
        self.screen.blit(render_obj_, text_pos_4)

        render_obj_ = font.render(t5_text, True, Color.WHITE)
        self.screen.blit(render_obj_, text_pos_5)

    def draw_background(self, screen):
        pg.draw.rect(screen, Color.BLACK, (0, DISPLAY_WIDTH, DISPLAY_WIDTH, BOTTOM_AREA_LENGTH))

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_texts(screen)


def bfs(grid_visual: GridVisual, parents: dict):
    start = grid_visual.start_point
    destination_point = grid_visual.destination_point
    grid = grid_visual.grid.grid

    if start is None:
        print("Start point is required")

    if destination_point is None:
        print("Destination point is required")

    m, n = len(grid), len(grid[0])
    visited = set()
    visited.add(start)
    parents[start] = None
    frontier = [start]

    while frontier:
        new_frontier = []
        for row,col in frontier:
            for r,c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
                if (r,c) not in visited and 0<=r<m and 0<=c<n:

                    val = grid[r][c]

                    if val == TileStatus.WALL:
                        visited.add((r,c))
                        continue

                    parents[(r,c)] = (row,col)
                    new_frontier.append((r,c))
                    visited.add((r,c))

                    if val == TileStatus.DESTINATION_TILE:
                        parents["did_find"] = True
                        return
                    yield r,c

        frontier = new_frontier
    return


def backward_track(gv: GridVisual, parents: dict):
    start = gv.start_point
    end = gv.destination_point
    shortest_path = [end]
    while start != parents[end]:
        try:
            parent_tile = parents[end]
        except KeyError:
            print(f"No path")
            return
        else:
            shortest_path.append(parent_tile)
            yield parent_tile
            end = parent_tile
    return


def dye_tile(gv, row, column, color):
    gv.update_tile_visual(row, column, color)
    pg.display.update()


def calculate_tile_index_from_pixels(x, y):
    return x//TILE_SIZE, y//TILE_SIZE


def run_sim(gv: GridVisual):
    print("simulation is running...")

    parents = {"did_find": False}

    for r, c in bfs(gv, parents):
        dye_tile(gv, r, c, Color.SOFT_PINK)

    if parents["did_find"]:
        for r, c in backward_track(gv, parents):
            dye_tile(gv, r, c, Color.ORANGE)

    return parents


def main():
    # Initialize: pygame
    pg.init()

    # Set: display&window dimensions
    # pg.SCALED scales if window is smaller than the display dimensions
    screen = pg.display.set_mode(DISPLAY_DIMENSIONS, pg.SCALED)
    pg.display.set_caption("Path Finder")

    # default is also True
    pg.mouse.set_visible(True)

    # Set: background, to update the visuals
    '''
        "With no additional arguments
        "the Surface will be created in a format"
        "that best matches the display Surface."
    '''
    background = pg.Surface(screen.get_size())

    # The convert with no arguments will make sure our
    # background is the same format as the display window,
    # which will give us the fastest results.
    background = background.convert()

    # Set: clock
    clock = pg.time.Clock()

    # Initialize: UI
    gv = GridVisual(screen, TILE_SIZE)
    gv.init_grid()
    tile_status = TileStatus.WALL
    cp = ControlPane(screen)
    cp.draw(screen)

    # Run the Game
    game_running = True
    while game_running:

        for event in pg.event.get():

            buttons = pg.mouse.get_pressed()
            if any(buttons):
                # pos: (tuple) -> (x,y)
                x, y = pg.mouse.get_pos()

                # buttons: (list[bool]) -> [0](left) or [1](wheel) or [2](right)
                if x<DISPLAY_WIDTH and y<DISPLAY_WIDTH:
                    # grid area

                    # conditions don't handle situations where more than one buttons are clicked at the same time.
                    if buttons[0]:
                        if tile_status==TileStatus.WALL or tile_status==TileStatus.EMPTY:
                            # change tile status
                            gv.update_tile(*calculate_tile_index_from_pixels(x, y), tile_status)
                        elif tile_status == TileStatus.STARTING_TILE:
                            # change starting tile
                            gv.update_start_tile(*calculate_tile_index_from_pixels(x,y))
                        elif tile_status == TileStatus.DESTINATION_TILE:
                            # change destination tile
                            gv.update_destination_tile(*calculate_tile_index_from_pixels(x,y))
                        else:
                            # do nothing
                            pass

                    elif buttons[2]:
                        # reset tile status
                        gv.update_tile(*calculate_tile_index_from_pixels(x, y), TileStatus.EMPTY)

                    else:
                        # do nothing
                        pass

            elif event.type == pg.KEYDOWN:
                # Tile type
                if event.key == pg.K_s:
                    tile_status = TileStatus.STARTING_TILE
                elif event.key == pg.K_d:
                    tile_status = TileStatus.DESTINATION_TILE
                elif event.key == pg.K_w:
                    tile_status = TileStatus.WALL
                elif event.key == pg.K_r:
                    gv.init_grid()
                elif event.key == pg.K_o:
                    _ = run_sim(gv)
                else:
                    # do nothing
                    pass

            elif event.type == pg.QUIT:
                # if the user clicks the close window button
                game_running = False

            else:
                # do nothing
                pass

        # Update: display
        pg.display.update()
        clock.tick(30)
    # Quit: pg
    pg.quit()


if __name__ == '__main__':
    main()
