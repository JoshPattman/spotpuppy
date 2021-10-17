from . import quadruped_base

class quadruped(quadruped_base.quadruped):
    def __init__(self, rotation_sensor=None, servo_controller=None, bone_length=6, body_dims=[10, 10], fall_rotation_limit=0):
        quadruped_base.quadruped.__init__(self, rotation_sensor=rotation_sensor,servo_controller=servo_controller,bone_length=bone_length,body_dims=body_dims,fall_rotation_limit=fall_rotation_limit)

    def _on_update(self):
        # Set all legs to default height, and tell the underlying quadruped to keep the legs grounded in global space
        posses = self._calculate_still_positions()
        self.quad_controller.body_rotation = self.current_rotation
        for l in range(4):
            self.quad_controller.set_leg(l, posses[l])


if __name__ == "__main__":
    q = quadruped()
    q.update()