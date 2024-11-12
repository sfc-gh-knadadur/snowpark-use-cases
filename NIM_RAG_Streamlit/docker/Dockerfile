FROM python:3.10

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install  \
        curl \
        sudo \
        libgl1 \
        poppler-utils \
        tesseract-ocr

ENV FLASK_APP=nvidia_nemo
ENV FLASK_DEBUG=true

# Install ttyd
RUN VER=$( curl --silent "https://api.github.com/repos/tsl0922/ttyd/releases/latest"| grep '"tag_name"'|sed -E 's/.*"([^"]+)".*/\1/') \
    && curl -LO https://github.com/tsl0922/ttyd/releases/download/$VER/ttyd.x86_64 \
    && mv ttyd.* /usr/local/bin/ttyd \
    && chmod +x /usr/local/bin/ttyd

RUN useradd --user-group --create-home --no-log-init --shell /bin/bash snowflake
RUN adduser snowflake sudo && \
    sed -i 's/sudo\tALL=(ALL:ALL) ALL/sudo\tALL=(ALL:ALL) NOPASSWD: ALL/' /etc/sudoers

USER snowflake
WORKDIR /home/snowflake
RUN mkdir -p handler streamlit
COPY  ./streamlit.py ./streamlit/
COPY  ./requirements.txt ./streamlit/
RUN python -m venv streamlit_env  && \
     . streamlit_env/bin/activate && \
     python -m pip install --upgrade pip && \
     pip install --no-cache-dir -r streamlit/requirements.txt