import os.path as osp
import random

import numpy as np
import pytest

import examples.settings
import habitat_sim


# return True if val_1 is within epsilon error of val_2
def within_eps_error(val_1, val_2):
    eps = 0.0000000001
    if abs(val_1 - val_2) < eps:
        return True
    return False


@pytest.mark.skipif(
    not osp.exists("data/scene_datasets/habitat-test-scenes/skokloster-castle.glb")
    or not osp.exists("data/objects/"),
    reason="Requires the habitat-test-scenes and habitat test objects",
)
def test_kinematics(sim):
    cfg_settings = examples.settings.default_sim_settings.copy()

    cfg_settings[
        "scene"
    ] = "data/scene_datasets/habitat-test-scenes/skokloster-castle.glb"
    # enable the physics simulator: also clears available actions to no-op
    cfg_settings["enable_physics"] = True
    cfg_settings["depth_sensor"] = True

    # test loading the physical scene
    hab_cfg = examples.settings.make_cfg(cfg_settings)
    sim.reconfigure(hab_cfg)
    assert sim.get_physics_object_library_size() > 0

    # test adding an object to the world
    object_id = sim.add_object(0)
    assert len(sim.get_existing_object_ids()) > 0

    # test kinematics
    I = np.identity(4)

    # test get and set translation
    sim.set_translation(np.array([0, 1.0, 0]), object_id)
    assert np.allclose(sim.get_translation(object_id), np.array([0, 1.0, 0]))

    # test get and set transform
    sim.set_transformation(I, object_id)
    assert np.allclose(sim.get_transformation(object_id), I)

    # test get and set rotation
    Q = habitat_sim.utils.quat_from_angle_axis(np.pi, np.array([0, 1.0, 0]))
    sim.set_rotation(habitat_sim.utils.quat_to_magnum(Q), object_id)
    assert np.allclose(
        sim.get_transformation(object_id),
        np.array(
            [
                [-1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, -1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        ),
    )
    assert np.allclose(
        habitat_sim.utils.quat_from_magnum(sim.get_rotation(object_id)),
        habitat_sim.utils.quat_from_coeffs(np.array([0.0, 1.0, 0.0, 0.0])),
    )

    # test object removal
    old_object_id = sim.remove_object(object_id)
    assert len(sim.get_existing_object_ids()) == 0
    assert old_object_id == object_id

    object_id = sim.add_object(0)

    prev_time = 0.0
    for _ in range(2):
        # do some kinematics here (todo: translating or rotating instead of absolute)
        sim.set_translation(np.random.rand(3), object_id)
        T = sim.get_transformation(object_id)

        # test getting observation
        obs = sim.step(random.choice(list(hab_cfg.agents[0].action_space.keys())))

        # check that time is increasing in the world
        assert sim.get_world_time() > prev_time
        prev_time = sim.get_world_time()
