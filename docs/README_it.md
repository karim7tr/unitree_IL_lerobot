<div align="center">
  <h1 align="center"> unitree_IL_lerobot </h1>
  <h3 align="center"> Unitree Robotics </h3>
  <p align="center">
    <a href="../README.md"> English </a> | <a href="./README_it.md"> Italiano </a> | <a href="./README_fr.md"> Français </a>
  </p>
    <p align="center">
     <a href="https://discord.gg/ZwcVwxv5rq" target="_blank"><img src="https://img.shields.io/badge/-Discord-5865F2?style=flat&logo=Discord&logoColor=white" alt="Unitree LOGO"></a>
  </p>
</div>

| Repository Unitree Robotics                         | link                                                                               |
| -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Dataset Unitree                                     | [dataset unitree](https://huggingface.co/unitreerobotics)                          |
| AVP Teleoperate                                    | [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate)              |
| Unitree Sim IsaacLab                               | [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab)    |
| Simulazione MuJoCo (NUOVO)                         | Vedi [MUJOCO_SIMULATION_GUIDE.md](../MUJOCO_SIMULATION_GUIDE.md)                   |
| Conversione varie versioni dataset lerobot        | [any4lerobot](https://github.com/Tavish9/any4lerobot/tree/main/ds_version_convert) |

# 📚 Documentazione

**NUOVO: Documentazione completa del workspace disponibile!**

| Documento | Descrizione | Tempo di lettura |
|----------|-------------|------------------|
| [ANALYSIS_SUMMARY.md](../ANALYSIS_SUMMARY.md) | Panoramica esecutiva, controlli, avvio rapido | 5 min |
| [WORKSPACE_ANALYSIS.md](../WORKSPACE_ANALYSIS.md) | Struttura repository, funzionalità, 11 configurazioni robot | 15 min |
| [TECHNICAL_DEEP_DIVE.md](../TECHNICAL_DEEP_DIVE.md) | Architettura sistema, flussi dati, benchmark | 30 min |
| [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) | Comandi, configurazioni, risoluzione problemi | Riferimento |
| [MUJOCO_SIMULATION_GUIDE.md](../MUJOCO_SIMULATION_GUIDE.md) | Configurazione simulazione MuJoCo (CPU-friendly) | 20 min |

# 🔖 Note di Rilascio

### 🏷️ v0.4 (NUOVO)

1. **Supporto Simulazione MuJoCo** - Alternativa CPU-friendly a IsaacLab
   - Script di valutazione standalone con correzioni di stabilità
   - Previene caduta robot e movimento casuale giunti
   - Guadagni PD configurabili e compensazione gravità
   - Nessuna GPU richiesta - funziona su CPU

2. **Documentazione Completa**
   - Analisi workspace e approfondimento architettura
   - Guida di riferimento rapido con risoluzione problemi
   - Supporto multilingua (EN/IT/FR/ZH)

### 🏷️ v0.3

1. Aggiornamento [`lerobot dataset v3.0`](https://github.com/huggingface/lerobot/blob/main/docs/source/porting_datasets_v3.mdx).

2. Maggior supporto policy ([`pi05`](https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies/pi05), [`groot`](https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies/groot)).

### 🏷️ v0.2

1. Aggiunta `conversione dati` e `distribuzione modelli` per mani destrose `brainco` e `inspire1`.

2. Aggiunta funzionalità di `replay del dataset robot`.

3. Aggiunta `verifica ambiente simulazione` [unitree_sim_isaaclab].

### 🏷️ v0.1

Supporto `conversione dati`, `distribuzione modelli` e `test nel mondo reale` per `G1 + Dex1 + Dex3`.

# 0. 📖 Introduzione

Questo repository fornisce una **pipeline completa di apprendimento per imitazione** per robot umanoidi Unitree (G1, Z1) usando il framework [LeRobot](https://github.com/huggingface/lerobot). Addestra i robot tramite dimostrazione - dalla raccolta dati alla distribuzione nel mondo reale.

**Caratteristiche Principali:**
- ✅ Conversione dati (JSON → formato LeRobot)
- ✅ Addestramento con policy multiple (ACT, Diffusion, Pi0, Pi05, Groot)
- ✅ Controllo robot in tempo reale (30 Hz)
- ✅ Due opzioni di simulazione: IsaacLab (GPU) o MuJoCo (CPU)
- ✅ 11 configurazioni robot supportate

`❗Suggerimento: Se hai domande, idee o suggerimenti da realizzare, sentiti libero di sollevarli in qualsiasi momento. Faremo del nostro meglio per risolverli e implementarli.`

## 🗂️ Struttura Repository

| Directory  | Descrizione                                                                                              |
| ---------- | -------------------------------------------------------------------------------------------------------- |
| `lerobot/` | Repository LeRobot per addestramento (submodule, commit: `0878c68`) |
| `utils/` | Strumenti elaborazione dati Unitree (conversione, ordinamento) |
| `eval_robot/` | Script distribuzione e valutazione robot |
| `test/` | Suite di test per caricamento e conversione dataset |
| `docs/` | Documentazione multilingua |

# 1. 📦 Configurazione Ambiente

## 1.1 🦾 Configurazione Ambiente LeRobot

Installa il framework [LeRobot](https://github.com/huggingface/lerobot) e le dipendenze:

```bash
# Clona con submodule
git clone --recurse-submodules https://github.com/karim7tr/unitree_IL_lerobot.git
cd unitree_IL_lerobot

# Se già clonato, aggiorna submodule
git submodule update --init --recursive

# Crea ambiente conda
conda create -y -n unitree_lerobot python=3.10
conda activate unitree_lerobot

# Installa dipendenze
conda install pinocchio -c conda-forge
conda install ffmpeg=7.1.1 -c conda-forge

# Installa LeRobot
cd unitree_lerobot/lerobot && pip install -e .

# Installa unitree_lerobot
cd ../../ && pip install -e .
```

## 1.2 🕹️ unitree_sdk2_python (Per Robot Reale)

Per comunicazione DDS con robot Unitree:

```bash
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
cd unitree_sdk2_python && pip install -e .
```

## 1.3 🎮 Configurazione Simulazione

### Opzione A: IsaacLab (GPU Richiesta)

Per simulazione ad alte prestazioni con GPU:

```bash
# Segui istruzioni su:
# https://github.com/unitreerobotics/unitree_sim_isaaclab
```

**Requisiti:** GPU NVIDIA con 8GB+ VRAM, supporto CUDA

### Opzione B: MuJoCo (CPU-Friendly) ⭐ NUOVO

Per simulazione leggera senza GPU:

```bash
pip install mujoco
```

**Nessuna GPU richiesta!** Vedi [MUJOCO_SIMULATION_GUIDE.md](../MUJOCO_SIMULATION_GUIDE.md) per configurazione completa.

# 2. ⚙️ Raccolta e Conversione Dati

## 2.1 🖼️ Carica Dataset Esistenti

Carica dataset pre-registrati da Hugging Face:

```python
from lerobot.datasets.lerobot_dataset import LeRobotDataset

# Carica dataset
dataset = LeRobotDataset(repo_id="unitreerobotics/G1_Dex3_ToastedBread_Dataset")

# Accedi episodio
episode_index = 0
from_idx = dataset.meta.episodes["dataset_from_index"][episode_index]
to_idx = dataset.meta.episodes["dataset_to_index"][episode_index]

for step_idx in range(from_idx, to_idx):
    step = dataset[step_idx]
```

**Visualizzazione:**

```bash
cd unitree_lerobot/lerobot
python src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id unitreerobotics/G1_Dex3_ToastedBread_Dataset \
    --episode-index 0
```

## 2.2 🔨 Raccolta Dati

Raccogli i tuoi dati usando [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate/tree/g1) con robot Unitree G1.

**Formato output:**
```
datasets/
└── nome_task/
    ├── episode_0001/
    │   ├── audios/
    │   ├── colors/
    │   ├── depths/
    │   └── data.json
    ├── episode_0002/
    └── ...
```

## 2.3 🛠️ Conversione Dati

### Passo 1: Ordina e Rinomina

Assicura denominazione episodi sequenziale:

```bash
python unitree_lerobot/utils/sort_and_rename_folders.py \
    --data_dir $HOME/datasets/nome_task
```

### Passo 2: Converti in Formato LeRobot

```bash
python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
    --raw-dir $HOME/datasets/nome_task \
    --repo-id tuo_nome/nome_task \
    --robot_type Unitree_G1_Dex3 \
    --push_to_hub
```

**Tipi robot supportati:**
- `Unitree_Z1_Single`, `Unitree_Z1_Dual`
- `Unitree_G1_Dex1`, `Unitree_G1_Dex3`
- `Unitree_G1_Brainco`, `Unitree_G1_Inspire`
- `Unitree_G1_Dex1_Sim` (per IsaacLab)
- E altre 4 configurazioni mobili/sollevamento

# 3. 🚀 Addestramento

Addestra policy usando LeRobot. Vedi [documentazione ufficiale LeRobot](https://github.com/huggingface/lerobot/tree/main/docs/source) per dettagli.

## 3.1 Policy ACT (Veloce, Buona Base)

```bash
cd unitree_lerobot/lerobot

python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=tuo_nome/nome_task \
    --policy.type=act \
    --policy.push_to_hub=false
```

## 3.2 Policy Diffusion (Prestazioni Migliori)

```bash
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=tuo_nome/nome_task \
    --policy.type=diffusion \
    --policy.push_to_hub=false
```

## 3.3 Policy MuJoCo ⭐ NUOVO

Testa con simulazione MuJoCo CPU-friendly:

```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=tuo_nome/nome_task \
    --frequency=30 \
    --kp_arm=100.0 \
    --kd_arm=10.0 \
    --use_gravity_compensation=true \
    --visualization=true
```

**Perché MuJoCo?**
- ✅ Nessuna GPU richiesta (funziona su CPU)
- ✅ Installazione semplice (`pip install mujoco`)
- ✅ Fisica stabile con guadagni PD configurabili
- ✅ Previene caduta robot e movimento casuale

Vedi [MUJOCO_SIMULATION_GUIDE.md](../MUJOCO_SIMULATION_GUIDE.md) per risoluzione problemi.

# 4. 🤖 Distribuzione e Valutazione

## 4.1 Distribuzione Robot Reale

Distribuisci policy addestrata su Unitree G1 fisico:

```bash
# Prima avvia server immagini (vedi documentazione avp_teleoperate)

python unitree_lerobot/eval_robot/eval_g1.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=tuo_nome/nome_task \
    --arm="G1_29" \
    --ee="dex3" \
    --frequency=30 \
    --visualization=true \
    --send_real_robot=true
```

## 4.2 Simulazione IsaacLab

Testa in simulazione GPU ad alta fedeltà:

```bash
python unitree_lerobot/eval_robot/eval_g1_sim.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=tuo_nome/nome_task \
    --arm="G1_29" \
    --ee="dex3" \
    --frequency=30 \
    --visualization=true
```

# 5. 🔧 Riferimento Configurazione

## Tipi Robot

| Tipo | Braccia | End-Effector | DOF | Caso d'uso |
|------|---------|--------------|-----|------------|
| `Unitree_Z1_Single` | Singola | Pinza | 7 | Manipolazione desktop |
| `Unitree_Z1_Dual` | Doppia | Pinza | 14 | Compiti bimanuali |
| `Unitree_G1_Dex1` | Doppia | Pinza 1-DOF | 16 | Presa semplice |
| `Unitree_G1_Dex3` | Doppia | Mano 7-DOF | 28 | Manipolazione destrezza |
| `Unitree_G1_Brainco` | Doppia | Mano BrainCo | 26 | Ricerca protesica |
| `Unitree_G1_Inspire` | Doppia | Mano Inspire1 | 26 | Presa avanzata |

## Parametri Comuni

| Parametro | Predefinito | Descrizione |
|-----------|-------------|-------------|
| `--arm` | `G1_29` | Versione robot (`G1_29` o `G1_23`) |
| `--ee` | `dex3` | End-effector (`dex3`, `dex1`, `inspire1`, `brainco`) |
| `--frequency` | 30 | Frequenza controllo (Hz) |
| `--episodes` | 0 | Numero episodi (0 = infinito) |
| `--visualization` | true | Abilita visualizzazione 3D |

# 6. 🤔 Risoluzione Problemi

| Problema | Soluzione |
|---------|-----------|
| **401 Non Autorizzato (HuggingFace)** | Esegui `huggingface-cli login` |
| **Errori FFmpeg** | `conda install -c conda-forge ffmpeg=7.1.1` |
| **Robot cade in MuJoCo** | Aumenta `--kp_leg` e abilita `--use_gravity_compensation` |
| **Movimento giunti casuale** | Abbassa `--kp_arm`, aumenta `--kd_arm`, riduci `--max_joint_velocity` |
| **Addestramento lento** | Riduci `--training.batch_size` o usa policy più piccola |
| **GPU memoria esaurita** | Abilita `--policy.gradient_checkpointing=true` |

Vedi [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) per ulteriore risoluzione problemi.

# 7. 📖 Risorse di Apprendimento

## Iniziare (Principiante)

1. Leggi [ANALYSIS_SUMMARY.md](../ANALYSIS_SUMMARY.md) - Panoramica
2. Carica dataset demo (sezione 2.1)
3. Visualizza dataset
4. Esegui simulazione MuJoCo con modello pre-addestrato

## Intermedio

1. Raccogli dati propri con `avp_teleoperate`
2. Converti in formato LeRobot
3. Addestra policy ACT
4. Valuta in simulazione

## Avanzato

1. Distribuisci su robot reale
2. Prova policy diverse (Diffusion, Pi0, Groot)
3. Aggiungi configurazione robot personalizzata
4. Modifica controller per il tuo hardware

# 8. 🎬 Esempio Workflow Completo

```bash
# 1. Configura ambiente
conda create -y -n unitree_lerobot python=3.10
conda activate unitree_lerobot
# ... (vedi sezione 1.1)

# 2. Converti i tuoi dati
python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
    --raw-dir $HOME/datasets/raccogli_mela \
    --repo-id mionome/raccogli_mela \
    --robot_type Unitree_G1_Dex3 \
    --push_to_hub

# 3. Addestra policy
cd unitree_lerobot/lerobot
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=mionome/raccogli_mela \
    --policy.type=act

# 4. Testa in simulazione MuJoCo (nessuna GPU necessaria!)
cd ../..
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=unitree_lerobot/lerobot/outputs/.../pretrained_model \
    --repo_id=mionome/raccogli_mela \
    --frequency=30

# 5. Distribuisci su robot reale
python unitree_lerobot/eval_robot/eval_g1.py \
    --policy.path=unitree_lerobot/lerobot/outputs/.../pretrained_model \
    --repo_id=mionome/raccogli_mela \
    --arm="G1_29" \
    --ee="dex3"
```

# 9. 🙏 Ringraziamenti

Questo codice si basa su questi eccellenti progetti open-source:

1. [LeRobot](https://github.com/huggingface/lerobot) - Framework addestramento
2. [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python) - Comunicazione robot
3. [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate) - Raccolta dati
4. [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab) - Simulazione
5. [MuJoCo](https://github.com/google-deepmind/mujoco) - Simulazione fisica

# 10. 📞 Supporto

- **Documentazione:** Controlla documentazione in questo repository
- **Issues:** [GitHub Issues](https://github.com/karim7tr/unitree_IL_lerobot/issues)
- **Discord:** [Comunità Unitree](https://discord.gg/ZwcVwxv5rq)
- **Dataset:** [HuggingFace Hub](https://huggingface.co/unitreerobotics)

# 11. 📄 Licenza

Apache License 2.0 - Vedi file [LICENSE](../LICENSE)

---

**Link Rapidi:**
- [README Inglese](../README.md) | [README Italiano](./README_it.md) | [README Francese](./README_fr.md)
- [Guida MuJoCo](../MUJOCO_SIMULATION_GUIDE.md) | [Riferimento Rapido](../QUICK_REFERENCE.md) | [Approfondimento Tecnico](../TECHNICAL_DEEP_DIVE.md)
