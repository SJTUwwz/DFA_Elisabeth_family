from Crypto.Cipher import AES
import math
import copy
import random
import time
# key = [k1, ..., k256] 0 <= ki <= 15, i = 1,...,256

C0 = bytes([i for i in range(16)])
C1 = bytes([15 - i for i in range(16)])
S1 = [3, 2, 6, 12, 10, 0, 1, 11, 13, 14, 10, 4, 6, 0, 15, 5]
S2 = [4, 11, 4, 4, 4, 15, 9, 12, 12, 5, 12, 12, 12, 1, 7, 4]
S3 = [11, 10, 12, 2, 2, 11, 13, 14, 5, 6, 4, 14, 14, 5, 3, 2]
S4 = [5, 9, 13, 2, 11, 10, 12, 5, 11, 7, 3, 14, 5, 6, 4, 11]
S5 = [3, 0, 11, 8, 13, 14, 13, 11, 13, 0, 5, 8, 3, 2, 3, 5]
S6 = [8, 13, 12, 12, 3, 15, 12, 7, 8, 3, 4, 4, 13, 1, 4, 9]
S7 = [4, 2, 9, 13, 10, 12, 10, 7, 12, 14, 7, 3, 6, 4, 6, 9]
S8 = [10, 2, 5, 5, 3, 13, 15, 1, 6, 14, 11, 11, 13, 3, 1, 15]


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


# PRNG for Elisabeth-4
def Elisabeth_PRNG_next(xof_k, xof_r, xof_offset, perm, w_vec):
    new_k = xof_k
    new_r = xof_r
    new_offset = xof_offset
    for i in range(60):
        r, new_k, new_r, new_offset = XOF_int(new_k, new_r, new_offset, i, 256)
        ww, new_k, new_r, new_offset = XOF_bits(new_k, new_r, new_offset, 4)
        tmp = perm[i]
        perm[i] = perm[r]
        perm[r] = tmp
        w_vec[perm[i]] = (w_vec[perm[i]] + ww) & 15
    return new_k, new_r, new_offset


# function h
def h_func(x1, x2, x3, x4):
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

    test_IV = [0 for i in range(16)]

    XOF_K = encrypt_aes(C0, bytes(test_IV))
    XOF_R = encrypt_aes(C1, XOF_K)
    XOF_offset = 0

    es_k = copy.deepcopy(test_key)
    fault_es_k = copy.deepcopy(test_key)
    fault_pos = 0
    delta_val = 15

    fault_es_k[fault_pos] = (fault_es_k[fault_pos] + delta_val) & 15
    es_perm = [i for i in range(256)]
    es_w_vec = [0 for i in range(256)]

    # # A simple method to check the fault_pos and compute the average times
    # n = 100000
    # times_count = 0
    # t1 = time.time()
    # for tmp in range(n):
    #     test_IV = [random.randint(0, 15) for i in range(16)]
    #
    #     XOF_K = encrypt_aes(C0, bytes(test_IV))
    #     XOF_R = encrypt_aes(C1, XOF_K)
    #     XOF_offset = 0
    #
    #     es_k = copy.deepcopy(test_key)
    #     fault_es_k = copy.deepcopy(test_key)
    #     fault_pos = random.randint(0, 255)
    #     # For other bit fault, the process is the same. The only difference is the number of \delta h table
    #     fault_es_k[fault_pos] = (fault_es_k[fault_pos] + 8) & 15
    #     es_perm = [i for i in range(256)]
    #     es_w_vec = [0 for i in range(256)]
    #     candidate_pos = set([i for i in range(256)])
    #     count = 0
    #     while len(candidate_pos) > 1:
    #         XOF_K, XOF_R, XOF_offset = Elisabeth_PRNG_next(XOF_K, XOF_R, XOF_offset, es_perm, es_w_vec)
    #         es_z = 0
    #         fault_es_z = 0
    #         for j in range(12):
    #             es_z += (h_func(
    #                 (es_k[es_perm[5 * j]] + es_w_vec[es_perm[5 * j]]) & 15,
    #                 (es_k[es_perm[5 * j + 1]] + es_w_vec[es_perm[5 * j + 1]]) & 15,
    #                 (es_k[es_perm[5 * j + 2]] + es_w_vec[es_perm[5 * j + 2]]) & 15,
    #                 (es_k[es_perm[5 * j + 3]] + es_w_vec[es_perm[5 * j + 3]]) & 15,
    #             ) + (es_k[es_perm[5 * j + 4]] + es_w_vec[es_perm[5 * j + 4]]))
    #             fault_es_z += (h_func(
    #                 (fault_es_k[es_perm[5 * j]] + es_w_vec[es_perm[5 * j]]) & 15,
    #                 (fault_es_k[es_perm[5 * j + 1]] + es_w_vec[es_perm[5 * j + 1]]) & 15,
    #                 (fault_es_k[es_perm[5 * j + 2]] + es_w_vec[es_perm[5 * j + 2]]) & 15,
    #                 (fault_es_k[es_perm[5 * j + 3]] + es_w_vec[es_perm[5 * j + 3]]) & 15,
    #             ) + (fault_es_k[es_perm[5 * j + 4]] + es_w_vec[es_perm[5 * j + 4]]))
    #         es_z = es_z & 15
    #         fault_es_z = fault_es_z & 15
    #         count += 1
    #         # print(count, len(candidate_pos))
    #         if es_z != fault_es_z:
    #             candidate_pos = candidate_pos.intersection(set(es_perm[:60]))
    #     times_count += count
    # t2 = time.time()
    # print("Total time:", t2-t1)
    # # print("Averaged time:", (t1-t2)/n)
    # print("Averaged count:", times_count/n)
        # print(candidate_pos, fault_pos, count)

    # generate normal and faulted keystream
    normal_key_stream = []
    fault_key_stream = []
    dif_stream = []
    useful_pairs = []
    t1 = time.time()
    f = open("tmp_result_file/E4_useful_dif_information_3000_0.txt", "w")
    for i in range(3000):
        XOF_K, XOF_R, XOF_offset = Elisabeth_PRNG_next(XOF_K, XOF_R, XOF_offset, es_perm, es_w_vec)
        es_z = 0
        fault_es_z = 0
        for j in range(12):
            es_z += (h_func(
                (es_k[es_perm[5 * j]] + es_w_vec[es_perm[5 * j]]) & 15,
                (es_k[es_perm[5 * j + 1]] + es_w_vec[es_perm[5 * j + 1]]) & 15,
                (es_k[es_perm[5 * j + 2]] + es_w_vec[es_perm[5 * j + 2]]) & 15,
                (es_k[es_perm[5 * j + 3]] + es_w_vec[es_perm[5 * j + 3]]) & 15,
            ) + (es_k[es_perm[5 * j + 4]] + es_w_vec[es_perm[5 * j + 4]]))
            fault_es_z += (h_func(
                (fault_es_k[es_perm[5 * j]] + es_w_vec[es_perm[5 * j]]) & 15,
                (fault_es_k[es_perm[5 * j + 1]] + es_w_vec[es_perm[5 * j + 1]]) & 15,
                (fault_es_k[es_perm[5 * j + 2]] + es_w_vec[es_perm[5 * j + 2]]) & 15,
                (fault_es_k[es_perm[5 * j + 3]] + es_w_vec[es_perm[5 * j + 3]]) & 15,
            ) + (fault_es_k[es_perm[5 * j + 4]] + es_w_vec[es_perm[5 * j + 4]]))
        es_z = es_z & 15
        fault_es_z = fault_es_z & 15
        normal_key_stream.append(es_z)
        fault_key_stream.append(fault_key_stream)
        dif_stream.append((es_z - fault_es_z) % 16)
        if fault_pos in es_perm[0:60] and es_perm.index(fault_pos) % 5 != 4:
            begin_index = (es_perm.index(fault_pos) // 5) * 5
            useful_pairs.append((i, set(es_perm[begin_index: begin_index+4])))
            act_es_w_vec = [es_w_vec[es_perm[t]] for t in range(begin_index, begin_index+4)]
            f.write(str(i) + "\t" + str(es_perm[begin_index: begin_index+4]) + "\t" + str(act_es_w_vec) + "\t" + str((es_z - fault_es_z) & 15) + "\n")
    t2 = time.time()
    f.close()
    print(len(useful_pairs))
    print("Time for generating keystream: ", t2 - t1)

    tt1 = time.time()
    # Multiple initial point greedy algorithm
    closest_pairs = []
    cor_dis = 4
    for i in range(len(useful_pairs)):
        for j in range(i + 1, len(useful_pairs)):
            new_dis = 4 - len(useful_pairs[i][1].intersection(useful_pairs[j][1]))
            if new_dis < cor_dis:
                closest_pairs = [(i, j)]
                cor_dis = new_dis
            elif new_dis == cor_dis:
                closest_pairs.append((i, j))

    print(len(closest_pairs), cor_dis)
    # print(closest_pairs[:20])
    len_try = min((200, len(closest_pairs)))
    # cor_dis = 1
    print("1ST Time used:", time.time() - tt1)

    # target_pair: [estimated_size of max set, beginning pair, first time that zero-dis appears]
    # we will choose the pair with smallest target_pair[0] at first
    # for the case where two pairs have the same target_pair[0], we want a smaller target_pair[2]
    target_pair = [10, (0 , 0), 10000]
    for closest_pair in closest_pairs[:len_try]:
        maximum_size = 3
        tmp_useful_pairs = useful_pairs.copy()
        tt2 = time.time()
        print(closest_pair, len(tmp_useful_pairs))
        tmp_set = tmp_useful_pairs[closest_pair[0]][1].union(tmp_useful_pairs[closest_pair[1]][1])
        merge_path = [tmp_useful_pairs[closest_pair[0]][0], tmp_useful_pairs[closest_pair[1]][0]]
        add_length = [4, cor_dis]
        tmp1 = tmp_useful_pairs[closest_pair[0]]
        tmp2 = tmp_useful_pairs[closest_pair[1]]
        tmp_useful_pairs.remove(tmp1)
        tmp_useful_pairs.remove(tmp2)
        more_than_one_pos = []
        if cor_dis > 1:
            more_than_one_pos.append((0, tmp_useful_pairs[closest_pair[1]]))
        # print(tmp_set)
        count = 0
        first_zero_count = 10000
        while len(tmp_set) < 256 and len(tmp_useful_pairs) > 1:
            count += 1
            tmp_dis = 4
            tmp_index = 1
            for i in range(1, len(tmp_useful_pairs)):
                new_dis = 4 - len(tmp_set.intersection(tmp_useful_pairs[i][1]))
                if new_dis == 0:
                    tmp_dis = new_dis
                    tmp_index = i
                    if first_zero_count > count:
                        first_zero_count = count
                    break
                if new_dis < tmp_dis:
                    tmp_dis = new_dis
                    tmp_index = i
            if tmp_dis > 1:
                more_than_one_pos.append((count, tmp_useful_pairs[tmp_index]))
                maximum_size += (tmp_dis-1)
            tmp_set = tmp_set.union(tmp_useful_pairs[tmp_index][1])
            merge_path.append(tmp_useful_pairs[tmp_index][0])
            add_length.append(tmp_dis)
            tmp_useful_pairs.remove(tmp_useful_pairs[tmp_index])
        print(len(tmp_set), maximum_size)
        if (maximum_size < target_pair[0]) or (maximum_size == target_pair[0] and first_zero_count < target_pair[2]):
            target_pair = [maximum_size, closest_pair, first_zero_count]
        print("Time used:", time.time()-tt2)
        # print(len(more_than_one_pos), more_than_one_pos)
        if len(tmp_useful_pairs) > 1:
            for tmp in tmp_useful_pairs[1:]:
                merge_path.append(tmp[0])
                add_length.append(0)
            print("Left pairs: ", len(tmp_useful_pairs))
        f = open("E4_tmp_result/E4_merge_path_3000_0_"+str(closest_pair)+".txt", "w")
        for i in range(len(merge_path)):
            f.write(str(merge_path[i])+" "+str(add_length[i])+"\n")
        f.close()
    print(target_pair)