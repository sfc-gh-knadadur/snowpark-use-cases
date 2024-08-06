FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu20.04
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    curl \
    sudo \
    git \
    python3 \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ensure Git is installed 
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV PATH="/root/miniconda3/bin:${PATH}"
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

# Create conda environment with Python 3.9
RUN conda create -y --name myenv python=3.9

# Activate conda environment and install necessary Python packages
RUN /bin/bash -c "source activate myenv && conda install -y pip pipenv jupyterlab  huggingface_hub"

# Install PyTorch, TorchVision, Torchaudio, and PyTorch-CUDA
# RUN /bin/bash -c "source activate myenv && conda install -y pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 pytorch-cuda=11.8 -c pytorch -c nvidia"

# Ensure the conda environment is activated when starting a container
ENV CONDA_DEFAULT_ENV=myenv
ENV PATH="/root/miniconda3/envs/myenv/bin:${PATH}"

WORKDIR /app


# Copy files and folders from local src folder to /app in the container
# COPY RAVE-main ./source/RAVE-main
COPY install_libs.sh .
COPY entrypoint.sh .
COPY Typing4sec.mp4 .

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh


WORKDIR /app

EXPOSE 8888

ENTRYPOINT ["/app/entrypoint.sh"]

# CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
