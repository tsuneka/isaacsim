ARG BASE_IMAGE=nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04
FROM $BASE_IMAGE

ARG UID
ARG GID
ARG USERNAME

USER root
SHELL ["/bin/bash", "-c"]

ENV TZ=Asia/Tokyo

RUN export DEBIAN_FRONTEND=noninactive \
    && apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
        apt-transport-https \
        build-essential \
        bzip2 \
        ca-certificates \
        curl \
        ffmpeg \
        g++ \
        git \
        gnupg \
        graphviz \
        locales \
        libgl1-mesa-dev \
        libusb-1.0-0-dev \
        lsb-release \
        net-tools \
        openssh-client \
        software-properties-common \
        sudo \
        unzip \
        vim \
        wget \
        xorg-dev \
        zip \
        emacs \
        python3-dev \
        python3-setuptools \
        python3-pip \
        python3-venv \
        vulkan-tools \
        usbutils \
        x11-apps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    libvulkan1 vulkan-tools libgl1 libxrender1 libxi6 libxkbcommon0 libgtk-3-0 libcanberra-gtk-module \
    libglib2.0-0 libnss3 libasound2 \
    zenity xdg-utils \
    && mkdir -p /usr/share/vulkan/icd.d /etc/vulkan/icd.d \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${GID} ${USERNAME} && useradd -u ${UID} -g ${GID} -s /bin/bash -m ${USERNAME}
WORKDIR /home/$USERNAME/ws

# ROS2
ENV ROS_DISTRO=humble
RUN locale-gen ja_JP ja_JP.UTF-8 \
    && update-locale LC_ALL=ja_JP.UTF-8 LANG=ja_JP.UTF-8
ENV LANG=ja_JP.UTF-8
RUN add-apt-repository universe \
    && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null \
    && apt-get update && apt-get install -y \
        ros-$ROS_DISTRO-desktop \
        ros-dev-tools \
        ros-$ROS_DISTRO-xacro \
        ros-$ROS_DISTRO-joint-state-publisher \
        ros-$ROS_DISTRO-joint-state-publisher-gui \
        ros-$ROS_DISTRO-moveit \
        python3-rosdep \
        python3-colcon-common-extensions \
        python3-colcon-mixin \
        python3-vcstool \
        python3-argcomplete \
        # for isaacsim bridge
        ros-$ROS_DISTRO-vision-msgs \
        ros-$ROS_DISTRO-ackermann-msgs \
        python3-rosinstall \
        python3-rosinstall-generator \
        python3-wstool \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rosdep init \
    && rosdep update

# uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /home/$USERNAME/

USER $USERNAME
RUN mkdir isaacsim \
    && cd isaacsim \
    && uv venv --python 3.10 \
    && source .venv/bin/activate \
    && uv pip install --upgrade pip \
    && uv pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu124 \
    && uv pip install 'isaacsim[all,extscache]==4.5.0' --extra-index-url https://pypi.nvidia.com

USER root
RUN source /opt/ros/$ROS_DISTRO/setup.bash --extend \
    && cd ws \
    && git clone https://github.com/isaac-sim/IsaacSim-ros_workspaces.git \
    && cd IsaacSim-ros_workspaces/humble_ws \
    && rosdep update && apt-get update \
    && rosdep install -i --from-path src --rosdistro humble -y \
    && colcon build

# entrypoint
COPY isaac_sim/entrypoint.sh ./ws/entrypoint.sh
RUN chmod +x ./ws/entrypoint.sh

USER $USERNAME
USER root

ENTRYPOINT ["./ws/entrypoint.sh"]