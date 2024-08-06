#!/bin/bash
set -e

#!/bin/bash
set -e

# Activate the Conda environment
source activate myenv

clone_with_retries() {
    local attempts=0
    local max_attempts=3
    while [ $attempts -lt $max_attempts ]; do
        if git clone  https://github.com/RehgLab/RAVE.git /app/rave/RAVE-main; then
            echo "Clone successful"
            return 0
        fi
        attempts=$((attempts+1))
        echo "Clone attempt $attempts failed. Retrying in 5 seconds..."
        sleep 5
    done
    echo "Failed to clone after $max_attempts attempts"
    return 1
}

# Check if RAVE repository exists
if [ ! -d "/app/rave/RAVE-main" ]; then
    echo "Downloading RAVE repository..."
    # Increase Git buffer size
    git config --global http.postBuffer 524288000

    if ! clone_with_retries; then
        echo "Failed to clone repository. Exiting."
        exit 1
    fi
    cd /app/rave/RAVE-main
    git submodule update --init --recursive
else
    echo "RAVE repository already exists. Updating..."
    cd /app/rave/RAVE-main
    
fi


# # Check if RAVE repository exists
# if [ ! -d "/app/rave/RAVE-main" ]; then
#     echo "Downloading RAVE repository..."
#     git clone https://github.com/RehgLab/RAVE.git /app/rave/RAVE-main
# else
#     echo "RAVE repository already exists. Skipping download."
# fi

# Copy install_libs.sh from /app to /app/rave/RAVE-main
if [ -f "/app/install_libs.sh" ]; then
    echo "Copying install_libs.sh to /app/rave/RAVE-main..."
    cp /app/install_libs.sh /app/rave/RAVE-main/
    
    # Run the install_libs.sh script
    echo "Running install_libs.sh..."
    bash /app/rave/RAVE-main/install_libs.sh
else
    echo "install_libs.sh not found in /app. Skipping copy and execution."
fi

# Copy mp4 file from /app to /app/rave/RAVE-main/
if [ -f "/app/Typing4sec.mp4" ]; then
    echo "Copying Typing4sec.mp4 to /app/rave/RAVE-main..."
    cp /app/Typing4sec.mp4 /app/rave/RAVE-main/data/mp4_videos/Typing4sec.mp4
    
else
    echo "Typing4sec.mp4 not found in /app. Skipping copying"
fi


# Change to the RAVE directory
cd /app

# Start Jupyter Lab
echo "Starting Jupyter Lab..."
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''