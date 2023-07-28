import hashlib


def file_hashes_match(file_path1, file_path2):
    # 파일 1의 해시 계산
    with open(file_path1, "rb") as file1:
        hash1 = hashlib.sha256(file1.read()).hexdigest()

    # 파일 2의 해시 계산
    with open(file_path2, "rb") as file2:
        hash2 = hashlib.sha256(file2.read()).hexdigest()

    # 두 파일의 해시 값 비교
    if hash1 == hash2:
        return True
    else:
        return False


if __name__ == "__main__":
    file1_path = "./tmp/AFCT-OUT_summary.csv"
    file2_path = "./AFCT-OUT_summary.csv"

    if file_hashes_match(file1_path, file2_path):
        print("두 파일이 완벽히 일치합니다.")
    else:
        print("두 파일이 일치하지 않습니다.")
