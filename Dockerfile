FROM resin/raspberry-pi-debian:latest
ENV INITSYSTEM on

WORKDIR /root/

RUN buildDeps='build-essential cmake unzip pkg-config wget gfortran python3-dev python3-pip' \
    && runDeps='libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libatlas-base-dev python3' \
    && set -x \
    && apt-get update \
    && apt-get install -y $buildDeps --no-install-recommends  \
    && apt-get install -y $runDeps --no-install-recommends  \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install numpy \
    && wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip \
    && wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip \
    && unzip opencv.zip \
    && unzip opencv_contrib.zip \
    && mv opencv-4.0.0 opencv \
    && mv opencv_contrib-4.0.0 opencv_contrib \
    && cd ./opencv \
    && mkdir build \
    && cd build \
    && cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D BUILD_EXAMPLES=OFF \
    -D PYTHON_DEFAULT_EXECUTABLE=$(which python3) \
    -D BUILD_opencv_python3=ON \
    -D HAVE_opencv_python3=ON \
    .. \
    && make -j4 install \
    && ldconfig \
    && cd ../../opencv/build/python_loader \
    && python3 setup.py install \
    && cd /root && rm -r opencv* \
    && apt-get remove -y $buildDeps