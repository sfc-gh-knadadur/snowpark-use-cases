#!/bin/bash

# Function to check command execution status
check_command_status() {
    if [ $? -ne 0 ]; then
        echo "Error: Command failed - $1"
        exit 1
    fi
}


# Install specific versions of PyTorch, torchvision, torchaudio, and CUDA
pip install -r requirements.txt

check_command_status "pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118"





