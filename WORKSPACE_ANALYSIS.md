# Unitree IL LeRobot - Workspace Analysis

**Generated:** 2026-01-08

---

## 📋 Executive Summary

This is a **Unitree Robotics** repository for **Imitation Learning (IL)** using the LeRobot framework. It provides comprehensive tooling for data collection, conversion, training, and deployment of robotic manipulation policies on Unitree humanoid robots (especially G1) with various end-effectors.

**Version:** 0.3.0  
**Primary Purpose:** Training and deploying imitation learning policies for Unitree robots  
**Framework:** Built on top of HuggingFace's [LeRobot](https://github.com/huggingface/lerobot)

---

## 🏗️ Repository Structure

```
unitree_IL_lerobot/
├── .git/                         # Git version control
├── .gitmodules                   # Submodule configuration (lerobot)
├── .pre-commit-config.yaml       # Code quality hooks
├── LICENSE                       # Apache 2.0 license
├── README.md                     # English documentation (343 lines)
├── docs/
│   └── README_zh.md              # Chinese documentation (313 lines)
├── pyproject.toml                # Python project configuration
├── test/                         # Test suite
│   ├── test_load_dataset.py
│   ├── test_load_h5.py
│   └── test_local_push_to_hub.py
└── unitree_lerobot/              # Main package directory
    ├── lerobot/                  # LeRobot submodule (HuggingFace)
    ├── utils/                    # Data conversion utilities
    │   ├── constants.py          # Robot configurations
    │   ├── convert_unitree_json_to_lerobot.py
    │   ├── convert_unitree_json_to_h5.py
    │   ├── convert_lerobot_to_h5.py
    │   └── sort_and_rename_folders.py
    └── eval_robot/               # Robot control and evaluation
        ├── assets/
        ├── eval_g1.py            # Real-world G1 evaluation
        ├── eval_g1_dataset.py    # Dataset evaluation
        ├── eval_g1_sim.py        # Simulation evaluation
        ├── make_robot.py         # Robot interface setup
        ├── replay_robot.py       # Dataset replay on robot
        ├── image_server/         # Image streaming
        ├── robot_control/        # Robot arm/hand control
        └── utils/                # Evaluation utilities
```

---

## 🎯 Core Functionality

### 1. **Data Collection & Conversion**
- Converts JSON-formatted teleoperation data to LeRobot dataset format (v2.0+, v3.0)
- Supports multiple robot configurations via `constants.py`
- Handles camera images, robot states, and actions
- Direct upload to HuggingFace Hub

### 2. **Supported Robot Configurations**

| Robot Type | Description | Cameras | DOF |
|------------|-------------|---------|-----|
| `Unitree_Z1_Single` | Single Z1 arm | 2 (high, wrist) | 7 |
| `Unitree_Z1_Dual` | Dual Z1 arms | 3 (high, left/right wrist) | 14 |
| `Unitree_G1_Dex1` | G1 + Dex1 grippers | 4 (binocular + wrist) | 16 |
| `Unitree_G1_Dex3` | G1 + Dex3 hands | 4 (binocular + wrist) | 28 |
| `Unitree_G1_Brainco` | G1 + BrainCo hands | 4 | 26 |
| `Unitree_G1_Inspire` | G1 + Inspire1 hands | 4 | 26 |
| `Unitree_G1_Dex1_Sim` | Simulation variant | 3 | 16 |

Additional configurations include mobile base and lift variations.

### 3. **Policy Training**
Supports multiple state-of-the-art imitation learning policies:
- **ACT** (Action Chunking Transformer)
- **Diffusion Policy**
- **Pi0** (Policy Zero)
- **Pi05** (Policy Zero 5)
- **Gr00t** (Generalist Robot)

All training runs through the LeRobot framework with customizable hyperparameters.

### 4. **Real-World Deployment**
- `eval_g1.py`: Deploy trained policies on physical G1 robots
- `eval_g1_sim.py`: Test in IsaacLab simulation environment
- `eval_g1_dataset.py`: Evaluate performance on recorded datasets
- `replay_robot.py`: Replay dataset trajectories on the robot

### 5. **Visualization & Debugging**
- Rerun-based 3D visualization
- Image streaming via custom image server
- Real-time state and action monitoring

---

## 🔧 Technical Architecture

### Dependencies
```python
# Core (from pyproject.toml)
- Python 3.10 (strict requirement)
- transformers >= 4.45.2
- tyro >= 0.9.10
- matplotlib >= 3.9.0
- meshcat == 0.3.2
- logging_mp
- unitree_sdk2_python (via git, for robot communication)

# From LeRobot submodule
- torch, torchvision
- huggingface_hub
- opencv-python
- ffmpeg (for video encoding)
```

### Code Quality Tools
- **Ruff**: Linting and formatting (120 char line length)
- **Bandit**: Security scanning (configured to skip certain checks)
- **Pre-commit hooks**: Automated checks before commits

### Submodules
- `unitree_lerobot/lerobot` → [HuggingFace LeRobot](https://github.com/huggingface/lerobot) @ commit `a5b29d4`
  - Provides core training loop, dataset utilities, and policy implementations
  - This repository extends it for Unitree-specific hardware

---

## 🔄 Typical Workflow

1. **Data Collection**
   - Use [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate) to collect demonstrations
   - Data stored in JSON format with images

2. **Data Preprocessing**
   ```bash
   # Sort and rename episodes
   python unitree_lerobot/utils/sort_and_rename_folders.py --data_dir <path>
   
   # Convert to LeRobot format
   python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
       --raw-dir <data_dir> \
       --repo-id <hf_repo> \
       --robot_type Unitree_G1_Dex3 \
       --push_to_hub
   ```

3. **Training**
   ```bash
   cd unitree_lerobot/lerobot
   python src/lerobot/scripts/lerobot_train.py \
       --dataset.repo_id=<hf_repo> \
       --policy.type=diffusion
   ```

4. **Evaluation**
   ```bash
   # On real robot
   python unitree_lerobot/eval_robot/eval_g1.py \
       --policy.path=<checkpoint_path> \
       --repo_id=<hf_repo> \
       --arm="G1_29" --ee="dex3"
   
   # In simulation
   python unitree_lerobot/eval_robot/eval_g1_sim.py <args>
   ```

---

## 📊 Key Features

### ✅ Strengths
1. **Comprehensive robot support**: 11 different robot configurations
2. **Production-ready**: Includes data conversion, training, and deployment
3. **Well-documented**: Extensive README in both English and Chinese
4. **Active development**: Recent v0.3 update with dataset v3.0 and new policies
5. **Open ecosystem**: Integrates with HuggingFace Hub for dataset/model sharing
6. **Simulation support**: Works with IsaacLab for safe testing

### 🎓 Educational Value
- Demonstrates end-to-end imitation learning pipeline
- Shows best practices for robotics ML projects
- Examples of multi-camera, multi-DOF robot control
- Integration with modern ML tools (HuggingFace, PyTorch)

---

## 🔗 Related Resources

| Resource | Link |
|----------|------|
| Datasets | [HuggingFace: unitreerobotics](https://huggingface.co/unitreerobotics) |
| Teleoperation | [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate) |
| Simulation | [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab) |
| Dataset Conversion | [any4lerobot](https://github.com/Tavish9/any4lerobot) |
| Discord | [Unitree Community](https://discord.gg/ZwcVwxv5rq) |

---

## 🧪 Testing Infrastructure

Three test files verify core functionality:
- `test_load_dataset.py` - LeRobot dataset loading
- `test_load_h5.py` - HDF5 file handling
- `test_local_push_to_hub.py` - HuggingFace Hub integration

---

## 🚀 Recent Updates (v0.3)

1. **LeRobot dataset v3.0** compatibility
2. New policy support: **Pi05** and **Gr00t**
3. Enhanced documentation and examples

---

## 💡 Use Cases

This workspace is designed for:
- **Robotics researchers** exploring imitation learning
- **Unitree robot owners** wanting to teach their robots new tasks
- **ML engineers** interested in vision-based manipulation
- **Students** learning about embodied AI and robot learning

---

## 🛠️ Development Status

- **License:** Apache 2.0 (permissive, commercial use allowed)
- **Maturity:** Production-ready (v0.3.0)
- **Activity:** Active development (recent commits)
- **Community:** Discord support available
- **Language:** Python 3.10 (strict requirement)

---

## 📝 Notes for Developers

### Environment Setup Gotchas
1. Must use Python 3.10 (not 3.11+)
2. FFmpeg required for video encoding (`conda install ffmpeg=7.1.1`)
3. Pinocchio needed for kinematics (`conda install pinocchio -c conda-forge`)
4. unitree_sdk2_python for robot communication (DDS-based)

### Code Organization
- **Separation of concerns**: Data utils, training (via lerobot), deployment
- **Configuration-driven**: Robot configs in `constants.py`, easy to extend
- **Modular**: Can use components independently (e.g., just data conversion)

---

## 🎬 Getting Started

**Quickest way to explore:**
```bash
# 1. Clone with submodules
git clone --recurse-submodules https://github.com/unitreerobotics/unitree_IL_lerobot.git

# 2. Create environment
conda create -y -n unitree_lerobot python=3.10
conda activate unitree_lerobot
conda install pinocchio ffmpeg=7.1.1 -c conda-forge

# 3. Install packages
cd unitree_IL_lerobot/unitree_lerobot/lerobot && pip install -e .
cd ../.. && pip install -e .

# 4. Load a demo dataset
python -c "
from lerobot.datasets.lerobot_dataset import LeRobotDataset
ds = LeRobotDataset('unitreerobotics/G1_Dex3_ToastedBread_Dataset')
print(f'Dataset has {len(ds)} frames')
"
```

---

## 🏁 Conclusion

**This workspace represents a complete, production-grade system for teaching Unitree robots through imitation learning.** It bridges the gap between raw teleoperation data and deployed robot behaviors, leveraging modern ML infrastructure (HuggingFace, PyTorch) and state-of-the-art policies.

The codebase is well-structured, actively maintained, and includes extensive documentation. It's suitable for both research and practical applications in robotic manipulation.

**Key Takeaway:** If you own a Unitree G1 robot and want to teach it new manipulation skills, this repository provides everything needed from data collection to deployment.
