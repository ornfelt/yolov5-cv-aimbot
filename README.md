## Description

The objective of this computer vision aimbot is to detect and target characters in video games that utilize humanoid character models. This aimbot has been designed specifically for cloud-based games, as they are impervious to conventional cheating methods. Traditional cheats necessitate access to the memory, object code, and network traffic of the client-side process. In contrast, with cloud-based games, users are unable to interfere with the game's internal workings.

This project is mainly a proof of concept as the computational requirements and level of performance renders this approach infeasible. 
For an overview of how this aimbot functions, see the [METHODOLOGY.md](https://github.com/RyanSawchuk/cv-aimbot/blob/main/METHODOLOGY.md) file.

### Built With

* [Python3](https://www.anaconda.com/products/individual)
* [YOLOv5](https://pytorch.org/hub/ultralytics_yolov5/)


## Getting Started

### Prerequisites

* [Python3](https://www.anaconda.com/products/individual)
* Cuda toolkit v11 if using an Nvidia GPU: 
```conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c conda-forge```
  * [PyTorch Installation](https://pytorch.org/get-started/locally/)


### Installation

1. Clone the repo: 
   ```sh
   git clone https://github.com/RyanSawchuk/cv-aimbot.git
   ```
2. Install Python packages: 
   ```sh
   python -m pip install -r requirements.txt
   ```


## Usage

```python3
python aimbot.py
```


Exit key: ```'='```


Toggle firing key: ```'-'```


## Example

![Test](images/example3.png?raw=true "Example aimbot")

## Road Map
- CLI argument for mirror screen size.
- Record filtered screen capture.

## Known Issues
- Finiky toggle firing key.
- Some applications dont allow mouse movements.


## Acknowledgments

* [YOLOv5](https://pytorch.org/hub/ultralytics_yolov5/)

