# 1) まず最初に SimulationApp（他の omni/isaacsim import より前）
from isaacsim.simulation_app import SimulationApp
simulation_app = SimulationApp({"headless": False})

# 2) ここから isaacsim を import
import numpy as np
from isaacsim.core.api.world import World
from isaacsim.core.prims import Articulation
from isaacsim.core.utils.stage import add_reference_to_stage
from isaacsim.core.utils.nucleus import get_assets_root_path
from isaacsim.core.utils.types import ArticulationAction

def main():
    world = World()
    assets_root = get_assets_root_path()

    # 例：Franka を1体ロード（USD パスは環境で違うことがあるので適宜）
    franka_prim = "/World/Franka_00"
    add_reference_to_stage(
        assets_root + "/Isaac/Robots/Franka/franka_alt_fingers.usd",
        franka_prim
    )

    robot = Articulation(prim_path=franka_prim, name="franka_00")
    world.scene.add(robot)

    world.reset()

    # ★ここがポイント：controller は Articulation から取る（引数で作らない）
    ctrl = robot.get_articulation_controller()

    # 例：関節 position を適当に送る（DOF数は robot に合わせる）
    dof = robot.num_dof
    q = np.zeros(dof)

    for _ in range(300):
        world.step(render=True)

        # 位置指令
        action = ArticulationAction(joint_positions=q)
        ctrl.apply_action(action)

    simulation_app.close()

if __name__ == "__main__":
    main()
