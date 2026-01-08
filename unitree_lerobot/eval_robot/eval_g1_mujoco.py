"""
MuJoCo-based simulation for Unitree G1 robot evaluation.
This provides an alternative to IsaacLab for users without high-end GPUs.

Usage:
    python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
        --policy.path=path/to/pretrained_model \
        --repo_id=dataset_repo_id \
        --frequency=30
"""

import time
import torch
import logging
import numpy as np
import mujoco
import mujoco.viewer
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any
from contextlib import nullcontext

from lerobot.policies.factory import make_policy, make_pre_post_processors
from lerobot.utils.utils import get_safe_torch_device, init_logging
from lerobot.configs import parser
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.processor.rename_processor import rename_stats
from lerobot.processor import PolicyAction, PolicyProcessorPipeline

import logging_mp

logging_mp.basic_config(level=logging_mp.INFO)
logger_mp = logging_mp.get_logger(__name__)


@dataclass
class EvalMuJoCoConfig:
    """Configuration for MuJoCo-based evaluation."""
    
    # Policy configuration
    policy: Any = field(default=None)
    
    # Dataset
    repo_id: str = "unitreerobotics/G1_Dex3_ToastedBread_Dataset"
    root: str = ""
    
    # Control parameters
    frequency: float = 30.0  # Hz
    episodes: int = 0  # 0 = infinite
    
    # Robot configuration
    arm: str = "G1_29"  # G1_29 or G1_23
    ee: str = "dex3"  # dex3, dex1, inspire1, brainco
    
    # Visualization
    visualization: bool = True
    
    # MuJoCo specific
    mujoco_model_path: str = "unitree_lerobot/eval_robot/assets/g1/g1_body29_hand14.xml"
    use_gravity_compensation: bool = True
    
    # Control gains
    kp_arm: float = 100.0  # Position gain for arms
    kd_arm: float = 10.0   # Damping gain for arms
    kp_leg: float = 200.0  # Position gain for legs (locked)
    kd_leg: float = 20.0   # Damping gain for legs (locked)
    
    # Safety
    max_joint_velocity: float = 3.0  # rad/s
    
    # Other
    rename_map: dict = field(default_factory=dict)
    use_dataset: bool = False


class MuJoCoRobotController:
    """Controller for Unitree G1 robot in MuJoCo simulation."""
    
    def __init__(self, model: mujoco.MjModel, data: mujoco.MjData, cfg: EvalMuJoCoConfig):
        self.model = model
        self.data = data
        self.cfg = cfg
        
        # Joint indices for G1_29 robot
        # Arms: shoulder_pitch, shoulder_roll, shoulder_yaw, elbow, wrist_roll, wrist_pitch, wrist_yaw (x2)
        self.arm_joint_names = [
            "left_shoulder_pitch_joint", "left_shoulder_roll_joint", "left_shoulder_yaw_joint",
            "left_elbow_joint", "left_wrist_roll_joint", "left_wrist_pitch_joint", "left_wrist_yaw_joint",
            "right_shoulder_pitch_joint", "right_shoulder_roll_joint", "right_shoulder_yaw_joint",
            "right_elbow_joint", "right_wrist_roll_joint", "right_wrist_pitch_joint", "right_wrist_yaw_joint",
        ]
        
        # Hand joints (Dex3)
        self.hand_joint_names = [
            "left_hand_thumb_0_joint", "left_hand_thumb_1_joint", "left_hand_thumb_2_joint",
            "left_hand_middle_0_joint", "left_hand_middle_1_joint",
            "left_hand_index_0_joint", "left_hand_index_1_joint",
            "right_hand_thumb_0_joint", "right_hand_thumb_1_joint", "right_hand_thumb_2_joint",
            "right_hand_index_0_joint", "right_hand_index_1_joint",
            "right_hand_middle_0_joint", "right_hand_middle_1_joint",
        ]
        
        # Leg joints (to be locked)
        self.leg_joint_names = [
            "left_hip_pitch_joint", "left_hip_roll_joint", "left_hip_yaw_joint",
            "left_knee_joint", "left_ankle_pitch_joint", "left_ankle_roll_joint",
            "right_hip_pitch_joint", "right_hip_roll_joint", "right_hip_yaw_joint",
            "right_knee_joint", "right_ankle_pitch_joint", "right_ankle_roll_joint",
        ]
        
        # Waist joints (to be locked)
        self.waist_joint_names = ["waist_yaw_joint", "waist_roll_joint", "waist_pitch_joint"]
        
        # Get joint IDs
        self.arm_joint_ids = self._get_joint_ids(self.arm_joint_names)
        self.hand_joint_ids = self._get_joint_ids(self.hand_joint_names)
        self.leg_joint_ids = self._get_joint_ids(self.leg_joint_names)
        self.waist_joint_ids = self._get_joint_ids(self.waist_joint_names)
        
        # Get actuator IDs
        self.arm_actuator_ids = self._get_actuator_ids(self.arm_joint_names)
        self.hand_actuator_ids = self._get_actuator_ids(self.hand_joint_names)
        self.leg_actuator_ids = self._get_actuator_ids(self.leg_joint_names)
        self.waist_actuator_ids = self._get_actuator_ids(self.waist_joint_names)
        
        # Store initial pose for locked joints
        self.initial_leg_pos = None
        self.initial_waist_pos = None
        
        logger_mp.info(f"Found {len(self.arm_joint_ids)} arm joints")
        logger_mp.info(f"Found {len(self.hand_joint_ids)} hand joints")
        logger_mp.info(f"Found {len(self.leg_joint_ids)} leg joints")
        logger_mp.info(f"Found {len(self.waist_joint_ids)} waist joints")
    
    def _get_joint_ids(self, joint_names):
        """Get joint IDs from joint names."""
        joint_ids = []
        for name in joint_names:
            try:
                joint_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, name)
                if joint_id >= 0:
                    joint_ids.append(joint_id)
            except Exception as e:
                logger_mp.warning(f"Joint {name} not found: {e}")
        return joint_ids
    
    def _get_actuator_ids(self, joint_names):
        """Get actuator IDs from joint names."""
        actuator_ids = []
        for name in joint_names:
            try:
                # Actuator names often match joint names
                actuator_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_ACTUATOR, name)
                if actuator_id >= 0:
                    actuator_ids.append(actuator_id)
            except Exception:
                # If not found, try without "_joint" suffix
                try:
                    actuator_name = name.replace("_joint", "")
                    actuator_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_ACTUATOR, actuator_name)
                    if actuator_id >= 0:
                        actuator_ids.append(actuator_id)
                except Exception:
                    pass
        return actuator_ids
    
    def initialize_pose(self, initial_arm_pose: np.ndarray, initial_hand_pose: np.ndarray = None):
        """Initialize robot to starting pose."""
        # Set arm positions
        for i, joint_id in enumerate(self.arm_joint_ids):
            if i < len(initial_arm_pose):
                self.data.qpos[joint_id] = initial_arm_pose[i]
        
        # Set hand positions if provided
        if initial_hand_pose is not None:
            for i, joint_id in enumerate(self.hand_joint_ids):
                if i < len(initial_hand_pose):
                    self.data.qpos[joint_id] = initial_hand_pose[i]
        
        # Store initial positions for locked joints
        self.initial_leg_pos = np.array([self.data.qpos[jid] for jid in self.leg_joint_ids])
        self.initial_waist_pos = np.array([self.data.qpos[jid] for jid in self.waist_joint_ids])
        
        # Zero out velocities
        self.data.qvel[:] = 0.0
        
        # Forward kinematics
        mujoco.mj_forward(self.model, self.data)
        
        logger_mp.info("Robot initialized to starting pose")
    
    def set_control_gains(self):
        """Set PD control gains for actuators."""
        # Set gains for arm actuators
        for act_id in self.arm_actuator_ids:
            if act_id < self.model.nu:
                self.model.actuator_gainprm[act_id, 0] = self.cfg.kp_arm
                self.model.actuator_biasprm[act_id, 1] = -self.cfg.kd_arm
        
        # Set gains for leg actuators (higher to lock)
        for act_id in self.leg_actuator_ids:
            if act_id < self.model.nu:
                self.model.actuator_gainprm[act_id, 0] = self.cfg.kp_leg
                self.model.actuator_biasprm[act_id, 1] = -self.cfg.kd_leg
        
        # Set gains for waist actuators (higher to lock)
        for act_id in self.waist_actuator_ids:
            if act_id < self.model.nu:
                self.model.actuator_gainprm[act_id, 0] = self.cfg.kp_leg
                self.model.actuator_biasprm[act_id, 1] = -self.cfg.kd_leg
        
        logger_mp.info(f"Control gains set: kp_arm={self.cfg.kp_arm}, kd_arm={self.cfg.kd_arm}")
    
    def get_observation(self):
        """Get current robot state observation."""
        # Get arm joint positions
        arm_qpos = np.array([self.data.qpos[jid] for jid in self.arm_joint_ids])
        
        # Get hand joint positions
        hand_qpos = np.array([self.data.qpos[jid] for jid in self.hand_joint_ids])
        
        # Combine into state vector
        state = np.concatenate([arm_qpos, hand_qpos])
        
        return state
    
    def apply_action(self, action: np.ndarray):
        """Apply action to robot."""
        # Split action into arm and hand components
        arm_action = action[:len(self.arm_joint_ids)]
        
        # Clip velocities for safety
        current_arm_qpos = np.array([self.data.qpos[jid] for jid in self.arm_joint_ids])
        dt = self.model.opt.timestep
        max_delta = self.cfg.max_joint_velocity * dt
        arm_action = np.clip(arm_action, current_arm_qpos - max_delta, current_arm_qpos + max_delta)
        
        # Set control for arm actuators
        for i, act_id in enumerate(self.arm_actuator_ids):
            if i < len(arm_action) and act_id < self.model.nu:
                self.data.ctrl[act_id] = arm_action[i]
        
        # Handle hand action if present
        if len(action) > len(self.arm_joint_ids):
            hand_action = action[len(self.arm_joint_ids):]
            for i, act_id in enumerate(self.hand_actuator_ids):
                if i < len(hand_action) and act_id < self.model.nu:
                    self.data.ctrl[act_id] = hand_action[i]
        
        # Lock leg and waist joints to initial position
        if self.initial_leg_pos is not None:
            for i, act_id in enumerate(self.leg_actuator_ids):
                if i < len(self.initial_leg_pos) and act_id < self.model.nu:
                    self.data.ctrl[act_id] = self.initial_leg_pos[i]
        
        if self.initial_waist_pos is not None:
            for i, act_id in enumerate(self.waist_actuator_ids):
                if i < len(self.initial_waist_pos) and act_id < self.model.nu:
                    self.data.ctrl[act_id] = self.initial_waist_pos[i]
        
        # Apply gravity compensation if enabled
        if self.cfg.use_gravity_compensation:
            self._apply_gravity_compensation()
    
    def _apply_gravity_compensation(self):
        """Apply gravity compensation torques."""
        # Compute inverse dynamics to get gravity compensation
        qacc_des = np.zeros(self.model.nv)
        mujoco.mj_inverse(self.model, self.data, qacc_des)
        
        # The qfrc_inverse now contains the required forces/torques
        # Add these to the control for better stability
        for i, act_id in enumerate(self.arm_actuator_ids):
            if act_id < self.model.nu:
                joint_id = self.arm_joint_ids[i]
                if joint_id < len(self.data.qfrc_inverse):
                    # Add a fraction of gravity compensation
                    self.data.ctrl[act_id] += 0.5 * self.data.qfrc_inverse[joint_id]


def eval_policy_mujoco(cfg: EvalMuJoCoConfig, dataset: LeRobotDataset, policy, preprocessor, postprocessor):
    """Evaluate policy in MuJoCo simulation."""
    
    logger_mp.info(f"Loading MuJoCo model from: {cfg.mujoco_model_path}")
    
    # Load MuJoCo model
    model_path = Path(cfg.mujoco_model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"MuJoCo model not found: {model_path}")
    
    model = mujoco.MjModel.from_xml_path(str(model_path))
    data = mujoco.MjData(model)
    
    # Create controller
    controller = MuJoCoRobotController(model, data, cfg)
    controller.set_control_gains()
    
    # Get initial pose from dataset
    from_idx = dataset.meta.episodes["dataset_from_index"][0]
    step = dataset[from_idx]
    
    # Extract arm pose (14 DOF for G1_29)
    arm_dof = 14
    initial_arm_pose = step["observation.state"][:arm_dof].cpu().numpy()
    
    # Extract hand pose if available
    hand_dof = 14  # Dex3 has 7 DOF per hand
    if len(step["observation.state"]) > arm_dof:
        initial_hand_pose = step["observation.state"][arm_dof:arm_dof+hand_dof].cpu().numpy()
    else:
        initial_hand_pose = None
    
    # Initialize robot pose
    controller.initialize_pose(initial_arm_pose, initial_hand_pose)
    
    # Reset policy
    if policy is not None:
        policy.reset()
        preprocessor.reset()
        postprocessor.reset()
    
    logger_mp.info(f"Starting MuJoCo evaluation at {cfg.frequency} Hz")
    
    # Launch viewer if visualization enabled
    if cfg.visualization:
        with mujoco.viewer.launch_passive(model, data) as viewer:
            _run_evaluation_loop(cfg, dataset, model, data, controller, policy, preprocessor, postprocessor, viewer)
    else:
        _run_evaluation_loop(cfg, dataset, model, data, controller, policy, preprocessor, postprocessor, None)


def _run_evaluation_loop(cfg, dataset, model, data, controller, policy, preprocessor, postprocessor, viewer):
    """Run the main evaluation loop."""
    
    dt = model.opt.timestep
    control_dt = 1.0 / cfg.frequency
    sim_steps_per_control = max(1, int(control_dt / dt))
    
    logger_mp.info(f"MuJoCo timestep: {dt}s, Control dt: {control_dt}s, Steps per control: {sim_steps_per_control}")
    
    step_count = 0
    episode_count = 0
    
    try:
        while True:
            loop_start = time.time()
            
            # Get observation
            state = controller.get_observation()
            state_tensor = torch.from_numpy(state).float()
            
            # Create observation dict (simplified - no images for now)
            observation = {
                "observation.state": state_tensor,
            }
            
            # Get action from policy
            with torch.no_grad():
                preprocessed_obs = preprocessor(observation)
                action = policy.select_action(preprocessed_obs)
                action = postprocessor(action)
            
            action_np = action.cpu().numpy()
            
            # Apply action to robot
            controller.apply_action(action_np)
            
            # Step simulation multiple times
            for _ in range(sim_steps_per_control):
                mujoco.mj_step(model, data)
                if viewer is not None:
                    viewer.sync()
            
            step_count += 1
            
            # Check for episode end (simple time-based for now)
            if step_count % 1000 == 0:
                logger_mp.info(f"Steps: {step_count}, Episode: {episode_count}")
            
            # Maintain control frequency
            elapsed = time.time() - loop_start
            sleep_time = max(0, control_dt - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)
            
            # Check if we should stop
            if cfg.episodes > 0 and episode_count >= cfg.episodes:
                break
    
    except KeyboardInterrupt:
        logger_mp.info("Evaluation interrupted by user")
    finally:
        logger_mp.info(f"Evaluation complete. Total steps: {step_count}")


@parser.wrap()
def eval_main(cfg: EvalMuJoCoConfig):
    """Main evaluation function."""
    
    # Check device
    device = get_safe_torch_device(cfg.policy.device, log=True)
    
    torch.backends.cudnn.benchmark = True
    torch.backends.cuda.matmul.allow_tf32 = True
    
    logger_mp.info("Loading dataset...")
    dataset = LeRobotDataset(repo_id=cfg.repo_id, root=cfg.root if cfg.root else None)
    
    logger_mp.info("Loading policy...")
    policy = make_policy(cfg=cfg.policy, ds_meta=dataset.meta)
    policy.eval()
    
    preprocessor, postprocessor = make_pre_post_processors(
        policy_cfg=cfg.policy,
        pretrained_path=cfg.policy.pretrained_path,
        dataset_stats=rename_stats(dataset.meta.stats, cfg.rename_map),
        preprocessor_overrides={
            "device_processor": {"device": cfg.policy.device},
            "rename_observations_processor": {"rename_map": cfg.rename_map},
        },
    )
    
    with torch.no_grad(), torch.autocast(device_type=device.type) if cfg.policy.use_amp else nullcontext():
        eval_policy_mujoco(cfg, dataset, policy, preprocessor, postprocessor)
    
    logger_mp.info("Evaluation complete")


if __name__ == "__main__":
    init_logging()
    eval_main()
