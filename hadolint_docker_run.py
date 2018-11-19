#! /usr/bin/env python

"""Run hadolint via docker container and provide ignore rules as command line options

This script will read all .hadolint.yaml ignore rules and execute hadolint docker

"""

import subprocess
import sys
import os
import yaml


def run_cmd(cmd):
  """Executed shell command
  Returns:
          STDOUT of successful command execution
  """
  p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
  output = p.communicate()[0]
  # Wait for process to terminate before getting return code
  p.wait()
  return (output.rstrip("\n"), p.returncode)


def load_yaml(file_path):
  if os.path.exists(file_path):
    with open(file_path, 'r') as stream:
      try:
        return yaml.load(stream) or {}
      except yaml.YAMLError as e:
        print(e)
  else:
    return {}


def get_ignore_rules(ignored):
  return ' '.join(['--ignore {}'.format(code) for code in ignored])


if __name__ == '__main__':

  file_path = ('.hadolint.yaml')

  config = load_yaml(file_path)

  print('Begin linting Dockerfile..')

  # If rules exist
  if config:
    ignore_str = get_ignore_rules(config['ignored'])
    hadolint_docker_cmd = 'docker run --rm -i hadolint/hadolint hadolint {} - < Dockerfile'.format(
        ignore_str)
    feedback, rc = run_cmd(hadolint_docker_cmd)
    print(feedback)
    if rc != 0:
      sys.exit(1)
  else:
    hadolint_docker_cmd = 'docker run --rm -i hadolint/hadolint hadolint - < Dockerfile'
  print('Dockerfile lint complete.')
