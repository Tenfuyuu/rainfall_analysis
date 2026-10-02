import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--input",
required=True, help="path to daily_HKO_RF_ALL.csv")
parser.add_argument("--out",
required=True, help="output folder")
args=parser.parse_args()

figures_dir = os.path.join(args.out, "figures")
os.makedirs(figures_dir, exist_ok=True)