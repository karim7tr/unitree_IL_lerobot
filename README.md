<div align="center">
  <h1 align="center"> unitree_IL_lerobot </h1>
  <h3 align="center"> Unitree Robotics </h3>
  <p align="center">
    <a href="./README.md"> English </a> | <a href="./docs/README_it.md"> Italiano </a> | <a href="./docs/README_fr.md"> Français </a>
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
   - Multi-language support (EN/IT/FR)

### 🏷️ v0.3

1. Update [`lerobot dataset v3.0`](https://github.com/huggingface/lerobot/blob/main/docs/source/porting_datasets_v3.mdx).

2. More policy support([`pi05`](https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies/pi05), [`groot`](https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies/groot)).

### 🏷️ v0.2

1. Add `data conversion` and `model deployment` for `brainco` and `inspire1` Dexterous hands.

2. Add the functionality of `replaying the robot dataset`.

3. Add `simulation environment verification` [unitree_sim_isaaclab].

### 🏷️ v0.1

Support `data conversion`, `model deployment`, and `real-world testing` for `G1 + Dex1 + Dex3`.

# 0. 📖 What is This?

This repository helps you **teach robots by showing them what to do**. It's a complete system for Unitree robots (G1, Z1) that works from start to finish.

**What You Can Do:**
- 🎥 Record yourself doing a task with the robot
- 🔄 Convert your recordings to a format AI can learn from
- 🧠 Train an AI model to copy what you did
- 🤖 Let the robot do the task automatically
- 💻 Test everything in simulation first (no GPU needed with MuJoCo!)

**Why It's Useful:**
- No coding needed for data collection
- Multiple AI models to choose from
- Works on regular computers (CPU-friendly simulation)
- Comprehensive guides in English, Italian, and French

## 🗂️ Repository Structure

| Directory  | Description                                                                                              |
| ---------- | -------------------------------------------------------------------------------------------------------- |
| `lerobot/` | LeRobot repository for training (submodule, commit: `0878c68`) |
| `utils/` | Unitree data processing tools (conversion, sorting) |
| `eval_robot/` | Robot deployment and evaluation scripts |
| `test/` | Test suite for dataset loading and conversion |
| `docs/` | Multi-language documentation |

# 1. 📦 Getting Started

## Step 1: Install Basic Requirements

First, set up Python and the AI framework:

```bash
# Clone this repository
git clone --recurse-submodules https://github.com/karim7tr/unitree_IL_lerobot.git
cd unitree_IL_lerobot

# Create Python environment (Python 3.10 required)
conda create -y -n unitree_lerobot python=3.10
conda activate unitree_lerobot

# Install core dependencies
conda install pinocchio -c conda-forge
conda install ffmpeg=7.1.1 -c conda-forge

# Install LeRobot (the AI training framework)
cd unitree_lerobot/lerobot && pip install -e .

# Install this package
cd ../../ && pip install -e .
```

## Step 2: Choose Your Simulation (Optional for Testing)

You have two options:

### Option A: MuJoCo (Recommended - No GPU Needed!) ⭐

Simple physics simulation that runs on any computer:

```bash
pip install mujoco
```

**Why choose this:**
- Works on laptops and regular PCs
- No expensive GPU required
- Good for testing and development
- See [MUJOCO_SIMULATION_GUIDE.md](./MUJOCO_SIMULATION_GUIDE.md) for details

### Option B: IsaacLab (Advanced - GPU Required)

High-end simulation for complex scenarios:

```bash
# Follow setup at: https://github.com/unitreerobotics/unitree_sim_isaaclab
```

**Requirements:** NVIDIA GPU with 8GB+ VRAM

## Step 3: For Real Robot (Optional)

If you have a physical Unitree robot:

```bash
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
cd unitree_sdk2_python && pip install -e .
```

# 2. 🎥 Working With Data

## Option 1: Use Example Data

Try it out with pre-recorded demonstrations:

```python
from lerobot.datasets.lerobot_dataset import LeRobotDataset

# Load a demo dataset
dataset = LeRobotDataset(repo_id="unitreerobotics/G1_Dex3_ToastedBread_Dataset")

# Look at what's inside
print(f"Dataset has {len(dataset)} frames")
episode_index = 0
from_idx = dataset.meta.episodes["dataset_from_index"][episode_index]
to_idx = dataset.meta.episodes["dataset_to_index"][episode_index]

for step_idx in range(from_idx, to_idx):
    step = dataset[step_idx]  # Each step has images and robot positions
```

View it visually:

```bash
cd unitree_lerobot/lerobot
python src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id unitreerobotics/G1_Dex3_ToastedBread_Dataset \
    --episode-index 0
```

## Option 2: Record Your Own Data

1. Use the [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate/tree/g1) tool to control your robot
2. Record yourself doing the task
3. Your recordings are saved as JSON files with images

## Option 3: Convert Your Data

Once you have recordings, convert them to the AI-readable format:

```bash
# Step 1: Organize your recordings
python unitree_lerobot/utils/sort_and_rename_folders.py \
    --data_dir $HOME/datasets/my_task

# Step 2: Convert to AI format
python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
    --raw-dir $HOME/datasets/my_task \
    --repo-id myname/my_task \
    --robot_type Unitree_G1_Dex3 \
    --push_to_hub
```

**Robot types you can use:**
- `Unitree_G1_Dex3` - G1 robot with dexterous hands (most common)
- `Unitree_G1_Dex1` - G1 with simple grippers
- `Unitree_Z1_Dual` - Desktop dual-arm robot
- And 8 more configurations (see [QUICK_REFERENCE.md](./QUICK_REFERENCE.md))

# 3. 🧠 Training the AI

Now teach the AI to copy what you demonstrated. Choose a model:

## Quick Start (Recommended)

**ACT Model** - Fast training, good results:

```bash
cd unitree_lerobot/lerobot

python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=myname/my_task \
    --policy.type=act \
    --policy.push_to_hub=false
```

Training takes ~8 hours on a good GPU. The model learns to replicate your demonstrations.

## Advanced Options

**Diffusion Model** - Better performance, slower training:

```bash
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=myname/my_task \
    --policy.type=diffusion
```

**Other models available:** Pi0, Pi05, Groot (see [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for details)

# 4. 🎮 Testing Your Trained Model

## Test in MuJoCo Simulation (No GPU Needed!) ⭐

This is what we built together - a stable simulation you can run on any computer:

```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=myname/my_task \
    --frequency=30 \
    --visualization=true
```

**Why use this:**
- ✅ Works on any computer (no GPU needed)
- ✅ Robot won't fall down (we fixed this!)
- ✅ Smooth, realistic movement
- ✅ Easy to adjust if something seems off

**Having issues?** See [MUJOCO_SIMULATION_GUIDE.md](./MUJOCO_SIMULATION_GUIDE.md) for fixes.

## Test on Real Robot

Once you're happy with simulation results:

```bash
python unitree_lerobot/eval_robot/eval_g1.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=myname/my_task \
    --arm="G1_29" \
    --ee="dex3" \
    --send_real_robot=true
```

**Important:** Always test in simulation first!

## Alternative: IsaacLab Simulation (If You Have a GPU)

```bash
python unitree_lerobot/eval_robot/eval_g1_sim.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=myname/my_task
```

# 5. 💡 Common Issues & Solutions

| Problem | Quick Fix |
|---------|-----------|
| **"401 Unauthorized" when loading datasets** | Run `huggingface-cli login` and enter your token |
| **Robot falls in MuJoCo** | It's already fixed in our code! Just use the default settings |
| **Training is slow** | Use ACT model instead of Diffusion, or reduce batch size |
| **FFmpeg errors** | Run: `conda install -c conda-forge ffmpeg=7.1.1` |
| **Out of memory** | Use a smaller model or enable gradient checkpointing |

**Need more help?** Check [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for detailed troubleshooting.

# 6. 📚 What We Built Together

This repository now includes:

1. **Complete Documentation** (what you're reading!)
   - Simple, clear explanations
   - Step-by-step guides
   - Available in English, Italian, and French

2. **MuJoCo Simulation** (the fix for GPU-less testing)
   - Prevents robot from falling
   - Smooth, stable movements
   - Works on any computer
   - See [MUJOCO_SIMULATION_GUIDE.md](./MUJOCO_SIMULATION_GUIDE.md)

3. **Helpful Guides**
   - [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Commands and configs
   - [ANALYSIS_SUMMARY.md](./ANALYSIS_SUMMARY.md) - Quick overview
   - [WORKSPACE_ANALYSIS.md](./WORKSPACE_ANALYSIS.md) - Detailed structure
   - [TECHNICAL_DEEP_DIVE.md](./TECHNICAL_DEEP_DIVE.md) - How it all works

# 7. 🎯 Quick Example: End-to-End

Here's the complete flow from start to finish:

```bash
# 1. Setup (one time)
conda create -y -n unitree_lerobot python=3.10
conda activate unitree_lerobot
pip install mujoco
# ... follow Step 1 above for full setup

# 2. Get some data (use example or record your own)
# Already done if using: unitreerobotics/G1_Dex3_ToastedBread_Dataset

# 3. Train the AI (8 hours)
cd unitree_lerobot/lerobot
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=unitreerobotics/G1_Dex3_ToastedBread_Dataset \
    --policy.type=act

# 4. Test it (immediate)
cd ../..
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=unitree_lerobot/lerobot/outputs/.../pretrained_model \
    --repo_id=unitreerobotics/G1_Dex3_ToastedBread_Dataset
```

That's it! You've taught a robot to do a task.

# 8. 🌍 Languages & Support

**This README is available in:**
- [English](./README.md) (you are here)
- [Italiano](./docs/README_it.md)
- [Français](./docs/README_fr.md)

**Get Help:**
- Check the guides in this repository
- Open an issue on GitHub
- Join the [Discord community](https://discord.gg/ZwcVwxv5rq)

# 9. 📄 License

Apache License 2.0 - Free to use for any purpose

---

**Quick Links:**
- [English README](./README.md) | [Italian README](./docs/README_it.md) | [French README](./docs/README_fr.md)
- [MuJoCo Guide](./MUJOCO_SIMULATION_GUIDE.md) | [Quick Reference](./QUICK_REFERENCE.md) | [Technical Deep Dive](./TECHNICAL_DEEP_DIVE.md)
