from Crypto.Cipher import AES
import math
import copy
import random
import time
import json
# key = [k1, ..., k512] 0 <= ki <= 15, i = 1,...,512

C0 = bytes([i for i in range(16)])
C1 = bytes([15 - i for i in range(16)])

# Elisabeth-4's NLUTs
S1 = [3, 2, 6, 12, 10, 0, 1, 11, 13, 14, 10, 4, 6, 0, 15, 5]
S2 = [4, 11, 4, 4, 4, 15, 9, 12, 12, 5, 12, 12, 12, 1, 7, 4]
S3 = [11, 10, 12, 2, 2, 11, 13, 14, 5, 6, 4, 14, 14, 5, 3, 2]
S4 = [5, 9, 13, 2, 11, 10, 12, 5, 11, 7, 3, 14, 5, 6, 4, 11]
S5 = [3, 0, 11, 8, 13, 14, 13, 11, 13, 0, 5, 8, 3, 2, 3, 5]
S6 = [8, 13, 12, 12, 3, 15, 12, 7, 8, 3, 4, 4, 13, 1, 4, 9]
S7 = [4, 2, 9, 13, 10, 12, 10, 7, 12, 14, 7, 3, 6, 4, 6, 9]
S8 = [10, 2, 5, 5, 3, 13, 15, 1, 6, 14, 11, 11, 13, 3, 1, 15]

# Elisabeth-b4's NLUTs
bS1 = [8, 12, 12, 9, 11, 11, 8, 15, 8, 4, 4, 7, 5, 5, 8, 1]
bS2 = [11, 3, 1, 2, 12, 3, 11, 12, 5, 13, 15, 14, 4, 13, 5, 4]
bS3 = [5, 7, 8, 0, 12, 4, 10, 5, 11, 9, 8, 0, 4, 12, 6, 11]
bS4 = [12, 12, 10, 0, 13, 1, 7, 7, 4, 4, 6, 0, 3, 15, 9, 9]
bS5 = [9, 12, 8, 15, 13, 13, 11, 8, 7, 4, 8, 1, 3, 3, 5, 8]
bS6 = [11, 14, 6, 13, 10, 4, 2, 3, 5, 2, 10, 3, 6, 12, 14, 13]
bS7 = [0, 3, 15, 15, 9, 5, 2, 7, 0, 13, 1, 1, 7, 11, 14, 9]
bS8 = [0, 11, 0, 5, 3, 0, 10, 0, 0, 5, 0, 11, 13, 0, 6, 0]
bS9 = [6, 14, 10, 6, 11, 9, 2, 15, 10, 2, 6, 10, 5, 7, 14, 1]
bS10 = [10, 8, 11, 12, 4, 12, 0, 0, 6, 8, 5, 4, 12, 4, 0, 0]
bS11 = [6, 13, 7, 11, 6, 12, 5, 7, 10, 3, 9, 5, 10, 4, 11, 9]
bS12 = [4, 2, 2, 12, 7, 6, 12, 6, 12, 14, 14, 4, 9, 10, 4, 10]
bS13 = [3, 5, 8, 9, 9, 2, 7, 14, 13, 11, 8, 7, 7, 14, 9, 2]
bS14 = [2, 6, 14, 1, 1, 3, 14, 4, 14, 10, 2, 15, 15, 13, 2, 12]
bS15 = [0, 2, 8, 6, 8, 4, 10, 1, 0, 14, 8, 10, 8, 12, 6, 15]
bS16 = [11, 3, 5, 11, 4, 13, 5, 14, 5, 13, 11, 5, 12, 3, 11, 2]
bS17 = [4, 11, 4, 5, 3, 1, 9, 13, 12, 5, 12, 11, 13, 15, 7, 3]
bS18 = [1, 9, 12, 6, 10, 10, 8, 15, 15, 7, 4, 10, 6, 6, 8, 1]


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


def Gabriel_PRNG_next(xof_k, xof_r, xof_offset, perm, w_vec):
    new_k = xof_k
    new_r = xof_r
    new_offset = xof_offset
    for i in range(110):
        r, new_k, new_r, new_offset = XOF_int(new_k, new_r, new_offset, i, 512)
        ww, new_k, new_r, new_offset = XOF_bits(new_k, new_r, new_offset, 4)
        tmp = perm[i]
        perm[i] = perm[r]
        perm[r] = tmp
        w_vec[perm[i]] = (w_vec[perm[i]] + ww) & 15
    return new_k, new_r, new_offset


def h_func_L(x1, x2, x3, x4):
    # h function for g_L
    a = (x1 + x2) & 15
    b = (x2 + x3) & 15
    c = (x3 + x4) & 15
    d = (x4 + x1) & 15

    s1a = S1[a]
    s2b = S2[b]
    s3c = S3[c]
    s4d = S4[d]

    tmp1 = S5[(x1 + s2b + s3c) & 15]
    tmp2 = S6[(x2 + s3c + s4d) & 15]
    tmp3 = S7[(x3 + s4d + s1a) & 15]
    tmp4 = S8[(x4 + s1a + s2b) & 15]

    return (tmp1 + tmp2 + tmp3 + tmp4) & 15


def h_func_R(x1, x2, x3, x4, x5, x6):
    # h function for g_R
    x2 = (x2 + x1) & 15
    x4 = (x4 + x3) & 15
    x6 = (x6 + x5) & 15

    y1 = bS1[x1]
    y2 = bS2[x2]
    y3 = bS3[x3]
    y4 = bS4[x4]
    y5 = bS5[x5]
    y6 = bS6[x6]

    z1 = bS7[(y6 + y1 + x3) & 15]
    z2 = bS8[(y5 + y2 + x4) & 15]
    z3 = bS9[(y2 + y3 + x5) & 15]
    z4 = bS10[(y1 + y4 + x6) & 15]
    z5 = bS11[(y4 + y5 + x1) & 15]
    z6 = bS12[(y3 + y6 + x2) & 15]

    t1 = (z1 + z2 + z3 + x6) & 15
    t2 = (z2 + z4 + x5) & 15
    t3 = (z3 + z4 + y1 + x4) & 15
    t4 = (z4 + z5 + z6 + x2) & 15
    t5 = (z5 + z1 + x1) & 15
    t6 = (z6 + z1 + y4 + x3) & 15

    return (bS13[t1] + bS14[t2] + bS15[t3] + bS16[t4] + bS17[t5] + bS18[t6] + 0) & 15


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
    test_key = [
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

    test_key = test_key + test_key
    print(len(test_key))

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
        fault_pos = random.randint(0, 511)
        # For other bit fault, the process is the same. The only difference is the number of \delta h table
        fault_es_k[fault_pos] = (fault_es_k[fault_pos] + random.randint(1, 15)) & 15
        es_perm = [i for i in range(512)]
        es_w_vec = [0 for i in range(512)]
        candidate_pos = set([i for i in range(512)])
        count = 0
        while len(candidate_pos) > 1:
            XOF_K, XOF_R, XOF_offset = Gabriel_PRNG_next(XOF_K, XOF_R, XOF_offset, es_perm, es_w_vec)
            es_z = 0
            fault_es_z = 0
            for j in range(18):
                if j < 8:
                    es_z += (h_func_L(
                        (es_k[es_perm[5 * j]] + es_w_vec[es_perm[5 * j]]) & 15,
                        (es_k[es_perm[5 * j + 1]] + es_w_vec[es_perm[5 * j + 1]]) & 15,
                        (es_k[es_perm[5 * j + 2]] + es_w_vec[es_perm[5 * j + 2]]) & 15,
                        (es_k[es_perm[5 * j + 3]] + es_w_vec[es_perm[5 * j + 3]]) & 15,
                    ) + (es_k[es_perm[5 * j + 4]] + es_w_vec[es_perm[5 * j + 4]]))
                    fault_es_z += (h_func_L(
                        (fault_es_k[es_perm[5 * j]] + es_w_vec[es_perm[5 * j]]) & 15,
                        (fault_es_k[es_perm[5 * j + 1]] + es_w_vec[es_perm[5 * j + 1]]) & 15,
                        (fault_es_k[es_perm[5 * j + 2]] + es_w_vec[es_perm[5 * j + 2]]) & 15,
                        (fault_es_k[es_perm[5 * j + 3]] + es_w_vec[es_perm[5 * j + 3]]) & 15,
                    ) + (fault_es_k[es_perm[5 * j + 4]] + es_w_vec[es_perm[5 * j + 4]]))
                else:
                    es_z += (h_func_R(
                        (es_k[es_perm[7 * j]] + es_w_vec[es_perm[7 * j]]) & 15,
                        (es_k[es_perm[7 * j + 1]] + es_w_vec[es_perm[7 * j + 1]]) & 15,
                        (es_k[es_perm[7 * j + 2]] + es_w_vec[es_perm[7 * j + 2]]) & 15,
                        (es_k[es_perm[7 * j + 3]] + es_w_vec[es_perm[7 * j + 3]]) & 15,
                        (es_k[es_perm[7 * j + 4]] + es_w_vec[es_perm[7 * j + 4]]) & 15,
                        (es_k[es_perm[7 * j + 5]] + es_w_vec[es_perm[7 * j + 5]]) & 15
                    ) + (es_k[es_perm[7 * j + 6]] + es_w_vec[es_perm[7 * j + 6]]))
                    fault_es_z += (h_func_R(
                        (fault_es_k[es_perm[7 * j]] + es_w_vec[es_perm[7 * j]]) & 15,
                        (fault_es_k[es_perm[7 * j + 1]] + es_w_vec[es_perm[7 * j + 1]]) & 15,
                        (fault_es_k[es_perm[7 * j + 2]] + es_w_vec[es_perm[7 * j + 2]]) & 15,
                        (fault_es_k[es_perm[7 * j + 3]] + es_w_vec[es_perm[7 * j + 3]]) & 15,
                        (fault_es_k[es_perm[7 * j + 4]] + es_w_vec[es_perm[7 * j + 4]]) & 15,
                        (fault_es_k[es_perm[7 * j + 5]] + es_w_vec[es_perm[7 * j + 5]]) & 15
                    ) + (fault_es_k[es_perm[7 * j + 6]] + es_w_vec[es_perm[7 * j + 6]]))
            es_z = es_z & 15
            fault_es_z = fault_es_z & 15
            count += 1
            # print(count, len(candidate_pos))
            if es_z != fault_es_z:
                candidate_pos = candidate_pos.intersection(set(es_perm[:110]))
            else:
                for j in range(18):
                    if j < 8 and es_perm[5 * j + 4] in candidate_pos:
                        candidate_pos.remove(es_perm[5 * j + 4])
                    if j >= 8 and es_perm[7 * j + 6] in candidate_pos:
                        candidate_pos.remove(es_perm[7 * j + 6])
        times_count += count
    record_t2 = time.time()
    print("Total time:", record_t2-record_t1)
    # print("Averaged time:", (t1-t2)/n)
    print("Averaged count:", times_count/n)

    # # generate normal and faulted keystream
    # delta_val = 15
    # test_IV = [0 for i in range(16)]

    # XOF_K = encrypt_aes(C0, bytes(test_IV))
    # XOF_R = encrypt_aes(C1, XOF_K)
    # XOF_offset = 0

    # es_k = copy.deepcopy(test_key)
    # fault_es_k = copy.deepcopy(test_key)
    # fault_pos = 0
    # # For other bit fault, the process is the same. The only difference is the number of \delta h table
    # fault_es_k[fault_pos] = (fault_es_k[fault_pos] + delta_val) & 15
    # es_perm = [i for i in range(512)]
    # es_w_vec = [0 for i in range(512)]
    # normal_key_stream = []
    # fault_key_stream = []
    # dif_stream = []
    # useful_pairs = []
    # f = open("tmp_result_file/Gabriel_useful_dif_information_0_80000_%s.txt"%delta_val, "w")
    # new_test_out = []
    # for i in range(80000):
    #     XOF_K, XOF_R, XOF_offset = Gabriel_PRNG_next(XOF_K, XOF_R, XOF_offset, es_perm, es_w_vec)
    #     es_z = 0
    #     fault_es_z = 0
    #     for j in range(18):
    #         if j < 8:
    #             es_z += (h_func_L(
    #                 (es_k[es_perm[5 * j]] + es_w_vec[es_perm[5 * j]]) & 15,
    #                 (es_k[es_perm[5 * j + 1]] + es_w_vec[es_perm[5 * j + 1]]) & 15,
    #                 (es_k[es_perm[5 * j + 2]] + es_w_vec[es_perm[5 * j + 2]]) & 15,
    #                 (es_k[es_perm[5 * j + 3]] + es_w_vec[es_perm[5 * j + 3]]) & 15,
    #             ) + (es_k[es_perm[5 * j + 4]] + es_w_vec[es_perm[5 * j + 4]]))
    #             fault_es_z += (h_func_L(
    #                 (fault_es_k[es_perm[5 * j]] + es_w_vec[es_perm[5 * j]]) & 15,
    #                 (fault_es_k[es_perm[5 * j + 1]] + es_w_vec[es_perm[5 * j + 1]]) & 15,
    #                 (fault_es_k[es_perm[5 * j + 2]] + es_w_vec[es_perm[5 * j + 2]]) & 15,
    #                 (fault_es_k[es_perm[5 * j + 3]] + es_w_vec[es_perm[5 * j + 3]]) & 15,
    #             ) + (fault_es_k[es_perm[5 * j + 4]] + es_w_vec[es_perm[5 * j + 4]]))
    #         else:
    #             es_z += (h_func_R(
    #                 (es_k[es_perm[7 * j]] + es_w_vec[es_perm[7 * j]]) & 15,
    #                 (es_k[es_perm[7 * j + 1]] + es_w_vec[es_perm[7 * j + 1]]) & 15,
    #                 (es_k[es_perm[7 * j + 2]] + es_w_vec[es_perm[7 * j + 2]]) & 15,
    #                 (es_k[es_perm[7 * j + 3]] + es_w_vec[es_perm[7 * j + 3]]) & 15,
    #                 (es_k[es_perm[7 * j + 4]] + es_w_vec[es_perm[7 * j + 4]]) & 15,
    #                 (es_k[es_perm[7 * j + 5]] + es_w_vec[es_perm[7 * j + 5]]) & 15
    #             ) + (es_k[es_perm[7 * j + 6]] + es_w_vec[es_perm[7 * j + 6]]))
    #             fault_es_z += (h_func_R(
    #                 (fault_es_k[es_perm[7 * j]] + es_w_vec[es_perm[7 * j]]) & 15,
    #                 (fault_es_k[es_perm[7 * j + 1]] + es_w_vec[es_perm[7 * j + 1]]) & 15,
    #                 (fault_es_k[es_perm[7 * j + 2]] + es_w_vec[es_perm[7 * j + 2]]) & 15,
    #                 (fault_es_k[es_perm[7 * j + 3]] + es_w_vec[es_perm[7 * j + 3]]) & 15,
    #                 (fault_es_k[es_perm[7 * j + 4]] + es_w_vec[es_perm[7 * j + 4]]) & 15,
    #                 (fault_es_k[es_perm[7 * j + 5]] + es_w_vec[es_perm[7 * j + 5]]) & 15
    #             ) + (fault_es_k[es_perm[7 * j + 6]] + es_w_vec[es_perm[7 * j + 6]]))
    #     es_z = es_z & 15
    #     fault_es_z = fault_es_z & 15
    #     normal_key_stream.append(es_z)
    #     fault_key_stream.append(fault_key_stream)
    #     dif_stream.append((es_z - fault_es_z) & 15)
    #     if fault_pos in es_perm[0:40] and es_perm.index(fault_pos) % 5 != 4:
    #         begin_index = (es_perm.index(fault_pos) // 5) * 5
    #         useful_pairs.append((i, set(es_perm[begin_index: begin_index+4])))
    #         act_es_w_vec = [es_w_vec[es_perm[t]] for t in range(begin_index, begin_index+4)]
    #         f.write(str(i) + "\t" + str(es_perm[begin_index: begin_index+4]) + "\t" + str(act_es_w_vec) + "\t" + str((es_z - fault_es_z) & 15) + "\n")
    # f.close()
    # print(len(useful_pairs))
    # # useful_pairs = read_useful_pair("tmp_result_file/Gabriel_useful_dif_information_0_100000_15.txt")
    # # print(len(useful_pairs), useful_pairs[0])
    # tt1 = time.time()
    # # search for the same pair as beginning point
    # closest_pairs = []
    # cor_dis = 4
    # for i in range(len(useful_pairs)):
    #     for j in range(i + 1, len(useful_pairs)):
    #         new_dis = 4 - len(useful_pairs[i][1].intersection(useful_pairs[j][1]))
    #         if new_dis < cor_dis:
    #             closest_pairs = [(i, j)]
    #             cor_dis = new_dis
    #         elif new_dis == cor_dis:
    #             closest_pairs.append((i, j))
    # # #
    # # use greedy algorithm to search sub-optimal merge path
    # print(len(closest_pairs), cor_dis)
    # # print(closest_pairs[:20])
    # len_try = min((200, len(closest_pairs)))
    # # cor_dis = 1
    # print("1ST Time used:", time.time() - tt1)
    # target_pair = [10, (0 , 0)]
    # for closest_pair in closest_pairs[:len_try]:
    #     maximum_size = 3
    #     tmp_useful_pairs = useful_pairs.copy()
    #     tt2 = time.time()
    #     print(closest_pair, len(tmp_useful_pairs))
    #     tmp_set = tmp_useful_pairs[closest_pair[0]][1].union(tmp_useful_pairs[closest_pair[1]][1])
    #     merge_path = [tmp_useful_pairs[closest_pair[0]][0], tmp_useful_pairs[closest_pair[1]][0]]
    #     add_length = [4, cor_dis]
    #     tmp1 = tmp_useful_pairs[closest_pair[0]]
    #     tmp2 = tmp_useful_pairs[closest_pair[1]]
    #     tmp_useful_pairs.remove(tmp1)
    #     tmp_useful_pairs.remove(tmp2)
    #     more_than_one_pos = []
    #     if cor_dis > 1:
    #         more_than_one_pos.append((0, tmp_useful_pairs[closest_pair[1]]))
    #     print(tmp_set)
    #     count = 0
    #     while len(tmp_set) < 512 and len(tmp_useful_pairs) > 1:
    #         count += 1
    #         tmp_dis = 4
    #         tmp_index = 1
    #         for i in range(1, len(tmp_useful_pairs)):
    #             new_dis = 4 - len(tmp_set.intersection(tmp_useful_pairs[i][1]))
    #             if new_dis == 0:
    #                 tmp_dis = new_dis
    #                 tmp_index = i
    #                 break
    #             if new_dis < tmp_dis:
    #                 tmp_dis = new_dis
    #                 tmp_index = i
    #         if tmp_dis > 1:
    #             more_than_one_pos.append((count, tmp_useful_pairs[tmp_index]))
    #             maximum_size += (tmp_dis-1)
    #         tmp_set = tmp_set.union(tmp_useful_pairs[tmp_index][1])
    #         merge_path.append(tmp_useful_pairs[tmp_index][0])
    #         add_length.append(tmp_dis)
    #         tmp_useful_pairs.remove(tmp_useful_pairs[tmp_index])
    #     print(len(tmp_set), maximum_size)
    #     if maximum_size < target_pair[0]:
    #         target_pair = [maximum_size, closest_pair]
    #     print("Time used:", time.time()-tt2)
    #     # print(len(more_than_one_pos), more_than_one_pos)
    #     if len(tmp_useful_pairs) > 1:
    #         for tmp in tmp_useful_pairs[1:]:
    #             merge_path.append(tmp[0])
    #             add_length.append(0)
    #         print("Left pairs: ", len(tmp_useful_pairs))
    #     f = open("Gab_tmp_result/Gabriel_merge_path_0_80000_"+str(closest_pair)+".txt", "w")
    #     for i in range(len(merge_path)):
    #         f.write(str(merge_path[i])+" "+str(add_length[i])+"\n")
    #     f.close()
    #     print(target_pair)




