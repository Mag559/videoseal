# Notice
Project is built around the VideoSeal v1.0 model, trained and shared by
the team behind the videoseal project: https://github.com/facebookresearch/videoseal
Appropriate sections of the project reference the MIT licence this project was shared under.

# Scope

This project aims to provide an extra layer of functionality around the model:
- add a transformation step, fully determined by a symmetric key,
before the embedding or detection,
to allow for multiple watermarks to be present and detectable in the same image
- enable use from the command line - see `main.py` and via http - see `web_service.py` and its usage section
- convert string, int, bytes data types to a list of 256 bits for embedding and the reverse for detection - see `algorithm/bits_adapter.py`

# Installation

The officially recommended version of python is 3.10 (pytorch > 2.3, torchvision 0.16.0, cuda 12.1),
however I haven't encountered problems using python 3.12.

To install pytorch:
```
conda install pytorch==2.4.0 torchvision==0.19.0 pytorch-cuda=12.1 -c pytorch -c nvidia
```

To install the other dependencies:
```commandline
pip install -r requirements.txt
```

Training the model is not part of the scope.
Tested usage involves a compiled (.jit) model available at:
https://dl.fbaipublicfiles.com/videoseal/y_256b_img.jit

That can be downloaded directly into the ckpts directory with:
```shell
Invoke-WebRequest -Uri "https://dl.fbaipublicfiles.com/videoseal/y_256b_img.jit" -OutFile "ckpts/y_256b_img.jit"
```
It is likely possible to substitute the model 
i.e. for the compiled PixelSeal (that is not yet available at the time of writing)
by modifying the Model class in `algorithm/handle_model.py`.


# Usage

For one-off uses use `main.py`, the help message can be triggered as so:

```commandline
python -m main -h
```

In cases with multiple operations it's significantly faster not to load the model every time.
This can be achieved by using the functions in the `algorithm/interface.py` script which lazily load the model only once.

### Web api

A development server can be locally hosted on the port 8000 by using:
```commandline
python -m web_service
```

Loading the model is performed once, upon the first request which may therefore take longer to be resolved.

Embedding the message is available via POST on /hide. The form fields are:
- image (file) — required cover image file
- key (string/int) — required key interpretable as an integer
- at least one one of the following, where the first ones take priority:
  - message (string) — watermark message in string form
  - message_int (string/number) — watermark message in int form 
  - message_bits (string - JSON) — watermark message as a list of bits (JSON-encoded) i.e. "[0,1,0,1,...]"

In return as watermarked image is sent as an attachment.
Example use with curl:
```
curl -X POST -F "key=123" -F "message=Hello" -F "image=@cover.png" http://localhost:8000/hide -o watermarked.png
```


Detecting the message is available via POST on /detect. The form fields are:
- image (file) — required, watermarked image
- key (string/int) — required key interpretable as an integer
- message_type (string) — optional way to interpret the detected message, by default string: 
"str", "int", "bits"

The response will contain the type and result fields.
Example use with curl:
```
 curl -X POST -F "key=123" -F "message_type=str" -F "image=@watermarked.png" http://localhost:8000/detect
```


# Evaluation
The `evaluation_scripts` directory contains scripts used for testing the watermarks robustness against:
blurring, clearing the least significant bits, change of brightness, additive white gaussian noise, reducing colour depth and embedding a secondary watermark.
In addition, multiple methods of transforming the image before embedding and detection can be tested.

After updating paths to the cover images and results in the `__main__` section of the script,
it can be run with the current directory being the root of the project:
```
python -m evaluation_scripts.evaluate
```