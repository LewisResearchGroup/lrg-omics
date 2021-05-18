#!/bin/bash
#SBATCH --time=10:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --mem=5000
#SBATCH -J 37a72c8a/home/swacker/workspace/lrg-omics/tests/data/fake/run/37a72c8a-b78e-11eb-a67e-107b44934408/fake.raw



cd /home/swacker/workspace/lrg-omics/tests/data/fake/run/37a72c8a-b78e-11eb-a67e-107b44934408

/usr/bin/time -o /home/swacker/workspace/lrg-omics/tests/data/fake/run/37a72c8a-b78e-11eb-a67e-107b44934408/time.txt -f "%E" maxquant /home/swacker/workspace/lrg-omics/tests/data/fake/run/37a72c8a-b78e-11eb-a67e-107b44934408/mqpar.xml 1>maxquant.out 2>maxquant.err

mv time.txt /home/swacker/workspace/lrg-omics/tests/data/fake/run/37a72c8a-b78e-11eb-a67e-107b44934408/combined/txt/

mv /home/swacker/workspace/lrg-omics/tests/data/fake/run/37a72c8a-b78e-11eb-a67e-107b44934408/combined/txt/* /home/swacker/workspace/lrg-omics/tests/data/fake/result

rm -r /home/swacker/workspace/lrg-omics/tests/data/fake/run/37a72c8a-b78e-11eb-a67e-107b44934408
