#!/bin/bash

# Function to check command execution status
check_command_status() {
    if [ $? -ne 0 ]; then
        echo "Error: Command failed - $1"
        exit 1
    fi
}

# Install additional requirements from requirements.txt
pip install -r requirements.txt
check_command_status "pip install -r requirements.txt"


# Install specific versions of PyTorch, torchvision, torchaudio, and CUDA
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
check_command_status "pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118"


# Install xformers using conda
pip install xformers==0.0.20
check_command_status "pip install xformers==0.0.20"
