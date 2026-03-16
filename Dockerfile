FROM osrf/ros:humble-desktop AS base

ARG USERNAME=RosGazebo
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG DEBIAN_FRONTEND=noninteractive

ENV NVIDIA_DRIVER_CAPABILITIES=all
ENV NVIDIA_VISIBLE_DEVICES=all
ENV DOCKER_RUNNING=true

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip nano sudo curl lsb-release gnupg

RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

RUN apt-get update
RUN apt-get install -y ignition-fortress

# camera driver things
RUN apt-get install -y aravis-tools
RUN apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
RUN apt-get install -y ros-humble-camera-aravis2
RUN apt-get install -y ros-humble-rosbag2-storage-mcap
RUN apt-get install -y ros-humble-stereo-image-proc
RUN apt-get install -y ros-humble-camera-calibration

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Munkakönyvtár beállítása a ROS 2 workspace-re
WORKDIR /ros2_ws