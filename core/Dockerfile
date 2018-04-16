FROM ubuntu:16.04

# install python and git
RUN \
    apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:jonathonf/python-3.6 && \
    apt-get update && \
    apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv git

# update pip
RUN \
    python3.6 -m pip install pip --upgrade && \
    python3.6 -m pip install wheel

# install required python packages
RUN pip3.6 install azure keras h5py tensorflow matplotlib Pillow

# download source code
RUN git clone https://github.com/YanniWangAnnie/PhotoFun.git

# enter to core path
WORKDIR /PhotoFun/core

# launch code
CMD python3.6 master.py
