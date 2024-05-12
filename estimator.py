import ioutils


class Estimator:

    def __init__(self):
        # {additional percent for forge: [success number, total number]}
        self.data = ioutils.load_data()
        if (not len(self.data)):
            self.data = [[{0: [0, 0], 10: [0, 0], 15: [0, 0]} for _ in range(9)]
                         for _ in range(120)]
        self.estimated = [[None for _ in range(9)] for _ in range(120)]
        self.__estimate_all()

    def estimate(self, level, stage):
        cell = self.data[level][stage]
        cell_0 = cell[0]
        cell_10 = cell[10]
        cell_15 = cell[15]
        if cell_0[1] + cell_10[1] + cell_15[1] == 0:
            return None

        self.estimated[level][stage] = \
            (cell_0[0] + max(0, cell_10[0] - 0.1 * cell_10[1]) + max(0, cell_15[0] - 0.15 * cell_15[1])) \
            / (cell_0[1] + cell_10[1] + cell_15[1])

    def update(self, level, stage, percentage, success):
        cell = self.data[level][stage][percentage]
        if success:
            cell[0] += 1
        cell[1] += 1
        self.estimate(level, stage)
        ioutils.save_data(self.data)

    def __estimate_all(self):
        for level in range(len(self.data)):
            for stage in range(len(self.data[level])):
                self.estimate(level, stage)
