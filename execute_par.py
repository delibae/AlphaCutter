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

folder_num = 3
input_folder = f"/runs/users/baehanjin/afdb_files/proteomes/csv/{folder_num}"
output_base = f"/runs/users/baehanjin/afdb_files/alphacutter"
target_folder = "/runs/users/baehanjin/afdb_files/proteomes/proteomes/cif"
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
    entryId_list = df["entryId"].tolist()

    tar_file_path = os.path.join(target_folder, f"proteome-tax_id-{tax_id}-0_v4.tar")

    tmp_folder = f"{tmp_folder_base}/{tax_id}"
    os.makedirs(tmp_folder, exist_ok=True)

    with tarfile.open(tar_file_path, "r") as tar:
        for entry in tar:
            entry_name = os.path.basename(entry.name)
            entry_id = entry_name.split("-model_v4.cif.gz")[0]
            if entry_id in entryId_list:
                tar.extract(entry, tmp_folder)
                with gzip.open(os.path.join(tmp_folder, entry.name), "rb") as f_in:
                    with open(os.path.join(tmp_folder, entry.name[:-3]), "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)

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
