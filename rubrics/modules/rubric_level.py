class RubricLevel(object):
    def __init__(self, levels_data):
        self.l1 = str(levels_data[0]).strip().split('.')[1].strip()
        self.l2 = str(levels_data[1]).strip()
        self.l3 = str(levels_data[2]).strip()
        self.l4 = str(levels_data[3]).strip()
        self.level_name = None
        self.max_marks = 0
        self.get_level()

    def get_level(self):
        if self.l1 and self.l2 and self.l3:
            self.level_name = 3
            self.max_marks = int(self.l4)
        elif self.l1 and self.l2 and not self.l3:
            self.level_name = 2
        elif self.l1 and not self.l2 and not self.l3:
            self.level_name = 1
