import hashlib
import random
import numpy as np

sha256_inst = hashlib.sha256()
sha256_inst.update("Welcome to Gabriel".encode("utf-8"))
hash_val = sha256_inst.hexdigest()
print(hash_val)

n = 18
random.seed(hash_val)
for i in range(n):
    nlut = []
    for j in range(8):
        nlut.append(random.randrange(16))
    for j in range(8):
        nlut.append((-nlut[j])&15)
    print(nlut)

# sha256_inst.update("Welcome to Margrethe".encode("utf-8"))
# hash_val = sha256_inst.hexdigest()
# print(hash_val)
#
# random.seed(hash_val)
# lut = []
# f = open("LUT_Margrethe.txt", "w")
# for i in range(int(2**18)):
#     current_image = random.randrange(16)
#     lut.append(current_image)
#     f.write(str(current_image)+"\n")
# f.close()
# print(len(lut))
# np_vec = np.array(lut)
# print(np_vec.shape)
# print(np_vec[:100])
# # f = open("LUT_M_list.txt", "w")
# # f.write(str(lut)+"\n")
# # f.close()
# np.save("LUT.npy", np_vec)
# print(lut[:100])