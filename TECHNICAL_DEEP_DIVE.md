# Unitree IL LeRobot - Technical Deep Dive

**Supplementary Technical Documentation**

---

## 🔍 System Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                     UNITREE IL LEROBOT SYSTEM                       │
└────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│  1. DATA COLLECTION │
└──────────┬──────────┘
           │
           │  ┌─────────────────────────────────────┐
           │  │ avp_teleoperate (External Tool)     │
           │  │ - VR/Keyboard teleoperation         │
           │  │ - Records JSON + Images             │
           └─▶│ Output: episode_XXXX/               │
              │   ├── data.json                     │
              │   └── colors/                       │
              └─────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│  2. DATA PREPROCESSING (utils/)                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  sort_and_rename_folders.py ───▶ Ensure episode_0, episode_1...    │
│                                                                      │
│  convert_unitree_json_to_lerobot.py ───▶ JSON → LeRobot format    │
│  │                                         │                        │
│  │  ┌────────────────────────────────┐   │                        │
│  └─▶│ JsonDataset Class              │───┘                        │
│     │ - Loads JSON files             │                            │
│     │ - Extracts states/actions      │                            │
│     │ - Processes camera images      │                            │
│     │ - Uses ROBOT_CONFIGS           │                            │
│     └────────────────────────────────┘                            │
│                     │                                              │
│                     ▼                                              │
│     ┌──────────────────────────────────────┐                      │
│     │ LeRobotDataset (HDF5/Parquet)        │                      │
│     │ - Standardized format                │                      │
│     │ - Metadata (episodes, stats)         │                      │
│     │ - Videos (encoded)                   │                      │
│     │ - Can push to HuggingFace Hub        │                      │
│     └──────────────────────────────────────┘                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│  3. TRAINING (lerobot/ submodule)                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  lerobot_train.py                                                   │
│         │                                                           │
│         ├─▶ Load LeRobotDataset                                    │
│         ├─▶ Initialize Policy (ACT/Diffusion/Pi0/Pi05/Groot)       │
│         ├─▶ Training Loop                                           │
│         │   └─▶ Observation → Action prediction                    │
│         └─▶ Save checkpoints                                        │
│                                                                      │
│  Output: pretrained_model/ (PyTorch checkpoint)                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│  4. DEPLOYMENT (eval_robot/)                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐      ┌──────────────────┐                   │
│  │ eval_g1.py       │      │ eval_g1_sim.py   │                   │
│  │ (Real Robot)     │      │ (IsaacLab Sim)   │                   │
│  └────────┬─────────┘      └────────┬─────────┘                   │
│           │                         │                              │
│           ├─────────────────────────┤                              │
│           │                                                         │
│           ▼                                                         │
│  ┌────────────────────────────────────────┐                       │
│  │ make_robot.py                          │                       │
│  │ ├─▶ setup_image_client()               │                       │
│  │ │   └─▶ ImageClient (shared memory)    │                       │
│  │ │                                       │                       │
│  │ ├─▶ setup_robot_interface()            │                       │
│  │ │   ├─▶ ArmController (G1_29/G1_23)    │                       │
│  │ │   ├─▶ ArmIK (Inverse Kinematics)     │                       │
│  │ │   └─▶ HandController                 │                       │
│  │ │       ├─ Dex3_1_Controller           │                       │
│  │ │       ├─ Dex1_1_Gripper_Controller   │                       │
│  │ │       ├─ Inspire_Controller          │                       │
│  │ │       └─ Brainco_Controller          │                       │
│  │ │                                       │                       │
│  │ └─▶ unitree_sdk2_python (DDS comms)    │                       │
│  └────────────────────────────────────────┘                       │
│           │                                                         │
│           ▼                                                         │
│  ┌────────────────────────────────────────┐                       │
│  │ Policy Inference Loop                  │                       │
│  │ 1. Get camera images                   │                       │
│  │ 2. Get robot state                     │                       │
│  │ 3. Predict action                      │                       │
│  │ 4. Send to robot                       │                       │
│  │ 5. (Optional) Visualize with Rerun     │                       │
│  └────────────────────────────────────────┘                       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📐 Data Flow: JSON to LeRobot

```
Unitree JSON Format                    LeRobot Format
─────────────────────                  ──────────────

episode_0001/                          parquet files:
├── data.json ──────────┐             ├── data/
│   {                   │             │   ├── chunk-000/
│     "data": [         │             │   │   └── data.parquet
│       {               │  Transform  │   └── ...
│         "states": {   │──────────▶  ├── meta/
│           "left_arm": │             │   └── info.json
│           "right_arm" │             └── videos/
│           "left_ee"   │                 ├── observation.images.cam_left_high/
│           ...         │                 ├── observation.images.cam_right_high/
│         },            │                 └── ...
│         "actions": {  │
│           ...         │             HDF5 structure (alternative):
│         },            │             ├── action [N x action_dim]
│         "colors": {   │             ├── observation.state [N x state_dim]
│           "color_0"   │             ├── observation.images.cam_* [N x H x W x C]
│           ...         │             └── episode metadata
│       }               │
│     ]                 │
│   }                   │
├── colors/ ────────────┘
│   ├── color_0_XXXX.jpg
│   └── ...
```

**Key Transformations:**
1. **State aggregation**: Combines left_arm, right_arm, end-effectors into single vector
2. **Image mapping**: color_0 → cam_left_high (via camera_to_image_key)
3. **Temporal alignment**: Ensures states/actions/images are synchronized
4. **Video encoding**: Converts image sequences to video for efficiency
5. **Normalization**: Computes statistics for policy training

---

## 🤖 Robot Configuration Details

### State vs Action Dimensions

Different robot configurations have different state/action spaces:

```python
# Example: Unitree_G1_Dex3
State = [
    left_arm.qpos,      # 7 DOF (shoulder pitch/roll/yaw, elbow, wrist roll/pitch/yaw)
    right_arm.qpos,     # 7 DOF
    left_ee.qpos,       # 7 DOF (Dex3 hand joints)
    right_ee.qpos,      # 7 DOF
]  # Total: 28 DOF

Action = Same structure (28 DOF)

# Example: Unitree_G1_MoveibleLift_Dex1_UseWaist
State = [
    left_arm.qpos,      # 7 DOF
    right_arm.qpos,     # 7 DOF
    waist.qpos,         # 2 DOF (yaw, pitch)
    torso.height,       # 1 DOF (scalar)
    chassis.qvel,       # 2 DOF (x velocity, yaw rate)
    left_ee.qpos,       # 1 DOF (gripper)
    right_ee.qpos,      # 1 DOF (gripper)
]  # Total: 21 DOF

Action = [
    left_arm.qpos,      # 7 DOF
    right_arm.qpos,     # 7 DOF
    waist.qpos,         # 2 DOF
    torso.qvel,         # 1 DOF (velocity command)
    chassis.qvel,       # 2 DOF
    left_ee.qpos,       # 1 DOF
    right_ee.qpos,      # 1 DOF
]  # Total: 21 DOF
```

Note: Some configurations have **different state and action spaces** (e.g., torso uses position in state but velocity in action).

---

## 🎥 Camera Configuration

### Standard Setup (Unitree_G1_Dex3)
```
┌──────────────────────────────────────────────────┐
│                    Robot G1                      │
│                                                  │
│     ┌─────┐           ┌─────┐                   │
│     │Cam  │           │Cam  │                   │
│     │Left │           │Right│                   │
│     │High │           │High │                   │
│     └─────┘           └─────┘                   │
│         │                 │                      │
│         └────────┬────────┘                      │
│                  │                               │
│             [Binocular                           │
│              Head Camera]                        │
│                                                  │
│         ┌───────┴───────┐                        │
│         │               │                        │
│    ┌────▼────┐    ┌────▼────┐                   │
│    │ Left    │    │ Right   │                   │
│    │ Arm     │    │ Arm     │                   │
│    └────┬────┘    └────┬────┘                   │
│         │               │                        │
│    ┌────▼────┐    ┌────▼────┐                   │
│    │ Wrist   │    │ Wrist   │                   │
│    │ Cam     │    │ Cam     │                   │
│    └─────────┘    └─────────┘                   │
│                                                  │
│    Total: 4 cameras (2 head + 2 wrist)          │
│    Resolution: 480x1280 (head), 480x640 (wrist) │
└──────────────────────────────────────────────────┘
```

### Simulation Setup (Unitree_G1_Dex1_Sim)
```
┌──────────────────────────────────────────────────┐
│              IsaacLab Simulation                 │
│                                                  │
│         ┌─────┐                                  │
│         │Cam  │                                  │
│         │Left │                                  │
│         │High │                                  │
│         └─────┘                                  │
│             │                                    │
│      [Single Head Camera]                       │
│                                                  │
│         ┌───────┴───────┐                        │
│         │               │                        │
│    ┌────▼────┐    ┌────▼────┐                   │
│    │ Wrist   │    │ Wrist   │                   │
│    │ Cam     │    │ Cam     │                   │
│    └─────────┘    └─────────┘                   │
│                                                  │
│    Total: 3 cameras (1 head + 2 wrist)          │
└──────────────────────────────────────────────────┘
```

---

## 🔄 Policy Inference Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│                   Real-Time Control Loop                      │
└──────────────────────────────────────────────────────────────┘

Step 1: Image Acquisition
┌────────────────────────────────┐
│ ImageClient (Shared Memory)    │
│ ↓                              │
│ TV Camera (numpy array)        │◀─── Image Server Process
│ Wrist Cameras (numpy arrays)   │     (running on robot)
└────────────────────────────────┘
          │
          ▼
Step 2: State Reading
┌────────────────────────────────┐
│ ArmController.read_state()     │
│ ↓                              │
│ Joint positions (qpos)         │◀─── unitree_sdk2_python
│ Joint velocities (qvel)        │     (DDS communication)
└────────────────────────────────┘
          │
          ▼
Step 3: Preprocessing
┌────────────────────────────────┐
│ preprocessor(observation)      │
│ - Normalize images             │
│ - Normalize state              │
│ - Create proper tensor format  │
└────────────────────────────────┘
          │
          ▼
Step 4: Policy Forward Pass
┌────────────────────────────────┐
│ policy.forward(obs)            │
│ - ACT: Transformer + CVAE      │
│ - Diffusion: UNet denoising    │
│ - Pi0/Pi05: Vision-Language    │
│ ↓                              │
│ Raw action tensor              │
└────────────────────────────────┘
          │
          ▼
Step 5: Postprocessing
┌────────────────────────────────┐
│ postprocessor(action)          │
│ - Denormalize action           │
│ - Optional: Action filtering   │
└────────────────────────────────┘
          │
          ▼
Step 6: Robot Command
┌────────────────────────────────┐
│ Split action vector:           │
│ - arm_action → ArmController   │
│ - ee_action → HandController   │
│ ↓                              │
│ arm_ctrl.send_target()         │◀─── unitree_sdk2_python
│ ee_ctrl.send_target()          │     (DDS publish)
└────────────────────────────────┘

Frequency: 30 Hz (default)
Latency: ~33ms per cycle
```

---

## 🧠 Supported Policy Architectures

### 1. ACT (Action Chunking Transformer)
```
Input: Stacked images + robot state
       ↓
┌──────────────────────────┐
│ Vision Encoder (ResNet)  │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Transformer Encoder      │
│ (Process observations)   │
└──────────┬───────────────┘
           │
           ├───────────────────┐
           ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│ CVAE Encoder     │  │ CVAE Decoder     │
│ (Training only)  │  │ (Generate chunk) │
└──────────────────┘  └────────┬─────────┘
                              │
                              ▼
                  ┌─────────────────────────┐
                  │ Transformer Decoder     │
                  │ (Generate action chunk) │
                  └────────┬────────────────┘
                           │
                           ▼
                  Action Chunk [T x action_dim]
                  (Predict multiple timesteps)
```

### 2. Diffusion Policy
```
Input: Images + State + Noise
       ↓
┌──────────────────────────┐
│ Vision Encoder           │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Conditional UNet         │
│ - Iterative denoising    │
│ - Timestep embedding     │
└──────────┬───────────────┘
           │
           ▼ (multiple iterations)
    Clean Action Trajectory
    [T x action_dim]
```

### 3. Pi0/Pi05 (Vision-Language Models)
```
Input: Images + Language Task
       ↓
┌──────────────────────────┐
│ Vision Encoder           │
│ (e.g., CLIP)             │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Language Encoder         │
│ (Process task text)      │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Multimodal Transformer   │
│ (Cross-attention)        │
└──────────┬───────────────┘
           │
           ▼
    Action Prediction
```

---

## 🔧 Key Implementation Details

### 1. Shared Memory for Images
```python
# Image server (on robot) writes to shared memory
shm = shared_memory.SharedMemory(create=True, size=image_size)
shm.buf[:] = image_data

# Image client (policy process) reads from shared memory
shm = shared_memory.SharedMemory(name="cam_name")
image = np.ndarray(shape, dtype=dtype, buffer=shm.buf)
```

**Benefits:**
- Zero-copy data transfer
- Low latency (~1ms)
- Enables 30 Hz control loop

### 2. Action Filtering
```python
# Weighted moving filter to smooth actions
filtered_action = alpha * predicted_action + (1 - alpha) * prev_action
```

**Purpose:**
- Reduces jittery movements
- Prevents sudden jumps
- Improves safety

### 3. Inverse Kinematics (Optional)
```python
# Convert end-effector pose to joint angles
joint_angles = ik_solver.solve(target_pose)

# Fallback if IK fails
if not success:
    use_joint_space_action()
```

**Use case:** Some policies predict task-space actions instead of joint-space.

---

## 📊 Dataset Statistics Example

For `G1_Dex3_ToastedBread_Dataset`:
```yaml
total_episodes: 50
total_frames: 12,500
episode_length: 200-300 frames
fps: 30
duration: ~8 minutes total

action_space:
  dim: 28
  range: [-3.14, 3.14] (normalized)

state_space:
  dim: 28
  range: [-3.14, 3.14] (normalized)

cameras:
  - cam_left_high: 480x640 RGB
  - cam_right_high: 480x640 RGB
  - cam_left_wrist: 480x640 RGB
  - cam_right_wrist: 480x640 RGB

task: "Pick up bread and place in toaster"
```

---

## 🚀 Performance Characteristics

### Training
- **Hardware**: NVIDIA A100 (recommended)
- **Training time**: 
  - ACT: ~8 hours for 100k steps
  - Diffusion: ~12 hours for 100k steps
  - Pi05: ~24 hours (requires pretrained checkpoint)
- **Memory**: 24-40 GB GPU RAM
- **Batch size**: 8-32 (depends on policy)

### Inference
- **Latency**: 20-50ms per prediction
- **Throughput**: 20-50 Hz
- **Hardware**: RTX 3090 or better (robot compute)
- **Memory**: 8-12 GB GPU RAM

---

## 🔒 Security & Safety

### Pre-commit Hooks
- **Gitleaks**: Prevents committing secrets
- **Bandit**: Security vulnerability scanning
- **Ruff**: Code quality and style

### Robot Safety
- **Joint limits**: Enforced in controllers
- **Velocity limits**: Configurable per robot
- **Emergency stop**: User input to halt execution
- **Collision detection**: Not implemented (external system recommended)

---

## 🧪 Testing Strategy

Current test coverage:
```
test/
├── test_load_dataset.py      # Verify LeRobot dataset loading
├── test_load_h5.py            # Verify HDF5 conversion
└── test_local_push_to_hub.py  # Verify HuggingFace Hub upload
```

**Missing tests** (improvement opportunities):
- Unit tests for robot controllers
- Integration tests for eval pipeline
- Mock tests for image server
- Policy inference tests

---

## 📚 Dependencies Deep Dive

### Core ML Stack
```
PyTorch ─────┐
             │
transformers ├──▶ Policy implementations
             │    (ACT, Diffusion, etc.)
huggingface  │
             │
lerobot ─────┘    (Submodule)
```

### Robot Communication
```
unitree_sdk2_python
    ├─▶ cyclonedds (DDS middleware)
    ├─▶ numpy
    └─▶ Custom IDL definitions
```

### Visualization
```
rerun-sdk ──▶ 3D visualization
meshcat ───▶ Robot mesh rendering
opencv ────▶ Image processing
```

---

## 🎓 Learning Resources

To understand this codebase, study these topics in order:

1. **Imitation Learning basics**
   - Behavioral Cloning
   - State-action pairs
   - Generalization

2. **LeRobot framework**
   - Dataset format
   - Policy interface
   - Training pipeline

3. **Robot kinematics**
   - Forward/Inverse kinematics
   - Jacobians
   - Joint vs task space

4. **Vision-based control**
   - Camera calibration
   - Visual servoing
   - Multi-camera fusion

5. **Real-time systems**
   - Control loop timing
   - Latency management
   - Shared memory IPC

---

## 🔮 Future Directions

Based on TODO comments and v0.3 trajectory:

1. **More policies**: TDMPC, R3M, MVP
2. **Sim-to-real**: Better domain adaptation
3. **Multi-task learning**: Single policy for multiple tasks
4. **Active learning**: Online data collection
5. **Safety layers**: Learned constraints
6. **Mobile manipulation**: Full-body control with locomotion

---

## 📝 Contributing Guidelines

From `.pre-commit-config.yaml`:
- Python 3.10 only
- Ruff formatting (120 char lines)
- Type hints encouraged (mypy disabled currently)
- Google-style docstrings (not enforced yet)
- Security scans mandatory

---

## 🏁 Summary

This technical deep dive reveals a **production-grade, end-to-end robotic learning system** with:
- ✅ Complete data pipeline
- ✅ Multiple policy architectures
- ✅ Real-time robot control
- ✅ Comprehensive safety checks
- ✅ Active development and support

The architecture is **modular**, **well-documented**, and **extensible** for research and commercial applications.
