import argparse
import gzip
import os
import shutil
import tarfile
from glob import glob

import pandas as pd
from tqdm import tqdm

cuda_num = 0
# os.environ["CUDA_VISIBLE_DEVICES"] = cuda_num

# CSV 파일들이 있는 폴더 경로
input_folder = f"/runs/users/baehanjin/afdb_files/chainsaw/csv/{cuda_num}"
output_base = f"/runs/users/baehanjin/afdb_files/chainsaw/in_afdb"


# 특정 경로의 파일들을 압축 해제할 폴더 경로
target_folder = "/runs/users/baehanjin/afdb_files/proteomes/proteomes"

# 압축 해제를 위한 임시 폴더 경로
tmp_folder_base = "/runs/users/baehanjin/work/AlphaCutter/tmp"

# CSV 파일들의 리스트 가져오기
csv_files = glob(f"{input_folder}/*.csv")

# List to store successfully processed taxIds
completed_taxIds = []

# File to store the completed taxIds
completed_file = (
    f"/runs/users/baehanjin/work/AlphaCutter/logs/completed_taxIds_{cuda_num}.txt"
)

for file in tqdm(csv_files):
    # 파일명에서 taxId 추출
    tax_id = int(file.split("/")[-1].split(".")[0].split("_")[1])

    # Read the CSV file to get the entryId column
    df = pd.read_csv(file)
    entryId_list = df["entryId"].tolist()

    # proteomes_proteome-(tax_id)-0_v4.tar 파일 경로
    tar_file_path = os.path.join(target_folder, f"proteome-tax_id-{tax_id}-0_v4.tar")

    tmp_folder = f"{tmp_folder_base}/{tax_id}"
    os.makedirs(tmp_folder, exist_ok=True)

    # tmp 폴더에 압축 해제
    with tarfile.open(tar_file_path, "r") as tar:
        # Extract files matching the entryId from the CSV file
        for entry in tar:
            entry_name = os.path.basename(entry.name)
            entry_id = entry_name.split("-model_v4.cif.gz")[0]
            if entry_id in entryId_list:
                tar.extract(entry, tmp_folder)
                # Decompress the .gz file
                with gzip.open(os.path.join(tmp_folder, entry.name), "rb") as f_in:
                    with open(os.path.join(tmp_folder, entry.name[:-3]), "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)

    # Dummy job 수행 (여기에 실제로 수행할 작업을 구현)
    # print(f"Dummy job for taxId {tax_id} is running...")

    output_dir = f"{output_base}/{tax_id}"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{tax_id}.csv")

    # main(parse_args_custom(output_file=output_file, structure_dir=tmp_folder))

    # Add the completed taxId to the list
    # completed_taxIds.append(tax_id)

    # Save the completed taxId to the file
    with open(completed_file, "a") as file:
        file.write(str(tax_id) + "\n")

    # tmp 폴더 삭제
    shutil.rmtree(tmp_folder)

print("작업이 완료되었습니다.")
# print("Completed taxIds:", completed_taxIds)
