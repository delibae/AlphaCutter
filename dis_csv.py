import os
from glob import glob

import pandas as pd
from tqdm import tqdm

# CSV 파일들이 있는 폴더 경로
input_folder = "/runs/users/baehanjin/afdb_files/not_in_proteomes/csv/*.csv"
out_dir = "/runs/users/baehanjin/afdb_files/not_in_proteomes/csv"
out_num = 6
# 분류된 파일들을 저장할 4개의 폴더 경로
output_folders = [f"{out_dir}/{i}" for i in range(out_num)]

# 만약 출력 폴더들이 존재하지 않는다면 생성
for folder in output_folders:
    os.makedirs(folder, exist_ok=True)

# CSV 파일들의 리스트 가져오기
csv_files = glob(input_folder)

# 각 파일을 읽어서 taxId 별로 분류하여 해당 폴더로 이동
for file in csv_files:
    df = pd.read_csv(file)

    # taxId 별로 데이터 분류
    grouped = df.groupby("taxId")

    for tax_id, group_df in tqdm(grouped):
        # 분류된 파일을 저장할 폴더 선택
        output_folder = output_folders[tax_id % 6]

        # 분류된 파일을 해당 폴더에 저장
        new_file_name = f"taxId_{tax_id}.csv"
        new_file_path = os.path.join(output_folder, new_file_name)
        group_df.to_csv(new_file_path, index=False)


print("파일 분류가 완료되었습니다.")
