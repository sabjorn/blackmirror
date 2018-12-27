#!/usr/bin/env bash
if [ "$(whoami)" != "root" ]; then
    echo "must be run as root."
    exit 1
fi

set -ex
cd /${HOME}/

PROJECT_NAME=blackmirror

# setup PI for installation
export HOSTVAR=blackmirror
wget -O - https://gist.githubusercontent.com/sabjorn/0d62b722fc49a7714d23313c856244ef/raw/5a141f58b9abd615df4c09e52497b15b0621cb14/rpi_installation_installer.sh | bash

## Add dependencies
deps="git ca-certificates python3 python3-pip python3-setuptools \
    libatlas-base-dev libopenjp2-7-dev libjpeg-dev libtiff5-dev zlib1g-dev libfreetype6-dev \
    liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev"
until apt-get update 
do
  echo "apt-get update failed, trying again."
  sleep 1
done
apt-get install -y ${deps} --no-install-recommends
rm -rf /var/lib/apt/lists/*

# Install project
GITBRANCH="${GITBRANCH:-master}"
if [[ ! -d "/${HOME}/${PROJECT_NAME}" ]]
then 
    git clone -b $GITBRANCH --single-branch https://github.com/sabjorn/${PROJECT_NAME}.git
else
    cd /${HOME}/${PROJECT_NAME}
    git checkout ${GITBRANCH}
    git fetch
    git pull -r
fi
cd /${HOME}/${PROJECT_NAME}
pip3 install -r requirements.txt
systemctl enable ${HOME}/${PROJECT_NAME}/${PROJECT_NAME}.service
cd /${HOME}

# Remove console blanking
echo "consoleblank=0" >> /boot/cmdline.txt

# enable RPI Camera
echo "start_x=1             # essential
gpu_mem=128           # at least, or maybe more if you wish
disable_camera_led=1  # optional, if you don't want the led to glow" >> /boot/config.txt

set +ex
reboot