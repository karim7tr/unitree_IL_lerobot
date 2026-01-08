<div align="center">
  <h1 align="center"> unitree_IL_lerobot </h1>
  <h3 align="center"> Unitree Robotics </h3>
  <p align="center">
    <a href="../README.md"> English </a> | <a href="./README_it.md"> Italiano </a> | <a href="./README_fr.md"> Français </a> | <a href="./README_zh.md"> 中文 </a>
  </p>
    <p align="center">
     <a href="https://discord.gg/ZwcVwxv5rq" target="_blank"><img src="https://img.shields.io/badge/-Discord-5865F2?style=flat&logo=Discord&logoColor=white" alt="Unitree LOGO"></a>
  </p>
</div>

| Dépôts Unitree Robotics                            | lien                                                                               |
| -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Ensembles de données Unitree                       | [unitree datasets](https://huggingface.co/unitreerobotics)                         |
| AVP Teleoperate                                    | [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate)              |
| Unitree Sim IsaacLab                               | [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab)    |
| Simulation MuJoCo (NOUVEAU)                        | Voir [MUJOCO_SIMULATION_GUIDE.md](../MUJOCO_SIMULATION_GUIDE.md)                   |
| Conversion diverses versions datasets lerobot     | [any4lerobot](https://github.com/Tavish9/any4lerobot/tree/main/ds_version_convert) |

# 📚 Documentation

**NOUVEAU : Documentation complète de l'espace de travail disponible !**

| Document | Description | Temps de lecture |
|----------|-------------|------------------|
| [ANALYSIS_SUMMARY.md](../ANALYSIS_SUMMARY.md) | Vue d'ensemble, contrôles santé, démarrage rapide | 5 min |
| [WORKSPACE_ANALYSIS.md](../WORKSPACE_ANALYSIS.md) | Structure dépôt, fonctionnalités, 11 configs robot | 15 min |
| [TECHNICAL_DEEP_DIVE.md](../TECHNICAL_DEEP_DIVE.md) | Architecture système, flux données, benchmarks | 30 min |
| [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) | Commandes, configurations, dépannage | Référence |
| [MUJOCO_SIMULATION_GUIDE.md](../MUJOCO_SIMULATION_GUIDE.md) | Configuration simulation MuJoCo (CPU-friendly) | 20 min |

# 🔖 Notes de Version

### 🏷️ v0.4 (NOUVEAU)

1. **Support Simulation MuJoCo** - Alternative CPU-friendly à IsaacLab
   - Script d'évaluation autonome avec corrections de stabilité
   - Empêche chute du robot et mouvement aléatoire des articulations
   - Gains PD configurables et compensation gravité
   - Aucun GPU requis - fonctionne sur CPU

2. **Documentation Complète**
   - Analyse workspace et approfondissement architecture
   - Guide référence rapide avec dépannage
   - Support multilingue (EN/IT/FR/ZH)

### 🏷️ v0.3

1. Mise à jour [`lerobot dataset v3.0`](https://github.com/huggingface/lerobot/blob/main/docs/source/porting_datasets_v3.mdx).

2. Plus de support politique ([`pi05`](https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies/pi05), [`groot`](https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies/groot)).

### 🏷️ v0.2

1. Ajout `conversion données` et `déploiement modèles` pour mains dextres `brainco` et `inspire1`.

2. Ajout fonctionnalité de `replay du dataset robot`.

3. Ajout `vérification environnement simulation` [unitree_sim_isaaclab].

### 🏷️ v0.1

Support `conversion données`, `déploiement modèles` et `tests dans le monde réel` pour `G1 + Dex1 + Dex3`.

# 0. 📖 Introduction

Ce dépôt fournit un **pipeline complet d'apprentissage par imitation** pour robots humanoïdes Unitree (G1, Z1) utilisant le framework [LeRobot](https://github.com/huggingface/lerobot). Formez les robots par démonstration - de la collecte de données au déploiement dans le monde réel.

**Caractéristiques Principales :**
- ✅ Conversion données (JSON → format LeRobot)
- ✅ Formation avec politiques multiples (ACT, Diffusion, Pi0, Pi05, Groot)
- ✅ Contrôle robot temps réel (30 Hz)
- ✅ Deux options simulation : IsaacLab (GPU) ou MuJoCo (CPU)
- ✅ 11 configurations robot supportées

`❗Conseil : Si vous avez des questions, idées ou suggestions à réaliser, n'hésitez pas à les soulever à tout moment. Nous ferons de notre mieux pour les résoudre et les implémenter.`

## 🗂️ Structure du Dépôt

| Répertoire | Description                                                                                              |
| ---------- | -------------------------------------------------------------------------------------------------------- |
| `lerobot/` | Dépôt LeRobot pour formation (sous-module, commit : `0878c68`) |
| `utils/` | Outils traitement données Unitree (conversion, tri) |
| `eval_robot/` | Scripts déploiement et évaluation robot |
| `test/` | Suite de tests pour chargement et conversion dataset |
| `docs/` | Documentation multilingue |

# 1. 📦 Configuration Environnement

## 1.1 🦾 Configuration Environnement LeRobot

Installez le framework [LeRobot](https://github.com/huggingface/lerobot) et les dépendances :

```bash
# Cloner avec sous-modules
git clone --recurse-submodules https://github.com/karim7tr/unitree_IL_lerobot.git
cd unitree_IL_lerobot

# Si déjà cloné, mettre à jour sous-modules
git submodule update --init --recursive

# Créer environnement conda
conda create -y -n unitree_lerobot python=3.10
conda activate unitree_lerobot

# Installer dépendances
conda install pinocchio -c conda-forge
conda install ffmpeg=7.1.1 -c conda-forge

# Installer LeRobot
cd unitree_lerobot/lerobot && pip install -e .

# Installer unitree_lerobot
cd ../../ && pip install -e .
```

## 1.2 🕹️ unitree_sdk2_python (Pour Robot Réel)

Pour communication DDS avec robots Unitree :

```bash
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
cd unitree_sdk2_python && pip install -e .
```

## 1.3 🎮 Configuration Simulation

### Option A : IsaacLab (GPU Requis)

Pour simulation hautes performances avec GPU :

```bash
# Suivez instructions sur :
# https://github.com/unitreerobotics/unitree_sim_isaaclab
```

**Exigences :** GPU NVIDIA avec 8GB+ VRAM, support CUDA

### Option B : MuJoCo (CPU-Friendly) ⭐ NOUVEAU

Pour simulation légère sans GPU :

```bash
pip install mujoco
```

**Aucun GPU requis !** Voir [MUJOCO_SIMULATION_GUIDE.md](../MUJOCO_SIMULATION_GUIDE.md) pour configuration complète.

# 2. ⚙️ Collecte et Conversion Données

## 2.1 🖼️ Charger Datasets Existants

Chargez datasets pré-enregistrés depuis Hugging Face :

```python
from lerobot.datasets.lerobot_dataset import LeRobotDataset

# Charger dataset
dataset = LeRobotDataset(repo_id="unitreerobotics/G1_Dex3_ToastedBread_Dataset")

# Accéder épisode
episode_index = 0
from_idx = dataset.meta.episodes["dataset_from_index"][episode_index]
to_idx = dataset.meta.episodes["dataset_to_index"][episode_index]

for step_idx in range(from_idx, to_idx):
    step = dataset[step_idx]
```

**Visualisation :**

```bash
cd unitree_lerobot/lerobot
python src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id unitreerobotics/G1_Dex3_ToastedBread_Dataset \
    --episode-index 0
```

## 2.2 🔨 Collecte Données

Collectez vos propres données en utilisant [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate/tree/g1) avec robot Unitree G1.

**Format sortie :**
```
datasets/
└── nom_tache/
    ├── episode_0001/
    │   ├── audios/
    │   ├── colors/
    │   ├── depths/
    │   └── data.json
    ├── episode_0002/
    └── ...
```

## 2.3 🛠️ Conversion Données

### Étape 1 : Trier et Renommer

Assurez dénomination épisodes séquentielle :

```bash
python unitree_lerobot/utils/sort_and_rename_folders.py \
    --data_dir $HOME/datasets/nom_tache
```

### Étape 2 : Convertir en Format LeRobot

```bash
python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
    --raw-dir $HOME/datasets/nom_tache \
    --repo-id votre_nom/nom_tache \
    --robot_type Unitree_G1_Dex3 \
    --push_to_hub
```

**Types robot supportés :**
- `Unitree_Z1_Single`, `Unitree_Z1_Dual`
- `Unitree_G1_Dex1`, `Unitree_G1_Dex3`
- `Unitree_G1_Brainco`, `Unitree_G1_Inspire`
- `Unitree_G1_Dex1_Sim` (pour IsaacLab)
- Et 4 configurations mobiles/levage supplémentaires

# 3. 🚀 Formation

Formez politiques en utilisant LeRobot. Voir [documentation officielle LeRobot](https://github.com/huggingface/lerobot/tree/main/docs/source) pour détails.

## 3.1 Politique ACT (Rapide, Bonne Base)

```bash
cd unitree_lerobot/lerobot

python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=votre_nom/nom_tache \
    --policy.type=act \
    --policy.push_to_hub=false
```

## 3.2 Politique Diffusion (Meilleures Performances)

```bash
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=votre_nom/nom_tache \
    --policy.type=diffusion \
    --policy.push_to_hub=false
```

## 3.3 Simulation MuJoCo ⭐ NOUVEAU

Testez avec simulation MuJoCo CPU-friendly :

```bash
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=votre_nom/nom_tache \
    --frequency=30 \
    --kp_arm=100.0 \
    --kd_arm=10.0 \
    --use_gravity_compensation=true \
    --visualization=true
```

**Pourquoi MuJoCo ?**
- ✅ Aucun GPU requis (fonctionne sur CPU)
- ✅ Installation simple (`pip install mujoco`)
- ✅ Physique stable avec gains PD configurables
- ✅ Empêche chute robot et mouvement aléatoire

Voir [MUJOCO_SIMULATION_GUIDE.md](../MUJOCO_SIMULATION_GUIDE.md) pour dépannage.

# 4. 🤖 Déploiement et Évaluation

## 4.1 Déploiement Robot Réel

Déployez politique formée sur Unitree G1 physique :

```bash
# D'abord démarrer serveur images (voir documentation avp_teleoperate)

python unitree_lerobot/eval_robot/eval_g1.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=votre_nom/nom_tache \
    --arm="G1_29" \
    --ee="dex3" \
    --frequency=30 \
    --visualization=true \
    --send_real_robot=true
```

## 4.2 Simulation IsaacLab

Testez dans simulation GPU haute fidélité :

```bash
python unitree_lerobot/eval_robot/eval_g1_sim.py \
    --policy.path=outputs/train/.../pretrained_model \
    --repo_id=votre_nom/nom_tache \
    --arm="G1_29" \
    --ee="dex3" \
    --frequency=30 \
    --visualization=true
```

# 5. 🔧 Référence Configuration

## Types Robot

| Type | Bras | End-Effector | DOF | Cas d'usage |
|------|------|--------------|-----|-------------|
| `Unitree_Z1_Single` | Simple | Pince | 7 | Manipulation bureau |
| `Unitree_Z1_Dual` | Double | Pince | 14 | Tâches bimanuelles |
| `Unitree_G1_Dex1` | Double | Pince 1-DOF | 16 | Préhension simple |
| `Unitree_G1_Dex3` | Double | Main 7-DOF | 28 | Manipulation dextre |
| `Unitree_G1_Brainco` | Double | Main BrainCo | 26 | Recherche prothétique |
| `Unitree_G1_Inspire` | Double | Main Inspire1 | 26 | Préhension avancée |

## Paramètres Communs

| Paramètre | Par défaut | Description |
|-----------|------------|-------------|
| `--arm` | `G1_29` | Version robot (`G1_29` ou `G1_23`) |
| `--ee` | `dex3` | End-effector (`dex3`, `dex1`, `inspire1`, `brainco`) |
| `--frequency` | 30 | Fréquence contrôle (Hz) |
| `--episodes` | 0 | Nombre épisodes (0 = infini) |
| `--visualization` | true | Activer visualisation 3D |

# 6. 🤔 Dépannage

| Problème | Solution |
|----------|----------|
| **401 Non Autorisé (HuggingFace)** | Exécutez `huggingface-cli login` |
| **Erreurs FFmpeg** | `conda install -c conda-forge ffmpeg=7.1.1` |
| **Robot tombe dans MuJoCo** | Augmentez `--kp_leg` et activez `--use_gravity_compensation` |
| **Mouvement articulations aléatoire** | Baissez `--kp_arm`, augmentez `--kd_arm`, réduisez `--max_joint_velocity` |
| **Formation lente** | Réduisez `--training.batch_size` ou utilisez politique plus petite |
| **GPU mémoire épuisée** | Activez `--policy.gradient_checkpointing=true` |

Voir [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) pour dépannage supplémentaire.

# 7. 📖 Ressources d'Apprentissage

## Commencer (Débutant)

1. Lisez [ANALYSIS_SUMMARY.md](../ANALYSIS_SUMMARY.md) - Vue d'ensemble
2. Chargez dataset démo (section 2.1)
3. Visualisez dataset
4. Exécutez simulation MuJoCo avec modèle pré-formé

## Intermédiaire

1. Collectez données propres avec `avp_teleoperate`
2. Convertissez en format LeRobot
3. Formez politique ACT
4. Évaluez en simulation

## Avancé

1. Déployez sur robot réel
2. Essayez politiques différentes (Diffusion, Pi0, Groot)
3. Ajoutez configuration robot personnalisée
4. Modifiez contrôleurs pour votre matériel

# 8. 🎬 Exemple Workflow Complet

```bash
# 1. Configurez environnement
conda create -y -n unitree_lerobot python=3.10
conda activate unitree_lerobot
# ... (voir section 1.1)

# 2. Convertissez vos données
python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
    --raw-dir $HOME/datasets/cueillir_pomme \
    --repo-id monnom/cueillir_pomme \
    --robot_type Unitree_G1_Dex3 \
    --push_to_hub

# 3. Formez politique
cd unitree_lerobot/lerobot
python src/lerobot/scripts/lerobot_train.py \
    --dataset.repo_id=monnom/cueillir_pomme \
    --policy.type=act

# 4. Testez en simulation MuJoCo (aucun GPU nécessaire !)
cd ../..
python unitree_lerobot/eval_robot/eval_g1_mujoco.py \
    --policy.path=unitree_lerobot/lerobot/outputs/.../pretrained_model \
    --repo_id=monnom/cueillir_pomme \
    --frequency=30

# 5. Déployez sur robot réel
python unitree_lerobot/eval_robot/eval_g1.py \
    --policy.path=unitree_lerobot/lerobot/outputs/.../pretrained_model \
    --repo_id=monnom/cueillir_pomme \
    --arm="G1_29" \
    --ee="dex3"
```

# 9. 🙏 Remerciements

Ce code s'appuie sur ces excellents projets open-source :

1. [LeRobot](https://github.com/huggingface/lerobot) - Framework formation
2. [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python) - Communication robot
3. [avp_teleoperate](https://github.com/unitreerobotics/avp_teleoperate) - Collecte données
4. [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab) - Simulation
5. [MuJoCo](https://github.com/google-deepmind/mujoco) - Simulation physique

# 10. 📞 Support

- **Documentation :** Consultez documentation dans ce dépôt
- **Issues :** [GitHub Issues](https://github.com/karim7tr/unitree_IL_lerobot/issues)
- **Discord :** [Communauté Unitree](https://discord.gg/ZwcVwxv5rq)
- **Datasets :** [HuggingFace Hub](https://huggingface.co/unitreerobotics)

# 11. 📄 Licence

Apache License 2.0 - Voir fichier [LICENSE](../LICENSE)

---

**Liens Rapides :**
- [README Anglais](../README.md) | [README Italien](./README_it.md) | [README Français](./README_fr.md) | [README Chinois](./README_zh.md)
- [Guide MuJoCo](../MUJOCO_SIMULATION_GUIDE.md) | [Référence Rapide](../QUICK_REFERENCE.md) | [Approfondissement Technique](../TECHNICAL_DEEP_DIVE.md)
