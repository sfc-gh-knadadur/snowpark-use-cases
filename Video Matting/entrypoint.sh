#!/bin/bash
set -e

#!/bin/bash
set -e

# Activate the Conda environment
source activate myenv

# # Check if RobustVideoMatting repository exists
# if [ ! -d "/app/RobustVideoMatting/RobustVideoMatting-master" ]; then
#     echo "Downloading RobustVideoMatting repository..."
#     git clone https://github.com/RehgLab/RobustVideoMatting.git /app/RobustVideoMatting/RobustVideoMatting-master
# else
#     echo "RobustVideoMatting repository already exists. Skipping download."
# fi

# Copy install_libs.sh from /app to /app/RobustVideoMatting/RobustVideoMatting-master
if [ -f "/app/install_libs.sh" ]; then
    mkdir -p /app/robustvideomatting/RobustVideoMatting/RobustVideoMatting-master
    echo "Copying install_libs.sh to /app/robustvideomatting/RobustVideoMatting/RobustVideoMatting-master..."
    cp /app/install_libs.sh /app/robustvideomatting/RobustVideoMatting/RobustVideoMatting-master/
    
    # Run the install_libs.sh script
    echo "Running install_libs.sh..."
    bash /app/robustvideomatting/RobustVideoMatting/RobustVideoMatting-master/install_libs.sh
else
    echo "install_libs.sh not found in /app. Skipping copy and execution."
fi

# Change to the RobustVideoMatting directory
cd /app

# Start Jupyter Lab
echo "Starting Jupyter Lab..."
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''