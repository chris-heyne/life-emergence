# HEYNE - Life Emergence

An interactive artificial life simulator built in Python. This engine simulates emergence—complex, self-organizing structures arising from simple physics rules.

![Heyne Life — Emergence](heyne_emergence.png)

## Concept
Instead of hardcoding complex behaviors, **HEYNE - Life Emergence** relies on a simple 4x4 Interaction Matrix. Four particle species (**Red**, **Blue**, **Green**, **White**) interact through attraction and repulsion forces.

By adjusting the pairwise interaction weights between `-1.0` and `+1.0`, the system spontaneously generates emergent biological patterns.

## Features
* **Vectorized Physics Engine:** High-performance pairwise force calculations powered by `NumPy`.
* **Crisp Flat Vector Rendering:** Clean 2D rendering pipeline using Pygame's batch blitting (`blits`) for high FPS performance.
* **Real-time Control Panel:**
  * **Interactive Matrix:** Adjust interaction forces live (Left-click: `+0.1`, Right-click: `-0.1`).
  * **Per-Species Population:** Dynamically tune individual particle species counts.
  * **Live Physics Tuning:** Modify friction damping, interaction radii (`r_max`, `r_repel`), and simulation speed on the fly.
* **Presets:** Instantly load stable emergent configurations (*Food Chain*, *Swarms*, *Gliding Worms*, *Symbiosis*).

## Installation & Setup

### Prerequisites
* Python 3.10 or higher

### 1. Clone the repository
```bash
git clone [https://github.com/chrisheyne-eth/heyne-life-emergence.git](https://github.com/chrisheyne-eth/heyne-life-emergence.git)
cd heyne-life-emergence
```

### 2. Create and activate a virtual environment
* **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
* **Windows:**
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate
  ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## How to Play

Run the simulation:
```bash
python app.py
```

* **Left-Click** a matrix cell to increase attraction strength (`+0.1`).
* **Right-Click** a matrix cell to increase repulsion strength (`-0.1`).
* Use the **Presets** to quickly switch between different synthetic ecosystems.
* Click **Randomize Matrix** to discover new emergent behaviors.
* Use **Reset Defaults** to restore base physics settings at any time.

## License
Distributed under the MIT License. See `LICENSE` for more information.