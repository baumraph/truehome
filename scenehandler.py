class Scene():
    def __init__(self, name):
        self.name = name

    def run(self):
        pass


class SceneHanlder():
    def __init__(self):
        self.scenes = []
        self.current_scene = 0

    def add_scene(self, scene):
        self.scenes.append(scene)

    def toggle(self):
        if self.current_scene > 0:
            self.current_scene = 0
        else:
            self.current_scene = 1
        self.scenes[self.current_scene].run()

    def get_scene(self):
        return self.scenes[self.current_scene].name

    def set_scene(self, name):
        for i, scene in enumerate(self.scenes):
            if scene.name == name:
                scene.run()
                self.current_scene = i

    def next_scene(self):
        if self.current_scene < len(self.scenes) - 1:
            self.current_scene += 1
        else:
            self.current_scene = 1
        self.scenes[self.current_scene].run()

    def prev_scene(self):
        if self.current_scene > 2:
            self.current_scene -= 1
        else:
            self.current_scene = len(self.scenes) - 1
        self.scenes[self.current_scene].run()
