import unittest
import game


class TestGrid(unittest.TestCase):

    def setUp(self):
        self.r = 2
        self.c = 3
        self.g = game.Grid(self.r, self.c)

    def test_grid_initialization(self):
        self.g = game.Grid(2, 3)
        # check grid
        dummy_grid = [[0 for _ in range(self.c)] for i in range(self.r)]
        msg = "grid initialization result is unexpected"
        self.assertEqual(self.g.grid, dummy_grid, msg)

    def test_set_tile_status(self):
        # target tile and its status
        val = 3
        r, c = 1, 2

        # check set_tile_status
        self.g.set_tile_status(r, c, val)
        res = self.g.grid[r][c]
        msg = f"set_tile_status result is unexpected: {res=}"
        self.assertEqual(res, val, msg)

    def test_get_tile_status(self):
        # target tile and its status
        val = 3
        r, c = 1, 2

        # set and then check get_tile_status
        self.g.set_tile_status(r, c, val)
        res = self.g.get_tile_status(r, c)
        msg = f"get_tile_status result is unexpected: {res=}"
        self.assertEqual(res, val, msg)

    def test_reset_grid(self):
        # check reset_grid
        self.g.reset_grid()
        dummy_grid = [[0 for _ in range(self.c)] for i in range(self.r)]
        msg = "reset_grid result is unexpected"
        self.assertEqual(self.g.grid, dummy_grid, msg)


if __name__ == '__main__':
    unittest.main()
