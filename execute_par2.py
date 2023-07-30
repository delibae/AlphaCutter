import argparse
import gzip
import logging
import os
import shutil
import tarfile
from concurrent.futures import ThreadPoolExecutor
from glob import glob

import pandas as pd
from tqdm import tqdm

from Alphacutter import main_pr
from cif2pdb import cif2pdb

# Argument parser setup
parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument(
    "--folder_num", type=int, required=True, help="Folder number to process"
)
args = parser.parse_args()

folder_num = args.folder_num

input_folder = f"/runs/users/baehanjin/afdb_files/not_in_proteomes/csv/{folder_num}"
output_base = f"/runs/users/baehanjin/afdb_files/not_in_proteomes/alphacutter"
target_folder = "/runs/users/baehanjin/afdb_files/not_in_proteomes/files/cif"
tmp_folder_base = "/runs/users/baehanjin/work/AlphaCutter/tmp"
csv_files = glob(f"{input_folder}/*.csv")

completed_file = (
    f"/runs/users/baehanjin/work/AlphaCutter/logs/completed_taxIds2_{folder_num}.log"
)

# Set up logging
logging.basicConfig(filename=completed_file, level=logging.INFO)


def process_file(file):
    tax_id = int(file.split("/")[-1].split(".")[0].split("_")[1])

    df = pd.read_csv(file)
    target_paths = (
        df["uniprotAccession"]
        .apply(lambda x: f"{target_folder}/AF-{x}-F1-model_v4.cif")
        .tolist()
    )

    tmp_folder = f"{tmp_folder_base}/{tax_id}"
    os.makedirs(tmp_folder, exist_ok=True)

    for target_path in target_paths:
        shutil.copy(target_path, tmp_folder)

    for cif_file in glob(os.path.join(tmp_folder, "*.cif")):
        cif2pdb(cif_file)

    output_dir = f"{output_base}/{tax_id}"
    os.makedirs(output_dir, exist_ok=True)
    main_pr(
        loop_min=20,
        helix_min=30,
        fragment_min=5,
        domain_min=0,
        pLDDT_min=50,
        local_contact_range=5,
        single_out=True,
        domain_out=True,
        tmp_folder=tmp_folder,
        csv_save_path=output_dir,
        except_seq=True,
    )

    # Log the completed taxId instead of writing it to a file directly.
    logging.info(tax_id)

    shutil.rmtree(tmp_folder)

    progress_bar.update()


# Max number of workers for ThreadPoolExecutor
max_workers = 20

# Use a ThreadPoolExecutor to parallelize the execution.
progress_bar = tqdm(total=len(csv_files))

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(process_file, csv_files)

print("작업이 완료되었습니다.")
