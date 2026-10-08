import os
pwd = os.path.join(os.getcwd(),'images')
os.environ["KAGGLEHUB_CACHE"] = pwd

import kagglehub

path = kagglehub.dataset_download("joebeachcapital/realwaste")

print("Path to dataset files:", path)

path = kagglehub.dataset_download("vencerlanz09/bottle-synthetic-images-dataset")

print("Path to dataset files:", path)
