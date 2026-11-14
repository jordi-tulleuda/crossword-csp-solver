import random

input_file = "./MaterialsPractica/diccionari_A.txt"
output_file = "./MaterialsPractica/diccionari_A_50k.txt"

with open(input_file, "r") as infile, \
     open(output_file, "w") as outfile:

    for line in infile:
        if random.random() < 0.085:
            outfile.write(line)

print("Done!")
print(f"Created: {output_file}")