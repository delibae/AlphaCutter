import os
from glob import glob

import pandas as pd
from tqdm import tqdm


def merge_csv_files(folder_path, output_file):
    all_data = pd.DataFrame()  # 빈 DataFrame 생성
    empty_files = []  # 행이 없는 CSV 파일 이름을 저장하는 리스트

    # 폴더 내 모든 파일 및 하위 폴더에 접근
    files = glob(folder_path)
    for file in tqdm(files):
        df = pd.read_csv(file)  # CSV 파일 읽기

        if df.empty:
            empty_files.append(os.path.basename(file))  # 행이 없는 파일 이름 저장
        else:
            all_data = pd.concat([all_data, df])  # DataFrame 합치기

    # 합쳐진 DataFrame을 CSV 파일로 저장
    all_data.to_csv(output_file, index=False)

    # # 행이 없는 파일 이름을 리스트로 저장
    # empty_files_output_file = "./empty_files_list.txt"
    # with open(empty_files_output_file, "w") as f:
    #     for file_name in empty_files:
    #         f.write(file_name + "\n")


if __name__ == "__main__":
    folder_path = (
        "/runs/users/baehanjin/afdb_files/alphacutter/in_afdb/*/*.csv"  # 폴더 경로 설정
    )
    output_file = "/runs/users/baehanjin/afdb_files/alphacutter/total/in_proteomes/alphacutter_merged.csv"  # 결과 파일 이름 설정

    merge_csv_files(folder_path, output_file)
