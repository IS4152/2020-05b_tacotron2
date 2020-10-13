# Tacotron 2 (without wavenet)

PyTorch implementation of [Natural TTS Synthesis By Conditioning
Wavenet On Mel Spectrogram Predictions](https://arxiv.org/pdf/1712.05884.pdf). 

This implementation includes **distributed** and **automatic mixed precision** support
and uses the [LJSpeech dataset](https://keithito.com/LJ-Speech-Dataset/).

Distributed and Automatic Mixed Precision support relies on NVIDIA's [Apex] and [AMP].

Visit our [website] for audio samples using our published [Tacotron 2] and
[WaveGlow] models.

![Alignment, Predicted Mel Spectrogram, Target Mel Spectrogram](tensorboard.png)


## Pre-requisites
1. NVIDIA GPU + CUDA cuDNN

## Setup

### Set up repository

1. Clone this repo: `git clone https://github.com/taneliang/tacotron2.git`
1. CD into this repo: `cd tacotron2`
1. Initialize submodule: `git submodule init; git submodule update`

### Set up dependencies

1. Check CUDA toolkit version: `nvcc --version`. NB: This is the toolkit version, which may be different from the version reported by nvidia-smi.
1. Create Python 3 virtual environment: `python3 -m venv .env-cuda<CUDA version>`
1. Activate venv, by running one of the following:
    - `bash`/`sh`: `source .env-cudaxxx/bin/activate`
    - `csh`: `source .env-cudaxxx/bin/activate.csh`
    - `fish`: `source .env-cudaxxx/bin/activate.fish`
1. Install [PyTorch 1.0]. As the time this was written, these are the instructions:
    - CUDA 10.0: `pip install torch==1.4.0+cu100 torchvision==0.5.0+cu100 -f https://download.pytorch.org/whl/cu100/torch_stable.html`
    - CUDA 10.1: `pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html`
    - CUDA 10.2 or 11.0: `pip install torch torchvision`
1. Install [Apex]:
    ```sh
    pushd ..
    git clone https://github.com/NVIDIA/apex
    cd apex
    pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
    popd
    ```
1. Install Python requirements: `pip install -r requirements.txt`

### Set up data for training

If running with access to NUS School of Computing resources (e.g. Sunfire, compute cluster), you can copy the training dataset from the `cgpb0` compute cluster machine:

```sh
scripts/copy_dataset.sh
```

Otherwise, you can set up the data from scratch:

1. EmoV-DB:
    1. Download the [EmoV-DB dataset](https://github.com/numediart/EmoV-DB)
    1. Normalize it: `ls */*/*.wav | xargs -I % sh -c 'mkdir -p ../out/$(dirname %) && sox % --rate 16000 -c 1 -b 16 ../out/%'` 
1. LJSpeech:
    1. Download the [LJSpeech dataset](https://keithito.com/LJ-Speech-Dataset/).
    1. Normalize it: `mkdir ../../LJSpeech-1.1/wavs && ls *.wav | xargs -I % sh -c 'sox % --rate 16000 -c 1 -b 16 ../../LJSpeech-1.1/wavs/%'`
1. Generate filelist files:
    ```sh
    cd scripts
    vim ./genfilelist.py # Configure the script
    ./genfilelist.py
    cd ..
    ```

## Training
1. `python train.py --output_directory=outdir --log_directory=logdir`
2. (OPTIONAL) `tensorboard --logdir=outdir/logdir`

## Training using a pre-trained model
Training using a pre-trained model can lead to faster convergence  
By default, the dataset dependent text embedding layers are [ignored]

1. Download our published [Tacotron 2] model
2. `python train.py --output_directory=outdir --log_directory=logdir -c tacotron2_statedict.pt --warm_start`

## Multi-GPU (distributed) and Automatic Mixed Precision Training
1. `python -m multiproc train.py --output_directory=outdir --log_directory=logdir --hparams=distributed_run=True,fp16_run=True`

## Inference demo
1. Download our published [Tacotron 2] model
2. Download our published [WaveGlow] model
3. `jupyter notebook --ip=127.0.0.1 --port=31337`
4. Load inference.ipynb 

N.b.  When performing Mel-Spectrogram to Audio synthesis, make sure Tacotron 2
and the Mel decoder were trained on the same mel-spectrogram representation. 


## Related repos
[WaveGlow](https://github.com/NVIDIA/WaveGlow) Faster than real time Flow-based
Generative Network for Speech Synthesis

[nv-wavenet](https://github.com/NVIDIA/nv-wavenet/) Faster than real time
WaveNet.

## Acknowledgements
This implementation uses code from the following repos: [Keith
Ito](https://github.com/keithito/tacotron/), [Prem
Seetharaman](https://github.com/pseeth/pytorch-stft) as described in our code.

We are inspired by [Ryuchi Yamamoto's](https://github.com/r9y9/tacotron_pytorch)
Tacotron PyTorch implementation.

We are thankful to the Tacotron 2 paper authors, specially Jonathan Shen, Yuxuan
Wang and Zongheng Yang.


[WaveGlow]: https://drive.google.com/open?id=1rpK8CzAAirq9sWZhe9nlfvxMF1dRgFbF
[Tacotron 2]: https://drive.google.com/file/d/1c5ZTuT7J08wLUoVZ2KkUs_VdZuJ86ZqA/view?usp=sharing
[pytorch 1.0]: https://github.com/pytorch/pytorch#installation
[website]: https://nv-adlr.github.io/WaveGlow
[ignored]: https://github.com/NVIDIA/tacotron2/blob/master/hparams.py#L22
[Apex]: https://github.com/nvidia/apex
[AMP]: https://github.com/NVIDIA/apex/tree/master/apex/amp