# Unitree IL LeRobot - Quick Reference Guide

**For: Researchers, Engineers, and Robot Operators**

---

## 🚀 Quick Start Commands

### Installation (5 minutes)
```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/karim7tr/unitree_IL_lerobot.git
cd unitree_IL_lerobot

# Create environment
conda create -y -n unitree_lerobot python=3.10
conda activate unitree_lerobot
conda install pinocchio ffmpeg=7.1.1 -c conda-forge

# Install packages
cd unitree_lerobot/lerobot && pip install -e .
cd ../.. && pip install -e .

# Install robot SDK (if using real hardware)
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
cd unitree_sdk2_python && pip install -e .
```

---

## 📋 Common Workflows

### 1. Load a Demo Dataset
```python
from lerobot.datasets.lerobot_dataset import LeRobotDataset

# Load from HuggingFace Hub
dataset = LeRobotDataset(repo_id="unitreerobotics/G1_Dex3_ToastedBread_Dataset")
print(f"Dataset has {len(dataset)} frames, {dataset.num_episodes} episodes")

# Access a frame
frame = dataset[0]
print(frame.keys())  # See available data
```

### 2. Convert Your Own Data
```bash
# Step 1: Organize data (ensure sequential naming)
python unitree_lerobot/utils/sort_and_rename_folders.py \
    --data_dir $HOME/datasets/my_task

# Step 2: Convert to LeRobot format
python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
    --raw-dir $HOME/datasets/my_task \
    --repo-id username/my_task \
    --robot_type Unitree_G1_Dex3 \
    --push_to_hub
```

### 3. Train a Policy
```bash
cd unitree_lerobot/lerobot

# ACT (fast, good baseline)
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=username/my_task \
    --policy.type=act \
    --policy.push_to_hub=false

# Diffusion (better performance, slower)
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=username/my_task \
    --policy.type=diffusion \
    --policy.push_to_hub=false
```

### 4. Deploy on Robot
```bash
# Test on real G1 robot
python unitree_lerobot/eval_robot/eval_g1.py \
    --policy.path=lerobot/outputs/.../pretrained_model \
    --repo_id=username/my_task \
    --arm="G1_29" \
    --ee="dex3" \
    --frequency=30 \
    --visualization=true

# Test in simulation first (safer)
python unitree_lerobot/eval_robot/eval_g1_sim.py \
    --policy.path=lerobot/outputs/.../pretrained_model \
    --repo_id=username/my_task \
    --arm="G1_29" \
    --ee="dex3"
```

### 5. Replay Dataset on Robot
```bash
# Verify your robot matches the dataset
python unitree_lerobot/eval_robot/replay_robot.py \
    --repo_id=username/my_task \
    --episodes=0 \
    --arm="G1_29" \
    --ee="dex3" \
    --frequency=30
```

---

## 🤖 Robot Configuration Cheat Sheet

| If you have... | Use `--robot_type` | Use `--arm` | Use `--ee` |
|----------------|-------------------|-------------|------------|
| G1 + Dex3 hands | `Unitree_G1_Dex3` | `G1_29` or `G1_23` | `dex3` |
| G1 + Dex1 grippers | `Unitree_G1_Dex1` | `G1_29` or `G1_23` | `dex1` |
| G1 + BrainCo hands | `Unitree_G1_Brainco` | `G1_29` or `G1_23` | `brainco` |
| G1 + Inspire hands | `Unitree_G1_Inspire` | `G1_29` or `G1_23` | `inspire1` |
| Z1 single arm | `Unitree_Z1_Single` | N/A | N/A |
| Z1 dual arms | `Unitree_Z1_Dual` | N/A | N/A |
| IsaacLab sim | `Unitree_G1_Dex1_Sim` | `G1_29` | `dex1` |

**Notes:**
- `G1_29` = 29 DOF version (newer)
- `G1_23` = 23 DOF version (older)
- Robot type is for data conversion
- Arm/EE are for deployment

---

## 📁 File Structure Quick Reference

```
Important files you'll modify:
├── unitree_lerobot/utils/
│   └── constants.py              ← Add new robot configs here
├── unitree_lerobot/eval_robot/
│   ├── eval_g1.py                ← Modify for custom deployment
│   └── make_robot.py             ← Add new robot controllers
└── test/
    └── test_*.py                 ← Add tests here

Important files you'll read:
├── README.md                     ← Main documentation
├── WORKSPACE_ANALYSIS.md         ← High-level overview
├── TECHNICAL_DEEP_DIVE.md        ← Architecture details
└── unitree_lerobot/lerobot/      ← LeRobot submodule (training)
```

---

## 🔧 Common Configuration Parameters

### Data Conversion
```python
--raw-dir           # Input: Your JSON dataset directory
--repo-id           # Output: HuggingFace repo (e.g., "user/task")
--robot_type        # Robot configuration (see cheat sheet)
--push_to_hub       # true/false: Upload to HuggingFace
```

### Training
```python
--dataset.repo_id   # Dataset to train on
--policy.type       # act, diffusion, pi0, pi05, groot
--policy.push_to_hub  # true/false: Upload trained model
--output_dir        # Where to save checkpoints
--job_name          # Experiment name
```

### Deployment
```python
--policy.path       # Path to trained model checkpoint
--repo_id           # Dataset repo (for stats/normalization)
--arm               # G1_29, G1_23
--ee                # dex3, dex1, inspire1, brainco
--frequency         # Control frequency (Hz), default 30
--episodes          # Number of rollouts, 0=infinite
--visualization     # true/false: Enable Rerun 3D viz
--send_real_robot   # true/false: Actually send commands
```

---

## 🐛 Troubleshooting Quick Fixes

### Issue: "401 Client Error: Unauthorized"
```bash
huggingface-cli login
# Enter your HuggingFace token
```

### Issue: "Unknown encoder 'libsvtav1'" or FFmpeg errors
```bash
conda install -c conda-forge ffmpeg=7.1.1
```

### Issue: "Access to model google/paligemma-3b-pt-224 is restricted"
```bash
huggingface-cli login
# Request access at https://huggingface.co/google/paligemma-3b-pt-224
```

### Issue: Dataset not found locally
```bash
# LeRobot caches datasets here:
ls ~/.cache/huggingface/lerobot/

# Force re-download:
rm -rf ~/.cache/huggingface/lerobot/<repo_id>
```

### Issue: Robot not responding
```bash
# Check robot is on network
ping <robot_ip>

# Verify image server running on robot
# (See avp_teleoperate docs)

# Check SDK installation
python -c "import unitree_sdk2py; print('SDK OK')"
```

### Issue: Training OOM (Out of Memory)
```bash
# Reduce batch size in training config
--training.batch_size=8  # or smaller

# Enable gradient checkpointing (Pi05/Groot)
--policy.gradient_checkpointing=true

# Use smaller policy variant
--policy.type=act  # Instead of diffusion
```

---

## 📊 Performance Benchmarks

### Training Time (on A100 GPU)
| Policy | 100k steps | GPU Memory |
|--------|-----------|------------|
| ACT | ~8 hours | 24 GB |
| Diffusion | ~12 hours | 32 GB |
| Pi0 | ~16 hours | 40 GB |
| Pi05 | ~24 hours | 48 GB |

### Inference Speed (on RTX 3090)
| Policy | FPS | Latency |
|--------|-----|---------|
| ACT | 50 Hz | 20ms |
| Diffusion | 30 Hz | 33ms |
| Pi0 | 25 Hz | 40ms |
| Pi05 | 20 Hz | 50ms |

### Dataset Size Guidelines
| Episodes | Frames | Disk Space | Training Time |
|----------|--------|------------|---------------|
| 10 | 2,500 | 5 GB | 2 hours |
| 50 | 12,500 | 25 GB | 8 hours |
| 100 | 25,000 | 50 GB | 16 hours |
| 500 | 125,000 | 250 GB | 80 hours |

---

## 🎯 Policy Selection Guide

### Choose ACT if...
- ✅ You have limited compute (< 24 GB GPU)
- ✅ You need fast training
- ✅ Your task is relatively simple (pick and place)
- ✅ You have 10-50 episodes

### Choose Diffusion if...
- ✅ You have sufficient compute (32 GB+ GPU)
- ✅ Your task requires smooth motions
- ✅ You have 50-100+ episodes
- ✅ You can wait longer for training

### Choose Pi0/Pi05 if...
- ✅ You want language-conditioned policies
- ✅ You have pretrained checkpoints
- ✅ You have very large compute (48 GB+ GPU)
- ✅ You want state-of-the-art performance

### Choose Groot if...
- ✅ You want to use NVIDIA's foundation model
- ✅ You have access to pretrained weights
- ✅ You have 48 GB+ GPU
- ✅ You're doing research

---

## 📚 Essential Reading

1. **Before you start:** `README.md`
2. **Understanding the system:** `WORKSPACE_ANALYSIS.md`
3. **Going deeper:** `TECHNICAL_DEEP_DIVE.md`
4. **LeRobot docs:** https://github.com/huggingface/lerobot/tree/main/docs
5. **ACT paper:** https://arxiv.org/abs/2304.13705
6. **Diffusion Policy paper:** https://arxiv.org/abs/2303.04137

---

## 🧪 Testing Your Setup

### Test 1: Environment
```bash
python -c "
import torch
import transformers
import lerobot
print('✅ All imports OK')
print(f'PyTorch: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
"
```

### Test 2: Dataset Loading
```bash
python test/test_load_dataset.py
```

### Test 3: Data Conversion
```bash
# Use example data (if available)
python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
    --raw-dir examples/sample_data \
    --repo-id test/debug \
    --robot_type Unitree_G1_Dex3
```

---

## 🔗 Important Links

| Resource | URL |
|----------|-----|
| **This Repo** | https://github.com/karim7tr/unitree_IL_lerobot |
| **Original Repo** | https://github.com/unitreerobotics/unitree_IL_lerobot |
| **Datasets** | https://huggingface.co/unitreerobotics |
| **Teleoperation** | https://github.com/unitreerobotics/avp_teleoperate |
| **Simulation** | https://github.com/unitreerobotics/unitree_sim_isaaclab |
| **LeRobot** | https://github.com/huggingface/lerobot |
| **Unitree SDK** | https://github.com/unitreerobotics/unitree_sdk2_python |
| **Discord** | https://discord.gg/ZwcVwxv5rq |

---

## 💡 Pro Tips

### Tip 1: Start with Simulation
Before deploying on real hardware, always test in `unitree_sim_isaaclab`. It's free, safe, and fast.

### Tip 2: Use Pretrained Models
Don't train from scratch if you don't have to:
```bash
# Load pretrained policy
--policy.pretrained_path=unitreerobotics/some_checkpoint
```

### Tip 3: Visualize Everything
Always use `--visualization=true` during deployment to debug issues.

### Tip 4: Record Diverse Data
- Vary starting positions
- Include failure cases
- Multiple backgrounds
- Different lighting conditions

### Tip 5: Monitor Training
```bash
# Use tensorboard
tensorboard --logdir unitree_lerobot/lerobot/outputs/

# Watch training loss, it should decrease smoothly
```

### Tip 6: Version Control Your Datasets
```bash
# Push to HuggingFace Hub with version tags
--repo-id=user/task
# Then tag versions: v1.0, v1.1, etc.
```

### Tip 7: Safety First
```python
# Always start with:
--send_real_robot=false  # Dry run mode
--visualization=true      # Watch predictions

# Then enable robot commands once verified
--send_real_robot=true
```

---

## 🎓 Learning Path

### Beginner (Week 1)
1. ✅ Install environment
2. ✅ Load demo dataset
3. ✅ Visualize dataset
4. ✅ Understand data format

### Intermediate (Week 2-3)
1. ✅ Collect own data (with avp_teleoperate)
2. ✅ Convert to LeRobot format
3. ✅ Train ACT policy
4. ✅ Evaluate on dataset

### Advanced (Week 4+)
1. ✅ Deploy on real robot
2. ✅ Try different policies
3. ✅ Add custom robot config
4. ✅ Modify controllers

---

## 📞 Getting Help

1. **Check README first:** Most questions answered there
2. **Search Issues:** https://github.com/unitreerobotics/unitree_IL_lerobot/issues
3. **Discord:** https://discord.gg/ZwcVwxv5rq
4. **Open Issue:** If bug or feature request
5. **Read LeRobot docs:** Many questions are LeRobot-specific

---

## ✅ Pre-Flight Checklist

Before deploying on real robot:

- [ ] Tested in simulation
- [ ] Verified dataset quality
- [ ] Reviewed training curves (smooth decrease)
- [ ] Tested with `--send_real_robot=false` first
- [ ] Checked joint limits in code
- [ ] Set appropriate frequency (start with 10 Hz)
- [ ] Have emergency stop ready (Ctrl+C works)
- [ ] Cleared robot workspace
- [ ] Standing by to intervene

---

## 🎬 Example Session

```bash
# Complete workflow from data to deployment

# 1. Activate environment
conda activate unitree_lerobot

# 2. Convert data
python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
    --raw-dir $HOME/datasets/pick_apple \
    --repo-id myname/pick_apple \
    --robot_type Unitree_G1_Dex3 \
    --push_to_hub

# 3. Train policy
cd unitree_lerobot/lerobot
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=myname/pick_apple \
    --policy.type=act \
    --job_name=apple_act_v1

# 4. Test in simulation
cd ../..
python unitree_lerobot/eval_robot/eval_g1_sim.py \
    --policy.path=unitree_lerobot/lerobot/outputs/.../pretrained_model \
    --repo_id=myname/pick_apple \
    --arm="G1_29" \
    --ee="dex3" \
    --episodes=10

# 5. Deploy on real robot (if sim looks good)
python unitree_lerobot/eval_robot/eval_g1.py \
    --policy.path=unitree_lerobot/lerobot/outputs/.../pretrained_model \
    --repo_id=myname/pick_apple \
    --arm="G1_29" \
    --ee="dex3" \
    --frequency=20 \
    --visualization=true
```

---

## 🏁 Summary

This quick reference covers 90% of common use cases. For deeper understanding:
- Read `WORKSPACE_ANALYSIS.md` for high-level overview
- Read `TECHNICAL_DEEP_DIVE.md` for architecture details
- Read LeRobot docs for training specifics
- Join Discord for community support

**Remember:** Start simple (demo dataset + ACT + simulation) before moving to complex setups.

---

**Last Updated:** 2026-01-08  
**Version:** 0.3.0 compatible
