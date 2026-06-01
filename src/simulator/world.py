from robot import Robot


class World:
    def init(self):
        self.robot = Robot()
        self.objects = [self.robot]

    def update(self):
        self.robot.update()

    def get_objects(self):
        return self.objects
