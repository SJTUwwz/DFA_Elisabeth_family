from Crypto.Cipher import AES
import math
import copy
import random
import time
import json
# key = [k1, ..., k2048] ki \in [0, 1], i = 1,...,2048

C0 = bytes([i for i in range(16)])
C1 = bytes([15 - i for i in range(16)])


def bin_list_to_int(bin_l):
    result = 0
    for i in range(len(bin_l)):
        result += bin_l[i] * 2**i
    return int(result)


def int_to_4bin(num):
    result_l = [0, 0, 0, 0]
    tmp = num
    for i in range(4):
        result_l[3-i] = int(tmp//(2**(3-i)))
        tmp = tmp % (2**(3-i))
    return result_l


f = open("LUT_M_list.txt", "r")
table_g = json.loads(f.readlines()[0].rstrip("\n"))
f.close()
print(table_g[:10], len(table_g))


def encrypt_aes(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(plaintext)


def XOF_update(xof_k):
    return encrypt_aes(C0, xof_k), encrypt_aes(C1, xof_k), 0


# generate an n-bit integer
def XOF_bits(xof_k, xof_r, offset, n):
    u = 0
    r = 0
    s = 0
    p = 0
    res = 0
    new_k = xof_k
    new_r = xof_r
    new_offset = offset
    tmp_n = n
    while tmp_n > 0:
        if new_offset == 128:
            new_k, new_r, new_offset = XOF_update(new_k)
        u = new_offset % 8
        r = 8 - u
        s = min(r, tmp_n)
        res ^= ((new_r[new_offset >> 3] >> u) % (1 << s)) << p
        p += s
        tmp_n -= s
        new_offset += s
    return res, new_k, new_r, new_offset


# generate an integer a <= x < b
def XOF_int(xof_k, xof_r, offset, a, b):
    n = math.ceil(math.log(b-a, 2))
    r = b-a
    new_k = xof_k
    new_r = xof_r
    new_offset = offset
    while r >= b-a:
        r, new_k, new_r, new_offset = XOF_bits(new_k, new_r, new_offset, n)
    return a+r, new_k, new_r, new_offset


def Margrethe_PRNG_next(xof_k, xof_r, xof_offset, perm, w_vec):
    new_k = xof_k
    new_r = xof_r
    new_offset = xof_offset
    for i in range(308):
        r, new_k, new_r, new_offset = XOF_int(new_k, new_r, new_offset, i, 2048)
        ww, new_k, new_r, new_offset = XOF_bits(new_k, new_r, new_offset, 1)
        tmp = perm[i]
        perm[i] = perm[r]
        perm[r] = tmp
        w_vec[perm[i]] = w_vec[perm[i]] ^ ww
    return new_k, new_r, new_offset


def read_useful_pair(filename):
    f = open(filename, "r")
    result_pairs = []
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        tmp_pair = line.split("\t")
        result_pairs.append((int(tmp_pair[0]), set(json.loads(tmp_pair[1]))))
    return result_pairs


if __name__ == "__main__":
    seed_key = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
    ]

    seed_key = seed_key + seed_key
    test_key = []
    for item in seed_key:
        test_key += int_to_4bin(item)
    # print(len(test_key), test_key)

    # A simple method to check the fault_pos and compute the average times
    n = 100000
    times_count = 0
    record_t1 = time.time()
    for tmp in range(n):
        test_IV = [random.randint(0, 15) for i in range(16)]
    
        XOF_K = encrypt_aes(C0, bytes(test_IV))
        XOF_R = encrypt_aes(C1, XOF_K)
        XOF_offset = 0
    
        es_k = copy.deepcopy(test_key)
        fault_es_k = copy.deepcopy(test_key)
        fault_pos = random.randint(0, 2047)
        # For other bit fault, the process is the same. The only difference is the number of \delta h table
        fault_es_k[fault_pos] = fault_es_k[fault_pos] ^ 1
        es_perm = [i for i in range(2048)]
        es_w_vec = [0 for i in range(2048)]
        candidate_pos = set([i for i in range(2048)])
        count = 0
        while len(candidate_pos) > 1:
            XOF_K, XOF_R, XOF_offset = Margrethe_PRNG_next(XOF_K, XOF_R, XOF_offset, es_perm, es_w_vec)
            es_z = 0
            fault_es_z = 0
            for j in range(14):
                used_seg1 = []
                used_seg2 = []
                for ii in range(18):
                    used_seg1.append(es_k[es_perm[22 * j + ii]] ^ es_w_vec[es_perm[22 * j + ii]])
                for jj in range(18, 22):
                    used_seg2.append(es_k[es_perm[22 * j + jj]] ^ es_w_vec[es_perm[22 * j + jj]])
                es_z += (table_g[bin_list_to_int(used_seg1)] + bin_list_to_int(used_seg2)) & 15
    
                used_seg3 = []
                used_seg4 = []
                for ii in range(18):
                    used_seg3.append(fault_es_k[es_perm[22 * j + ii]] ^ es_w_vec[es_perm[22 * j + ii]])
                for jj in range(18, 22):
                    used_seg4.append(fault_es_k[es_perm[22 * j + jj]] ^ es_w_vec[es_perm[22 * j + jj]])
                fault_es_z += (table_g[bin_list_to_int(used_seg3)] + bin_list_to_int(used_seg4)) & 15
            es_z = es_z & 15
            fault_es_z = fault_es_z & 15
            count += 1
            # print(count, len(candidate_pos))
            if es_z != fault_es_z:
                candidate_pos = candidate_pos.intersection(set(es_perm[:308]))
            else:
                for j in range(14):
                    for jj in range(18, 22):
                        if es_perm[22 * j +jj] in candidate_pos:
                            candidate_pos.remove(es_perm[22 * j +jj])
        times_count += count
    record_t2 = time.time()
    print("Total time:", record_t2-record_t1)
    print("Averaged count:", times_count/n)

    # # simulate the known keys by multiple faults
    # random.seed(0)
    # # # tmp_set = set(random.sample([i for i in range(2048)], 699))
    # tmp_set = set(random.sample([i for i in range(2048)], 699))
    # # print(list(tmp_set))
    # key_value = [test_key[i] for i in tmp_set]
    # print([key_value])
    # # generate normal and faulted keystream
    # test_IV = [0 for i in range(16)]

    # XOF_K = encrypt_aes(C0, bytes(test_IV))
    # XOF_R = encrypt_aes(C1, XOF_K)
    # XOF_offset = 0

    # es_k = copy.deepcopy(test_key)
    # fault_es_k = copy.deepcopy(test_key)
    # rest_pos = set([i for i in range(2048)]).difference(tmp_set)
    # # print(rest_pos)
    # fault_pos = random.choice(list(rest_pos))
    # print(fault_pos)
    # fault_es_k[fault_pos] = fault_es_k[fault_pos] ^ 1
    # es_perm = [i for i in range(2048)]
    # es_w_vec = [0 for i in range(2048)]
    # # normal_key_stream = []
    # # fault_key_stream = []
    # # dif_stream = []
    # # useful_pairs = []
    # # f = open("Mar_tmp_result/Margrethe_useful_dif_information_200000_0_699.txt", "w")
    # # new_test_out = []
    # # ttime1 = time.time()
    # # for i in range(200000):
    # #     XOF_K, XOF_R, XOF_offset = Margrethe_PRNG_next(XOF_K, XOF_R, XOF_offset, es_perm, es_w_vec)
    # #     es_z = 0
    # #     fault_es_z = 0
    # #     for j in range(14):
    # #         used_seg1 = []
    # #         used_seg2 = []
    # #         for ii in range(18):
    # #             used_seg1.append(es_k[es_perm[22 * j + ii]] ^ es_w_vec[es_perm[22 * j + ii]])
    # #         for jj in range(18, 22):
    # #             used_seg2.append(es_k[es_perm[22 * j + jj]] ^ es_w_vec[es_perm[22 * j + jj]])
    # #         es_z += (table_g[bin_list_to_int(used_seg1)] + bin_list_to_int(used_seg2)) & 15

    # #         used_seg3 = []
    # #         used_seg4 = []
    # #         for ii in range(18):
    # #             used_seg3.append(fault_es_k[es_perm[22 * j + ii]] ^ es_w_vec[es_perm[22 * j + ii]])
    # #         for jj in range(18, 22):
    # #             used_seg4.append(fault_es_k[es_perm[22 * j + jj]] ^ es_w_vec[es_perm[22 * j + jj]])
    # #         fault_es_z += (table_g[bin_list_to_int(used_seg3)] + bin_list_to_int(used_seg4)) & 15
    # #     es_z = es_z & 15
    # #     fault_es_z = fault_es_z & 15
    # #     normal_key_stream.append(es_z)
    # #     fault_key_stream.append(fault_key_stream)
    # #     dif_stream.append((es_z - fault_es_z) & 15)
    # #     if fault_pos in es_perm[0:308] and es_perm.index(fault_pos) % 22 < 18:
    # #         begin_index = (es_perm.index(fault_pos) // 22) * 22
    # #         useful_pairs.append((i, set(es_perm[begin_index: begin_index+18])))
    # #         act_es_w_vec = [es_w_vec[es_perm[t]] for t in range(begin_index, begin_index+18)]
    # #         f.write(str(i) + "\t" + str(es_perm[begin_index: begin_index+18]) + "\t" + str(act_es_w_vec) + "\t" + str((es_z - fault_es_z) & 15) + "\n")
    # # f.close()
    # # print(len(useful_pairs))
    # # ttime2 = time.time()
    # # print(ttime2-ttime1)

    # useful_pairs = read_useful_pair("Mar_tmp_result/Margrethe_useful_dif_information_200000_0_699.txt")
    # print(len(useful_pairs), useful_pairs[0])
    # #
    # # # search for the same pair as beginning point
    # # zero_pair = []
    # # for i in range(len(useful_pairs)):
    # #     for j in range(i+1, len(useful_pairs)):
    # #         if len(useful_pairs[i][1].symmetric_difference(useful_pairs[j][1])) == 0:
    # #             zero_pair.append((i, j, useful_pairs[i][0], useful_pairs[j][0], useful_pairs[i][1]))
    # # print(len(zero_pair))
    # # print(zero_pair)
    # #
    # # choose_pair = 1
    # # useful_pairs.remove((zero_pair[choose_pair][2], zero_pair[choose_pair][4]))
    # # useful_pairs.insert(0, (zero_pair[choose_pair][2], zero_pair[choose_pair][4]))
    # # #
    # # use greedy algorithm to search sub-optimal merge path

    # # # tmp_set = useful_pairs[0][1]
    # # merge_path = []
    # # add_length = []
    # # more_than_one_pos = []
    # # # print(tmp_set)
    # # count = 0
    # # while len(tmp_set) < 2048 and len(useful_pairs) > 1:
    # #     count += 1
    # #     tmp_dis = 18
    # #     tmp_index = 1
    # #     for i in range(1, len(useful_pairs)):
    # #         new_dis = 18 - len(tmp_set.intersection(useful_pairs[i][1]))
    # #         if new_dis == 0:
    # #             tmp_dis = new_dis
    # #             tmp_index = i
    # #             break
    # #         if new_dis < tmp_dis:
    # #             tmp_dis = new_dis
    # #             tmp_index = i
    # #     if tmp_dis > 1:
    # #         more_than_one_pos.append((count, useful_pairs[tmp_index]))
    # #     tmp_set = tmp_set.union(useful_pairs[tmp_index][1])
    # #     merge_path.append(useful_pairs[tmp_index][0])
    # #     add_length.append(tmp_dis)
    # #     # if count <= 50:
    # #     #     print(count, tmp_dis-4, len(tmp_set))
    # #     # if count > 50:
    # #     #     break
    # #     useful_pairs.remove(useful_pairs[tmp_index])
    # # print(len(tmp_set))
    # # # print(len(more_than_one_pos), more_than_one_pos)
    # # if len(useful_pairs) > 1:
    # #     for tmp in useful_pairs[1:]:
    # #         merge_path.append(tmp[0])
    # #         add_length.append(0)
    # #     print("Left pairs: ", len(useful_pairs))
    # # f = open("Mar_tmp_result/Margrethe_merge_path_200000.txt", "w")
    # # for i in range(len(merge_path)):
    # #     f.write(str(merge_path[i])+" "+str(add_length[i])+"\n")
    # # f.close()

    # # new greedy algorithm
    # tt1 = time.time()
    # closest_index = []
    # cor_dis = 18
    # for i in range(len(useful_pairs)):
    #     new_dis = 18 - len(tmp_set.intersection(useful_pairs[i][1]))
    #     if new_dis < cor_dis:
    #         print(len(closest_index), new_dis)
    #         closest_index = [i]
    #         cor_dis = new_dis
    #     elif new_dis == cor_dis:
    #         closest_index.append(i)

    # # use greedy algorithm to search sub-optimal merge path
    # print(len(closest_index), cor_dis)
    # # print(closest_pairs[:20])
    # len_try = min((20, len(closest_index)))
    # # cor_dis = 1
    # print("1ST Time used:", time.time() - tt1)
    # for ind in closest_index[0:len_try]:
    #     tmp_useful_pairs = useful_pairs.copy()
    #     tt2 = time.time()
    #     print(ind, len(tmp_useful_pairs))
    #     new_tmp_set = tmp_set.union(tmp_useful_pairs[ind][1])
    #     merge_path = []
    #     add_length = [cor_dis]
    #     tmp = tmp_useful_pairs[ind]
    #     tmp_useful_pairs.remove(tmp)
    #     # print(new_tmp_set)
    #     count = 0
    #     while len(new_tmp_set) < 2048 and len(tmp_useful_pairs) > 1:
    #         count += 1
    #         tmp_dis = 18
    #         tmp_index = 1
    #         for i in range(1, len(tmp_useful_pairs)):
    #             new_dis = 18 - len(new_tmp_set.intersection(tmp_useful_pairs[i][1]))
    #             if new_dis == 0:
    #                 tmp_dis = new_dis
    #                 tmp_index = i
    #                 break
    #             if new_dis < tmp_dis:
    #                 tmp_dis = new_dis
    #                 tmp_index = i
    #         new_tmp_set = new_tmp_set.union(tmp_useful_pairs[tmp_index][1])
    #         merge_path.append(tmp_useful_pairs[tmp_index][0])
    #         add_length.append(tmp_dis)
    #         tmp_useful_pairs.remove(tmp_useful_pairs[tmp_index])
    #     print(len(new_tmp_set))
    #     print("Time used:", time.time()-tt2)
    #     if len(tmp_useful_pairs) > 1:
    #         for tmp in tmp_useful_pairs[1:]:
    #             merge_path.append(tmp[0])
    #             add_length.append(0)
    #         print("Left pairs: ", len(tmp_useful_pairs))
    #     f = open("Mar_tmp_result/Margrethe_merge_path_200000_0_699_"+str(ind)+".txt", "w")
    #     for i in range(len(merge_path)):
    #         f.write(str(merge_path[i])+" "+str(add_length[i])+"\n")
    #     f.close()