#!/bin/bash
set -e

#!/bin/bash
set -e

# Activate the Conda environment
source activate myenv

if [ -f "/app/install_libs.sh" ]; then
    echo "Copying install_libs.sh to /app/imagesimilarity/..."
    cp /app/install_libs.sh /app/imagesimilarity/
    cp /app/Demo_Notebook.ipynb /app/imagesimilarity/
    cp /app/creds.json /app/imagesimilarity/
    cp /app/requirements.txt /app/imagesimilarity/
        
    # Run the install_libs.sh script
    echo "Running install_libs.sh..."
    bash /app/imagesimilarity/install_libs.sh
else
    echo "install_libs.sh not found in /app. Skipping copy and execution."
fi

cd /app

# Start Jupyter Lab
echo "Starting Jupyter Lab..."
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''