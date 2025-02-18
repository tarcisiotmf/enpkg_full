from pathlib import Path
import os
import shutil
import argparse
import textwrap
from tqdm import tqdm
import gzip
import yaml

# These lines allows to make sure that we are placed at the repo directory level 
p = Path(__file__).parents[2]
os.chdir(p)

# Loading the parameters from yaml file


if not os.path.exists('config/params.yaml'):
    print('No config/params.yaml: copy from config/template.yaml and modify according to your needs')
with open(r'config/params.yaml') as file:
    params_list = yaml.load(file, Loader=yaml.FullLoader)

# Parameters can now be accessed using params_list['level1']['level2'] e.g. params_list['options']['download_gnps_job']


# """ Argument parser """
# parser = argparse.ArgumentParser(
#     formatter_class=argparse.RawDescriptionHelpFormatter,
#     description=textwrap.dedent('''\
#         This script copy individual sample-specific RDF graphs(.ttl format) from the ENPKG file-architecture into a single specified folder.
#          --------------------------------
#             Arguments:
#             - (--source/-s) Path to the directory where samples folders are located.
#             - (--target/-t) Path to the directory where individual ttl files are copied.
#             - (--compress/-c) Compress files to .gz while when copying.
#         '''))

# parser.add_argument('-s', '--source_path', required=True,
#                     help='The path to the directory where samples folders to process are located')
# parser.add_argument('-t', '--target_path', required=True,
#                     help='The path to the directory into wich the .ttl files are copied')
# parser.add_argument('-c', '--compress', action='store_true',
#                     help='Compress files to .gz')

# args = parser.parse_args()

source_path = os.path.normpath(params_list['sample_dir_path'])
target_path = os.path.normpath(params_list['graph_output_dir_path'])
compress = params_list['compress_outputs']

os.makedirs(target_path, exist_ok=True)

samples_dir = [directory for directory in os.listdir(source_path)]
df_list = []
for directory in tqdm(samples_dir):
    if os.path.isdir(os.path.join(source_path, directory, "rdf")):
        for file in [directory for directory in os.listdir(os.path.join(source_path, directory, "rdf"))]:
            if 'merged_graph' in file:
                file_name = file
                src = os.path.join(source_path, directory, "rdf", file_name)
    else:
        continue
    if os.path.isfile(src):
        dst = os.path.join(target_path, file_name)
        if compress:
            with open(src, 'rb') as f_in:
                file_out = os.path.join(dst) + '.gz'
                if not os.path.isfile(file_out):
                    with gzip.open(file_out, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
        else:
            shutil.copyfile(src, dst)
    else:
        continue
