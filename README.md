# Notice
Project is built around the VideoSeal v1.0 model trained and shared by
the team behind the videoseal project: https://github.com/facebookresearch/videoseal
Appropriate sections of the project reference the MIT licence this project was shared under.

# Scope

This project aims to provide an extra layer of functionality around the model:
- add a transformation step, fully determined by a symmetric key,
before the embedding or detection,
to allow for multiple watermarks to be present and detectable in the same image
- enable use from the command line - see `main.py`
- convert string, int, bytes data types to a list of 256 bits for embedding and the reverse for detection - see `algorithm/bits_adapter.py`

# Installation

The officially recommended version of python is 3.10 (pytorch > 2.3, torchvision 0.16.0, cuda 12.1),
however I haven't encountered problems using python 3.12.

To install pytorch:
```
conda install pytorch==2.4.0 torchvision==0.19.0 pytorch-cuda=12.1 -c pytorch -c nvidia
```

To install the other dependencies:
```
pip install -r requirements.txt
```

Training the model is not part of the scope.
Tested usage involves a compiled (.jit) model available at:
https://dl.fbaipublicfiles.com/videoseal/y_256b_img.jit

That can be downloaded directly into the ckpts directory with:
```
Invoke-WebRequest -Uri "https://dl.fbaipublicfiles.com/videoseal/y_256b_img.jit" -OutFile "ckpts/y_256b_img.jit"
```
It is likely possible to substitute the model 
i.e. for the compiled PixelSeal (that is not yet available at the time of writing)
by modifying the Model class in `algorithm/handle_model.py`.


# Usage

For one-off uses use `main.py`, the help message can be triggered as so:

```
python -m main -h
```

In cases with multiple operations it's significantly faster not to load the model every time.
This can be achieved with the `algorithm/interface.py` script which lazily loads the model only once,
albeit requires writing a bit of python code.


### Evaluation
The `evaluation_scripts` directory contains scripts used for testing the watermarks robustness against:
blurring, clearing the least significant bits, change of brightness, additive white gaussian noise, reducing colour depth and embedding a secondary watermark.
In addition, multiple methods of transforming the image before embedding and detection can be tested.

After updating paths to the cover images and results in the `__main__` section of the script,
it can be run with the current directory being the root of the project:
```
python -m evaluation_scripts.evaluate
```