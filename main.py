
import csv
import os
import sys
from utils import parse_commands

csv.field_size_limit(sys.maxsize)

def to_dir_file_map(rootdir):
  dir_file_map = {}
  for root, dirs, files in os.walk(rootdir):
    if root == rootdir:
      continue
    dir_file_map[root] = files
  return dir_file_map

def to_tag_from_dir(dir_name, rootdir):
  return os.path.relpath(dir_name, rootdir)

def tag_to_file(input_file, output_file, tag):
  reader = csv.DictReader(input_file, delimiter='\t', fieldnames=['k', 'v'])
  writer = csv.writer(output_file, delimiter='\t')
  for row in reader:
    tagged_v = '%s:%s' % (row['v'], tag)
    writer.writerow([row['k'], tagged_v])

def main():
  command_configs = {
    '-i': {
      'longInputForm': '--input-dir',
      'field': 'input_dir',
    },
    '-o': {
      'longInputForm': '--output-dir',
      'field': 'output_dir',
    },
  }
  commands = parse_commands(sys.argv[1:], command_configs)
  dir_file_map = to_dir_file_map(commands.input_dir)

  for dir_name, files in dir_file_map.items():
    tag = to_tag_from_dir(dir_name, commands.input_dir)
    for file_name in files:
      input_file_path = os.path.join(dir_name, file_name)
      output_file_path = os.path \
        .join(commands.output_dir, tag, file_name) \
        .replace('.tsv', '.txt')

      if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))

      print(input_file_path)
      print(output_file_path)

      with open(input_file_path, 'r') as input_file, \
          open(output_file_path, 'w', newline='') as output_file:
        tag_to_file(input_file, output_file, tag)

if __name__ == '__main__':
  main()
