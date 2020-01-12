import os
import shutil

output_dir = "final_data"
input_dirs = ["data", "data1", "old_data"]

subgroups = []

# initialize output dir structure
os.makedirs(output_dir)
for d in os.listdir(input_dirs[0]):
    p = "{}/{}".format(output_dir, d)
    os.makedirs(p)
    subgroups.append(d)

for sg in subgroups:
    count = 0

    for d in input_dirs:
        path = "{}/{}".format(d, sg)
        for f in os.listdir(path):
            output_filename = "{}/{}/{:04d}.jpg".format(output_dir, sg, count)
            shutil.copy("{}/{}".format(path, f), output_filename)
            count += 1
