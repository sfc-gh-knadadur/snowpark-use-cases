#!/bin/bash

# Function to check command execution status
check_command_status() {
    if [ $? -ne 0 ]; then
        echo "Error: Command failed - $1"
        exit 1
    fi
}


# Install specific versions of PyTorch, torchvision, torchaudio, and CUDA
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
pip install --quiet av pims
pip install --quiet torchvision
pip install --quiet gdown

check_command_status "pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118"


# Install xformers using conda
pip install xformers==0.0.20
check_command_status "pip install xformers==0.0.20"

#navigate and git clone repo
cd /app/robustvideomatting/RobustVideoMatting/RobustVideoMatting-master
git clone  https://github.com/PeterL1n/RobustVideoMatting /app/robustvideomatting/RobustVideoMatting/RobustVideoMatting-master/temp
mv temp/* /app/robustvideomatting/RobustVideoMatting/RobustVideoMatting-master
rm -rf temp

# download model files and input video
gdown https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3.pth
gdown https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_resnet50.pth
gdown https://drive.google.com/uc?id=1I0v72-hNlK1hm9q1OwyaATUYApXpotS6 -O input.mp4



