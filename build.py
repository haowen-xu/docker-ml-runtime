#!/usr/bin/env python
import os
import shutil
import subprocess
import sys
import time

import click

try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory


@click.command()
@click.option('--pypi-mirror', type=str,
              default='https://pypi.tuna.tsinghua.edu.cn/simple')
@click.option('--apache-mirror', type=str,
              default='https://mirrors.tuna.tsinghua.edu.cn/apache')
@click.option('--tensorflow', type=str, default='1.11', required=False)
@click.option('--spark', type=str, default='2.3', required=False)
@click.option('-r', '--repo', type=str, required=True,
              help='Repository of the docker image. '
                   '(e.g., "haowenxu/base-runtime")')
@click.option('--push', is_flag=True, required=False, default=False,
              help='Push the image to DockerHub.')
@click.option('--push-to', multiple=True, type=str, required=False,
              help='Push the image to a customized docker registry.')
@click.option('--sudo', is_flag=True, required=False, default=False,
              help='Whether or not to use sudo to launch the docker CLI?')
@click.argument('variant', required=True)
def main(variant, pypi_mirror, apache_mirror,
         tensorflow, spark, repo, push, push_to, sudo):
    if variant not in ('cpu', 'gpu'):
        click.echo('Invalid variant {}'.format(variant), err=True)
        sys.exit(-1)

    def docker_call(args, **kwargs):
        args = (['sudo', 'docker'] if sudo else ['docker']) + args
        print('$ {}'.format(' '.join(args)))
        sys.stdout.flush()
        sys.stderr.flush()
        subprocess.check_call(args, **kwargs)

    tags = [
        variant,
        '{variant}-tensorflow{tensorflow}-spark{spark}'.format(
            variant=variant, tensorflow=tensorflow, spark=spark)
    ]
    image_names = ['{}:{}'.format(repo, tag) for tag in tags]

    with TemporaryDirectory() as tmpdir:
        pwd = os.path.abspath(os.getcwd())
        work_dir = os.path.join(tmpdir, 'build')
        shutil.copytree(pwd, work_dir)
        
        # configure the Dockerfile
        args = [
            sys.executable,
            'configure.py',
            '-c', 'config/{}.yml'.format(variant),
            '-c', 'config/tensorflow{}.yml'.format(tensorflow),
            '-c', 'config/spark{}.yml'.format(spark)
        ]
        subprocess.check_call(args, cwd=work_dir)
        
        # build the docker
        args = [
            'build',
            '--build-arg', 'CACHEBUST={}'.format(time.time()),
            '--build-arg', 'PIP_OPTS=-i {}'.format(pypi_mirror),
            '--build-arg', 'APACHE_MIRROR={}'.format(apache_mirror),
            '-t', image_names[-1]
        ]
        args.append('.')
        docker_call(args, cwd=work_dir)

    # tag the docker images
    for image_name in image_names[:-1]:
        docker_call(['tag', image_names[-1], image_name])
    for registry in push_to:
        for image_name in image_names:
            remote_image_name = '{}/{}'.format(registry, image_name)
            docker_call(['tag', image_names[-1], remote_image_name])

    # push the docker images
    if push:
        for image_name in image_names:
            docker_call(['push', image_name])
    for registry in push_to:
        for image_name in image_names:
            remote_image_name = '{}/{}'.format(registry, image_name)
            docker_call(['push', remote_image_name])

if __name__ == '__main__':
    main()
