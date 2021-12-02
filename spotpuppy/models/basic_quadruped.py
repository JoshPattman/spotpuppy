from . import quadruped_base

class quadruped(quadruped_base.quadruped):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _on_update(self):
        self.quad_controller.set_all_legs(self.calculate_still_positions())

