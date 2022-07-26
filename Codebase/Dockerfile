FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"]

ENV LC_CTYPE="C.UTF-8"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get clean \
    && rm -rf /var/lib/apt/list/* \
    && apt-get update --fix-missing \
    && apt-get -y upgrade --fix-missing\
    && apt-get install -y build-essential checkinstall \
    cmake curl make \
    gcc git g++ \
    wget unzip yasm \
    pkg-config openssl libswscale-dev \
    libncursesw5-dev libc6-dev libtbb2 \
    libtbb-dev libjpeg-dev libpng-dev \
    libtiff-dev libavformat-dev libpq-dev \
    libgdbm-dev libsm6 libxext6 libv4l-dev \
    libxrender-dev zlib1g-dev \
    python3.8 python3.8-dev python3-venv python3.8-venv \
    python3-pip --fix-missing


WORKDIR /venv
COPY requirements.txt .
RUN    python3.8 -m venv env \
    && /venv/env/bin/pip install --upgrade pip \
    && /venv/env/bin/pip install -r requirements.txt \
    && echo "source /venv/env/bin/activate" >> ~/.bashrc

EXPOSE 8080
EXPOSE 9002
EXPOSE 5672
#docker run -v C:\Users\kalpit\PycharmProjects\Internship\venv2:C:\ProgramData\DockerDesktop

WORKDIR /new
COPY . .
RUN source /venv/env/bin/activate
#CMD [ "/venv/env/bin/python", "new.py"]