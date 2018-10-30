#!/usr/bin/env python
import codecs
import os

import click
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined


@click.command()
@click.option('-c', '--config', help='YAML configuration file to read.',
              multiple=True)
def main(config):
    # load the configurations
    config_dict = {}
    for config_file in config:
        with codecs.open(config_file, 'rb', 'utf-8') as f:
            config_dict.update(yaml.load(f))

    # render the template
    source_root = os.path.split(os.path.abspath(__file__))[0]
    env = Environment(
        loader=FileSystemLoader(source_root),
        undefined=StrictUndefined,
        autoescape=False
    )
    template = env.get_template('Dockerfile.template')
    dockerfile_source = template.render(config=config_dict) + '\n'

    # generate the Dockerfile
    dockerfile_path = os.path.join(source_root, 'Dockerfile')
    with codecs.open(dockerfile_path, 'wb', 'utf-8') as f:
        f.write(dockerfile_source)


if __name__ == '__main__':
    main()
