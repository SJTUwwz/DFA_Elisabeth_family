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


def h_func_b4(x1, x2, x3, x4, x5, x6):
    # h function for g_R
    x2 = (x2 + x1) & 15
    x4 = (x4 + x3) & 15
    x6 = (x6 + x5) & 15

    y1 = bS1[x1 & 15]
    y2 = bS2[x2 & 15]
    y3 = bS3[x3 & 15]
    y4 = bS4[x4 & 15]
    y5 = bS5[x5 & 15]
    y6 = bS6[x6 & 15]

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


# # compute the table (index, x1, x2, x3, x4, x5, x6, dh) directly
# index_dh_count = []
# for word_diff in range(1, 16):
#     for pos in range(6):
#         add_dif = [0 for i in range(6)]
#         add_dif[pos] = word_diff
#         f = open("Eb4_Diff_tables/New_Small_h_x%s_v%s.txt"%(pos, word_diff), "w")
#         print(add_dif)
#         dh_count = [0 for i in range(16)]
#         for t1 in range(16):
#             for t2 in range(16):
#                 for t3 in range(16):
#                     for t4 in range(16):
#                         for t5 in range(16):
#                             for t6 in range(16):
#                                 dh = (h_func_b4(t1, t2, t3, t4, t5, t6) - h_func_b4(t1+add_dif[0], t2+add_dif[1], t3+add_dif[2], t4+add_dif[3], t5+add_dif[4], t6+add_dif[5])) & 15
#                                 f.write("%s %s %s %s %s %s %s\n"%(t1, t2, t3, t4, t5, t6, dh))
#                                 dh_count[dh] += 1
#         index_dh_count.append(dh_count)
#         print(dh_count)
#         f.close()

import json

f = open("LUT_M_list.txt", "r")
table_g = json.loads(f.readlines()[0].rstrip("\n"))
f.close()
print(table_g[:10], len(table_g))


def bin_list_to_int(bin_l):
    result = 0
    for i in range(len(bin_l)):
        result += bin_l[i] * 2**i
    return int(result)


def int_to_bin(num, length):
    result_l = [0 for i in range(length)]
    tmp = num
    for i in range(length):
        result_l[length-1-i] = int(tmp//(2**(length-1-i)))
        tmp = tmp % (2**(length-1-i))
    return result_l


# for bit_pos in range(18):
#     xor_diff = int(2**bit_pos)
#     f = open("Margrethe_Diff_tables/diff_g_x%s.txt" % bit_pos, "w")
#     for all_x in range(int(2**18)):
#         dg = (table_g[all_x] - table_g[all_x ^ xor_diff]) & 15
#         bin_x = int_to_bin(all_x, 18)
#         write_text = ""
#         for item in bin_x:
#             write_text += (str(item) + " ")
#         write_text += (str(dg) + "\n")
#         f.write(write_text)
#     f.close()

for bit_pos in range(4):
    xor_diff = int(2**bit_pos)
    f = open("Margrethe_Diff_tables/diff_add_x%s.txt" % bit_pos, "w")
    for all_x in range(int(2**4)):
        dg = (all_x - (all_x ^ xor_diff)) & 15
        print(all_x, all_x ^ xor_diff, dg)
        bin_x = int_to_bin(all_x, 4)
        write_text = ""
        for item in bin_x:
            write_text += (str(item) + " ")
        write_text += (str(dg) + "\n")
        f.write(write_text)
    f.close()
