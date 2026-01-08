<div align="center">
  <h1 align="center"> unitree_IL_lerobot </h1>
  <h3 align="center"> Unitree Robotics </h3>
  <p align="center">
    <a href="./README.md"> English </a> | <a href="./docs/README_it.md"> Italiano </a> | <a href="./docs/README_fr.md"> Français </a> | <a href="./docs/README_zh.md"> 中文 </a>
  </p>
    <p align="center">
     <a href="https://discord.gg/ZwcVwxv5rq" target="_blank"><img src="https://img.shields.io/badge/-Discord-5865F2?style=flat&logo=Discord&logoColor=white" alt="Unitree LOGO"></a>
  </p>
</div>

| Unitree Robotics repositories                      | link                                                                               |
| -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Unitree Datasets                                   | [unitree datasets](https://huggingface.co/unitreerobotics)                         |
| AVP Teleoperate                                    | [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate)              |
| Unitree Sim IsaacLab                               | [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab)    |
| MuJoCo Simulation (NEW)                            | See [MUJOCO_SIMULATION_GUIDE.md](./MUJOCO_SIMULATION_GUIDE.md)                    |
| Conversion of various versions of lerobot datasets | [any4lerobot](https://github.com/Tavish9/any4lerobot/tree/main/ds_version_convert) |

# 📚 Documentation

**NEW: Comprehensive workspace documentation available!**

| Document | Description | Reading Time |
|----------|-------------|--------------|
| [ANALYSIS_SUMMARY.md](./ANALYSIS_SUMMARY.md) | Executive overview, health checks, quick start | 5 min |
| [WORKSPACE_ANALYSIS.md](./WORKSPACE_ANALYSIS.md) | Repository structure, features, 11 robot configs | 15 min |
| [TECHNICAL_DEEP_DIVE.md](./TECHNICAL_DEEP_DIVE.md) | System architecture, data flows, benchmarks | 30 min |
| [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) | Commands, config cheat sheets, troubleshooting | Reference |
| [MUJOCO_SIMULATION_GUIDE.md](./MUJOCO_SIMULATION_GUIDE.md) | MuJoCo simulation setup (CPU-friendly) | 20 min |

# 🔖 Release Notes

### 🏷️ v0.4 (NEW)

1. **MuJoCo Simulation Support** - CPU-friendly alternative to IsaacLab
   - Standalone evaluation script with stability fixes
   - Prevents robot falling and random joint motion
   - Configurable PD gains and gravity compensation
   - No GPU required - runs on CPU

2. **Comprehensive Documentation**
   - Workspace analysis and architecture deep dive
   - Quick reference guide with troubleshooting
   - Multi-language support (EN/IT/FR/ZH)

### 🏷️ v0.3

1. Update [`lerobot dataset v3.0`](https://github.com/huggingface/lerobot/blob/main/docs/source/porting_datasets_v3.mdx).

2. More policy support([`pi05`](https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies/pi05), [`groot`](https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies/groot)).

### 🏷️ v0.2

1. Add `data conversion` and `model deployment` for `brainco` and `inspire1` Dexterous hands.

2. Add the functionality of `replaying the robot dataset`.

3. Add `simulation environment verification` [unitree_sim_isaaclab].

### 🏷️ v0.1

Support `data conversion`, `model deployment`, and `real-world testing` for `G1 + Dex1 + Dex3`.

# 0. 📖 Introduction

This repository provides a **complete imitation learning pipeline** for Unitree humanoid robots (G1, Z1) using the [LeRobot](https://github.com/huggingface/lerobot) framework. Train robots through demonstration - from data collection to real-world deployment.

**Key Features:**
- ✅ Data conversion (JSON → LeRobot format)
- ✅ Training with multiple policies (ACT, Diffusion, Pi0, Pi05, Groot)
- ✅ Real-time robot control (30 Hz)
- ✅ Two simulation options: IsaacLab (GPU) or MuJoCo (CPU)
- ✅ 11 robot configurations supported

`❗Tips: If you have any questions, ideas or suggestions, please feel free to raise them at any time. We will do our best to solve and implement them.`

## 🗂️ Repository Structure

| Directory  | Description                                                                                              |
| ---------- | -------------------------------------------------------------------------------------------------------- |
| `lerobot/` | LeRobot repository for training (submodule, commit: `0878c68`) |
| `utils/` | Unitree data processing tools (conversion, sorting) |
| `eval_robot/` | Robot deployment and evaluation scripts |
| `test/` | Test suite for dataset loading and conversion |
| `docs/` | Multi-language documentation |

# 1. 📦 Environment Setup

## 1.1 🦾 LeRobot Environment Setup

Install the [LeRobot](https://github.com/huggingface/lerobot) framework and dependencies:

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/karim7tr/unitree_IL_lerobot.git
cd unitree_IL_lerobot

# If already cloned, update submodules
git submodule update --init --recursive

# Create conda environment
conda create -y -n unitree_lerobot python=3.10
conda activate unitree_lerobot

# Install dependencies
conda install pinocchio -c conda-forge
conda install ffmpeg=7.1.1 -c conda-forge

# Install LeRobot
cd unitree_lerobot/lerobot && pip install -e .

# Install unitree_lerobot
cd ../../ && pip install -e .
```

## 1.2 🕹️ unitree_sdk2_python (For Real Robot)

For DDS communication with Unitree robots:

```bash
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
cd unitree_sdk2_python && pip install -e .
```

## 1.3 🎮 Simulation Setup

### Option A: IsaacLab (GPU Required)

For high-performance simulation with GPU:

```bash
# Follow instructions at:
# https://github.com/unitreerobotics/unitree_sim_isaaclab
```

**Requirements:** NVIDIA GPU with 8GB+ VRAM, CUDA support

### Option B: MuJoCo (CPU-Friendly) ⭐ NEW

For lightweight simulation without GPU:

```bash
pip install mujoco
```

**No GPU required!** See [MUJOCO_SIMULATION_GUIDE.md](./MUJOCO_SIMULATION_GUIDE.md) for complete setup.

# 2. ⚙️ Data Collection and Conversion

## 2.1 🖼️ Load Existing Datasets

Load pre-recorded datasets from Hugging Face:

```python
from lerobot.datasets.lerobot_dataset import LeRobotDataset

# Load dataset
dataset = LeRobotDataset(repo_id="unitreerobotics/G1_Dex3_ToastedBread_Dataset")

# Access episode
episode_index = 0
from_idx = dataset.meta.episodes["dataset_from_index"][episode_index]
to_idx = dataset.meta.episodes["dataset_to_index"][episode_index]

for step_idx in range(from_idx, to_idx):
    step = dataset[step_idx]
```

**Visualization:**

```bash
cd unitree_lerobot/lerobot
python src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id unitreerobotics/G1_Dex3_ToastedBread_Dataset \
    --episode-index 0
```

## 2.2 🔨 Data Collection

Collect your own data using [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate/tree/g1) with Unitree G1 robot.

**Output format:**
```
datasets/
└── task_name/
    ├── episode_0001/
    │   ├── audios/
    │   ├── colors/
    │   ├── depths/
    │   └── data.json
    ├── episode_0002/
    └── ...
```

## 2.3 🛠️ Data Conversion

### Step 1: Sort and Rename

Ensure sequential episode naming:

```bash
python unitree_lerobot/utils/sort_and_rename_folders.py \
    --data_dir $HOME/datasets/task_name
```

### Step 2: Convert to LeRobot Format

```bash
python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
    --raw-dir $HOME/datasets/task_name \
    --repo-id your_name/task_name \
    --robot_type Unitree_G1_Dex3 \
    --push_to_hub
```

**Supported robot types:**
- `Unitree_Z1_Single`, `Unitree_Z1_Dual`
- `Unitree_G1_Dex1`, `Unitree_G1_Dex3`
- `Unitree_G1_Brainco`, `Unitree_G1_Inspire`
- `Unitree_G1_Dex1_Sim` (for IsaacLab)
- And 4 more mobile/lift configurations

# 3. 🚀 Training

Train policies using LeRobot. See [official LeRobot docs](https://github.com/huggingface/lerobot/tree/main/docs/source) for details.

## 3.1 ACT Policy (Fast, Good Baseline)

```bash
cd unitree_lerobot/lerobot

python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=your_name/task_name \
    --policy.type=act \
    --policy.push_to_hub=false
```

## 3.2 Diffusion Policy (Better Performance)

```bash
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=your_name/task_name \
    --policy.type=diffusion \
    --policy.push_to_hub=false
```

## 3.3 Pi0 Policy

```bash
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=your_name/task_name \
    --policy.type=pi0 \
    --policy.push_to_hub=false
```

## 3.4 Pi05 Policy (Vision-Language)

```bash
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=your_name/task_name \
    --policy.type=pi05 \
    --policy.pretrained_path=lerobot/pi05_base \
    --policy.compile_model=true \
    --policy.gradient_checkpointing=true \
    --policy.dtype=bfloat16 \
    --policy.push_to_hub=false
```

## 3.5 Groot Policy

```bash
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=your_name/task_name \
    --policy.type=groot \
    --policy.tune_diffusion_model=false \
    --policy.push_to_hub=false
```

**Multi-GPU training:** See [LeRobot multi-GPU docs](https://github.com/huggingface/lerobot/blob/main/docs/source/multi_gpu_training.mdx)

# 4. 🤖 Deployment and Evaluation

## 4.1 Real Robot Deployment

Deploy trained policy on physical Unitree G1:

```bash
# Start image server first (see avp_teleoperate docs)

python unitree_lerobot/eval_robot/eval_g1.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=your_name/task_name \
    --arm="G1_29" \
    --ee="dex3" \
    --frequency=30 \
    --visualization=true \
    --send_real_robot=true
```

## 4.2 IsaacLab Simulation

Test in high-fidelity GPU simulation:

```bash
python unitree_lerobot/eval_robot/eval_g1_sim.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=your_name/task_name \
    --arm="G1_29" \
    --ee="dex3" \
    --frequency=30 \
    --visualization=true
```

## 4.3 MuJoCo Simulation ⭐ NEW

Test with CPU-friendly MuJoCo simulation:

```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=your_name/task_name \
    --frequency=30 \
    --kp_arm=100.0 \
    --kd_arm=10.0 \
    --use_gravity_compensation=true \
    --visualization=true
```

**Why MuJoCo?**
- ✅ No GPU required (runs on CPU)
- ✅ Simple installation (`pip install mujoco`)
- ✅ Stable physics with configurable PD gains
- ✅ Prevents robot falling and random motion

See [MUJOCO_SIMULATION_GUIDE.md](./MUJOCO_SIMULATION_GUIDE.md) for troubleshooting.

## 4.4 Dataset Replay

Replay dataset trajectories on robot:

```bash
python unitree_lerobot/eval_robot/replay_robot.py \
    --repo_id=your_name/task_name \
    --episodes=0 \
    --frequency=30 \
    --arm="G1_29" \
    --ee="dex3" \
    --visualization=true
```

## 4.5 Dataset Evaluation

Evaluate policy on dataset:

```bash
python unitree_lerobot/eval_robot/eval_g1_dataset.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=your_name/task_name \
    --arm="G1_29" \
    --ee="dex3" \
    --visualization=true
```

# 5. 🔧 Configuration Reference

## Robot Types

| Type | Arms | End-Effector | DOF | Use Case |
|------|------|--------------|-----|----------|
| `Unitree_Z1_Single` | Single | Gripper | 7 | Desktop manipulation |
| `Unitree_Z1_Dual` | Dual | Gripper | 14 | Bimanual tasks |
| `Unitree_G1_Dex1` | Dual | 1-DOF gripper | 16 | Simple grasping |
| `Unitree_G1_Dex3` | Dual | 7-DOF hand | 28 | Dexterous manipulation |
| `Unitree_G1_Brainco` | Dual | BrainCo hand | 26 | Prosthetic research |
| `Unitree_G1_Inspire` | Dual | Inspire1 hand | 26 | Advanced grasping |

## Common Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--arm` | `G1_29` | Robot version (`G1_29` or `G1_23`) |
| `--ee` | `dex3` | End-effector (`dex3`, `dex1`, `inspire1`, `brainco`) |
| `--frequency` | 30 | Control frequency (Hz) |
| `--episodes` | 0 | Number of episodes (0 = infinite) |
| `--visualization` | true | Enable 3D visualization |

# 6. 🤔 Troubleshooting

| Problem | Solution |
|---------|----------|
| **401 Unauthorized (HuggingFace)** | Run `huggingface-cli login` |
| **FFmpeg errors** | `conda install -c conda-forge ffmpeg=7.1.1` |
| **Robot falls in MuJoCo** | Increase `--kp_leg` and enable `--use_gravity_compensation` |
| **Random joint motion** | Lower `--kp_arm`, increase `--kd_arm`, reduce `--max_joint_velocity` |
| **Slow training** | Reduce `--training.batch_size` or use smaller policy |
| **GPU out of memory** | Enable `--policy.gradient_checkpointing=true` |

See [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for more troubleshooting.

# 7. 📖 Learning Resources

## Getting Started (Beginner)

1. Read [ANALYSIS_SUMMARY.md](./ANALYSIS_SUMMARY.md) - Overview
2. Load demo dataset (section 2.1)
3. Visualize dataset
4. Run MuJoCo simulation with pretrained model

## Intermediate

1. Collect own data with `avp_teleoperate`
2. Convert to LeRobot format
3. Train ACT policy
4. Evaluate in simulation

## Advanced

1. Deploy on real robot
2. Try different policies (Diffusion, Pi0, Groot)
3. Add custom robot configuration
4. Modify controllers for your hardware

## Documentation Reading Order

```
1. ANALYSIS_SUMMARY.md       → Quick overview (5 min)
2. WORKSPACE_ANALYSIS.md      → Understand structure (15 min)
3. QUICK_REFERENCE.md         → Commands & examples (reference)
4. MUJOCO_SIMULATION_GUIDE.md → Simulation setup (20 min)
5. TECHNICAL_DEEP_DIVE.md     → Architecture details (30 min)
```

# 8. 🎬 Complete Example Workflow

```bash
# 1. Setup environment
conda create -y -n unitree_lerobot python=3.10
conda activate unitree_lerobot
# ... (see section 1.1)

# 2. Convert your data
python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
    --raw-dir $HOME/datasets/pick_apple \
    --repo-id myname/pick_apple \
    --robot_type Unitree_G1_Dex3 \
    --push_to_hub

# 3. Train policy
cd unitree_lerobot/lerobot
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=myname/pick_apple \
    --policy.type=act

# 4. Test in MuJoCo simulation (no GPU needed!)
cd ../..
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=unitree_lerobot/lerobot/outputs/.../pretrained_model \
    --repo_id=myname/pick_apple \
    --frequency=30

# 5. Deploy on real robot
python unitree_lerobot/eval_robot/eval_g1.py \
    --policy.path=unitree_lerobot/lerobot/outputs/.../pretrained_model \
    --repo_id=myname/pick_apple \
    --arm="G1_29" \
    --ee="dex3"
```

# 9. 🙏 Acknowledgements

This codebase builds upon these excellent open-source projects:

1. [LeRobot](https://github.com/huggingface/lerobot) - Training framework
2. [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python) - Robot communication
3. [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate) - Data collection
4. [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab) - Simulation
5. [MuJoCo](https://github.com/google-deepmind/mujoco) - Physics simulation

# 10. 📞 Support

- **Documentation:** Check docs in this repository
- **Issues:** [GitHub Issues](https://github.com/karim7tr/unitree_IL_lerobot/issues)
- **Discord:** [Unitree Community](https://discord.gg/ZwcVwxv5rq)
- **Datasets:** [HuggingFace Hub](https://huggingface.co/unitreerobotics)

# 11. 📄 License

Apache License 2.0 - See [LICENSE](./LICENSE) file

---

**Quick Links:**
- [English README](./README.md) | [Italian README](./docs/README_it.md) | [French README](./docs/README_fr.md) | [Chinese README](./docs/README_zh.md)
- [MuJoCo Guide](./MUJOCO_SIMULATION_GUIDE.md) | [Quick Reference](./QUICK_REFERENCE.md) | [Technical Deep Dive](./TECHNICAL_DEEP_DIVE.md)
