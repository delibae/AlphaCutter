#!/bin/bash -l

folder_num=$1  # 커맨드라인에서 첫 번째 인자를 folder_num 변수에 저장

#SBATCH --partition=single
#SBATCH --job-name=alpha${folder_num}  # job name에 folder_num을 추가
#SBATCH --time=UNLIMITED
#SBATCH  --nodelist=pop4
##SBATCH --gres-flags=enforce-binding
#SBATCH --output ./logs/slurm2-%x.log   
#SBATCH --error ./logs/slurm2-%x.log   

##SBATCH   --gres=gpu:1
##SBATCH           --nodes   1
##SBATCH --ntasks-per-node   1
#SBATCH   --cpus-per-task   30
##SBATCH   --gpus-per-task   1

date
source "/runs/users/baehanjin/apps/anaconda3/etc/profile.d/conda.sh"
conda activate AlphaCutter

python /runs/users/baehanjin/work/AlphaCutter/execute_par2.py --folder_num=${folder_num}  # execute_par2.py에 folder_num을 인자로 전달
date
