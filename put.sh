#!/bin/bash

for i in {0..5}; do
    sbatch --job-name=alpha${i} --output=./logs/slurm2-alpha${i}.log --error=./logs/slurm2-alpha${i}.log alphacutter.slurm $i
done