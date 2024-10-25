import os
import argparse
import shutil
import random

parser = argparse.ArgumentParser(
    description="Divide all patches to training/validation/test sets"
)
parser.add_argument(
    "--src_dir",
    default="../../datasets/SIDD_Small_patches/train",
    type=str,
    help="Directory for all patches",
)
parser.add_argument(
    "--val_dir",
    default="../../datasets/SIDD_Small_patches/val",
    type=str,
    help="Directory for validation sets",
)
parser.add_argument(
    "--test_dir",
    default="../../datasets/SIDD_Small_patches/test",
    type=str,
    help="Directory for test sets",
)
parser.add_argument(
    "--ratio", default="8:1:1", help="training/validation/test ratio (n:m:l)"
)
parser.add_argument("--num_cores", default=10, type=int, help="Number of CPU Cores")

args = parser.parse_args()

src_dir = args.src_dir
val_dir = args.val_dir
test_dir = args.test_dir
ratio = args.ratio
NUM_CORES = args.num_cores

val_noisy_dir = os.path.join(val_dir, "input")
val_clean_dir = os.path.join(val_dir, "groundtruth")

test_noisy_dir = os.path.join(test_dir, "input")
test_clean_dir = os.path.join(test_dir, "groundtruth")

if os.path.exists(val_dir):
    os.system("rm -r {}".format(val_dir))

if os.path.exists(test_dir):
    os.system("rm -r {}".format(test_dir))

os.makedirs(val_noisy_dir)
os.makedirs(val_clean_dir)

os.makedirs(test_noisy_dir)
os.makedirs(test_clean_dir)

filenames = os.listdir(os.path.join(src_dir, "input"))
random.shuffle(filenames)

val_noisy_files, val_clean_files = [], []
test_noisy_files, test_clean_files = [], []
total_len = len(filenames)

ratio_train, ratio_val, ratio_test = map(int, ratio.split(":"))
val_idx = total_len * ratio_train // 10

for idx, file in enumerate(filenames[val_idx:]):
    gt_file = os.path.join(src_dir, "groundtruth", file)
    input_file = os.path.join(src_dir, "input", file)
    filename = os.path.split(gt_file)[-1]
    print(filename)

    if idx < total_len * ratio_val // 10:
        shutil.move(input_file, os.path.join(val_noisy_dir, filename))
        shutil.move(gt_file, os.path.join(val_clean_dir, filename))
    else:
        shutil.move(input_file, os.path.join(test_noisy_dir, filename))
        shutil.move(gt_file, os.path.join(test_clean_dir, filename))
