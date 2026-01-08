# MuJoCo Simulation Guide for Unitree G1

This guide helps you run unitree_IL_lerobot simulations using **MuJoCo** instead of IsaacLab. This is useful if you don't have access to high-end GPUs required for IsaacLab.

---

## Why MuJoCo Instead of IsaacLab?

**IsaacLab** requires:
- NVIDIA GPU with 8GB+ VRAM
- CUDA support
- Complex setup

**MuJoCo** provides:
- ✅ Runs on CPU or basic GPUs
- ✅ Simple installation (`pip install mujoco`)
- ✅ Fast physics simulation
- ✅ Built-in visualization

---

## Quick Start

### 1. Install MuJoCo

```bash
pip install mujoco
```

### 2. Verify Installation

```bash
# Test MuJoCo viewer
python -m mujoco.viewer

# Drag and drop this file to test:
# unitree_lerobot/eval_robot/assets/g1/g1_body29_hand14.xml
```

### 3. Run Evaluation

```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=path/to/pretrained_model \
    --repo_id=unitreerobotics/G1_Dex3_ToastedBread_Dataset \
    --frequency=30 \
    --visualization=true
```

---

## Fixing Common Issues

### Problem: Robot Falls Down

**Causes:**
1. PD gains too low (joints can't support weight)
2. No gravity compensation
3. Wrong initial pose

**Solutions:**

#### Solution 1: Increase PD Gains
```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --kp_arm=150.0 \
    --kd_arm=15.0 \
    --kp_leg=300.0 \
    --kd_leg=30.0 \
    ...
```

#### Solution 2: Enable Gravity Compensation (Default: ON)
```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --use_gravity_compensation=true \
    ...
```

#### Solution 3: Check Initial Pose
The robot starts from the first frame of your dataset. Make sure your dataset has stable initial poses.

### Problem: Joints Move Randomly

**Causes:**
1. PD gains too high (oscillation)
2. Control frequency mismatch
3. Joint velocity limits too high

**Solutions:**

#### Solution 1: Lower PD Gains
```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --kp_arm=80.0 \
    --kd_arm=8.0 \
    ...
```

#### Solution 2: Adjust Control Frequency
```bash
# Try lower frequency for more stable control
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --frequency=20 \
    ...
```

#### Solution 3: Reduce Max Joint Velocity
```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --max_joint_velocity=2.0 \
    ...
```

### Problem: Simulation Runs Too Slow

**Causes:**
1. Visualization overhead
2. Control frequency too high

**Solutions:**

#### Solution 1: Disable Visualization
```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --visualization=false \
    ...
```

#### Solution 2: Lower Control Frequency
```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --frequency=10 \
    ...
```

---

## Configuration Parameters

### Control Gains

| Parameter | Default | Description | Tuning Guide |
|-----------|---------|-------------|--------------|
| `kp_arm` | 100.0 | Position gain for arms | Too low → floppy joints<br>Too high → oscillation |
| `kd_arm` | 10.0 | Damping gain for arms | Too low → overshoot<br>Too high → sluggish |
| `kp_leg` | 200.0 | Position gain for legs (locked) | Higher = stiffer lock |
| `kd_leg` | 20.0 | Damping gain for legs | Higher = more damping |

### Safety

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_joint_velocity` | 3.0 rad/s | Maximum allowed joint velocity |
| `use_gravity_compensation` | true | Enable gravity compensation |

### Control

| Parameter | Default | Description |
|-----------|---------|-------------|
| `frequency` | 30 Hz | Control loop frequency |
| `episodes` | 0 | Number of episodes (0 = infinite) |

---

## Tuning Guide

### Step 1: Start Conservative

```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --kp_arm=80.0 \
    --kd_arm=8.0 \
    --frequency=20 \
    --max_joint_velocity=2.0 \
    --use_gravity_compensation=true \
    --visualization=true \
    ...
```

### Step 2: Observe Behavior

- **Robot droops/falls** → Increase `kp_arm` by 20-30
- **Robot shakes/oscillates** → Decrease `kp_arm` by 20-30, increase `kd_arm`
- **Movements too slow** → Increase `max_joint_velocity`
- **Movements too jerky** → Decrease `max_joint_velocity`, increase `kd_arm`

### Step 3: Fine-tune

Once stable, gradually:
1. Increase `frequency` to 30 Hz for smoother control
2. Adjust `kp_arm` and `kd_arm` for desired stiffness
3. Test with different datasets

### Step 4: Recommended Stable Settings

For most use cases:
```bash
--kp_arm=100.0 \
--kd_arm=10.0 \
--kp_leg=200.0 \
--kd_leg=20.0 \
--frequency=30 \
--max_joint_velocity=3.0 \
--use_gravity_compensation=true
```

---

## Advanced: Editing MuJoCo Model

If you need more control, you can edit the MuJoCo XML model directly:

```bash
# Location
unitree_lerobot/eval_robot/assets/g1/g1_body29_hand14.xml
```

### Adjust Joint Properties

Find joint definitions and modify:

```xml
<joint name="left_shoulder_pitch_joint" 
       pos="0 0 0" 
       axis="0 1 0" 
       range="-2.5307 2.8798"      <!-- Joint limits -->
       actuatorfrcrange="-88 88"   <!-- Force limits -->
       damping="0.5"                <!-- Add damping -->
       armature="0.01"/>            <!-- Add inertia -->
```

### Adjust Physics

Modify the `<option>` tag:

```xml
<option timestep="0.002"        <!-- Smaller = more accurate, slower -->
        gravity="0 0 -9.81"     <!-- Adjust gravity -->
        viscosity="0.0001"/>    <!-- Air resistance -->
```

### Adjust Solver

For more stable simulation:

```xml
<option>
  <flag gravity="enable"/>
</option>

<option>
  <solver iterations="50"       <!-- More = more accurate -->
          tolerance="1e-10"/>   <!-- Smaller = more accurate -->
</option>
```

---

## Comparison: IsaacLab vs MuJoCo

| Feature | IsaacLab | MuJoCo |
|---------|----------|--------|
| GPU Required | Yes (8GB+) | No |
| Installation | Complex | Simple |
| Physics Accuracy | Very High | High |
| Rendering | GPU | CPU/GPU |
| Speed (with GPU) | Very Fast | Fast |
| Speed (without GPU) | N/A | Moderate |
| Parallel Envs | Yes | No |
| Best For | Training, Large-scale eval | Testing, Development, Low-resource |

---

## Troubleshooting Checklist

- [ ] MuJoCo installed: `pip install mujoco`
- [ ] Model file exists: `unitree_lerobot/eval_robot/assets/g1/g1_body29_hand14.xml`
- [ ] Dataset accessible: Check `--repo_id`
- [ ] Policy checkpoint exists: Check `--policy.path`
- [ ] Started with recommended settings
- [ ] Gravity compensation enabled
- [ ] Joint limits not violated (check MuJoCo warnings)

---

## Example Workflows

### Workflow 1: Quick Test (No Training)

```bash
# Just visualize robot in MuJoCo
python -m mujoco.viewer
# Drag: unitree_lerobot/eval_robot/assets/g1/g1_body29_hand14.xml
```

### Workflow 2: Test Trained Policy

```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=your_username/your_dataset \
    --frequency=30 \
    --visualization=true
```

### Workflow 3: Headless Evaluation (Fast)

```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=your_username/your_dataset \
    --frequency=50 \
    --visualization=false \
    --episodes=100
```

---

## Known Limitations

1. **No camera rendering** (yet) - Images not captured during evaluation
2. **No parallel environments** - Single robot at a time
3. **No reward calculation** - Task success must be evaluated manually
4. **Limited robot types** - Currently only G1_29 with Dex3 hands

These will be addressed in future updates.

---

## Getting Help

If robot still falls or behaves incorrectly:

1. **Check MuJoCo warnings** - Run with verbose output
2. **Verify dataset** - Load first frame and check joint values
3. **Test without policy** - Lock joints to initial pose only
4. **Compare with IsaacLab** - If available, check for data issues

**Report issues:**
- GitHub: https://github.com/unitreerobotics/unitree_IL_lerobot/issues
- Discord: https://discord.gg/ZwcVwxv5rq

---

## Summary

**For stable MuJoCo simulation:**
1. ✅ Use recommended PD gains
2. ✅ Enable gravity compensation
3. ✅ Start with 20-30 Hz control frequency
4. ✅ Limit joint velocities
5. ✅ Use stable initial poses from dataset

**Key command:**
```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=YOUR_MODEL \
    --repo_id=YOUR_DATASET \
    --kp_arm=100 --kd_arm=10 \
    --frequency=30 \
    --use_gravity_compensation=true \
    --visualization=true
```

This should give you a stable, realistic MuJoCo simulation! 🚀
