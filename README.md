# postura-project

## Description
Postura Project is software for the physical analysis of human gait. The system detects and processes a person’s joint keypoints from video or sequences of images, computes kinematic variables (position, velocity, and acceleration), and produces visualizations that allow quantifying the different phenomena of movement during walking. From the charts and results, it is possible to distinguish a "normal" gait from patterns that indicate difficulties or gait impairments.

## What it does
- Captures or loads video/frame sequences and detects joints (keypoints).
- Computes joint positions over time and differentiates these signals to obtain velocity and acceleration.
- Generates plots of position, velocity, and acceleration for each joint or relevant segment.
- Enables quantification and comparison of movement phenomena (for example: step periodicity, symmetry, acceleration peaks).
- Exports processed data (CSV) for further analysis.

## Main technologies and libraries
The project is developed in Python and uses, among others, the following key libraries:
- Python
- OpenCV (opencv-contrib-python) — image/video capture and processing
- MediaPipe — joint keypoint detection and tracking (pose)
- NumPy — numerical computing
- Pandas — data handling and export (DataFrames, CSV)
- Matplotlib — static plotting
- Plotly / Kaleido — interactive visualizations and figure export
- SciPy — signal processing and advanced numerical routines
- JAX / jaxlib — (present in dependencies; used in specific parts if applicable)
- Pillow — image manipulation
- sounddevice — (if audio capture/use is required)
- protobuf, flatbuffers, etc. — dependencies of MediaPipe and other modules

## Setting up the virtual environment
- On macOS and Linux:
```bash
python -m venv myenv
source myenv/bin/activate
```

- On Windows:
```shell
python -m venv myenv
myenv\Scripts\activate
```

## Managing dependencies
1. Install existing dependencies from `requirement.txt` file:
```bash
pip install -r requirements.txt
```

2. Install any new dependency if needed:
```bash
pip install <lib>
```

3. Re-generate the requirements file:
```bash
pip freeze > requirements.txt
```
