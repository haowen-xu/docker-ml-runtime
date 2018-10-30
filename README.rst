ML Runtime
==========

This is a Ubuntu Docker image with various machine learning runtime.

It is based on the `Base Runtime <https://github.com/haowen-xu/docker-base-runtime>`_.

Major Packages
--------------

All the variants can be retrieved at `Docker Hub <https://hub.docker.com/r/haowenxu/ml-runtime>`_.

* Variants:
   * CPU variant: based on `haowenxu/base-runtime:cpu`
   * GPU variant: based on `haowenxu/base-runtime:gpu`

Installation
------------

Generate the Dockerfile
~~~~~~~~~~~~~~~~~~~~~~~

We use `configure.py` to generate the Dockerfile according to configurations.

You should first install the dependencies of `configure.py`::

    pip install -r requirements.txt

Then for example, you can use the following statement to generate the CPU
variant Dockerfile::

    python configure.py \
        -c config/cpu.yml \
        -c config/tensorflow1.11.yml

Build the Docker Image
~~~~~~~~~~~~~~~~~~~~~~

After generate the Dockerfile, you can build the docker image by::

    docker build .

Usage
-----

The basic usage of this docker image is shown as below.
Note that you may specify the `TZ` environmental variable, such that the
container will have the correct timezone::

    docker run \
        -ti --rm \
        -e TZ=Asia/Shanghai \
        haowenxu/ml-runtime:cpu \
        /bin/bash
