import copy
import math
import time
import os


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


def read_truth_table(file_name):
    # [x1, x2, x3, x4, dh]
    f = open(file_name, "r")
    lines = f.readlines()
    truth_table = []
    for line in lines:
        line = line.rstrip("\n")
        new_list = line.split(" ")
        row = [int(i) for i in new_list]
        truth_table.append(row)
    # print(len(truth_table))
    # print(truth_table[0])

    return truth_table


def read_simulate_result(file_name):
    f = open(file_name, "r")
    lines = f.readlines()
    time_infs = []
    diff_val_infs = []
    pos_infs = []
    white_vec_infs = []
    for line in lines:
        line = line.rstrip("\n")
        tmp_pair = line.split("\t")
        time_infs.append(int(tmp_pair[0]))
        diff_val_infs.append(int(tmp_pair[3]))
        tmp_pos_inf = tmp_pair[1].strip('[')
        tmp_pos_inf = tmp_pos_inf.strip(']')
        tmp_pos_inf = [int(x) for x in tmp_pos_inf.split(',')]
        pos_infs.append(tmp_pos_inf)
        tmp_w_vec = tmp_pair[2].strip('[')
        tmp_w_vec = tmp_w_vec.strip(']')
        tmp_w_vec = [int(x) for x in tmp_w_vec.split(',')]
        white_vec_infs.append(tmp_w_vec)
    return time_infs, diff_val_infs, pos_infs, white_vec_infs


def determine_inter(index_pair, sol1, sol2):
    # print(index_pair, sol1, sol2)
    for pair in index_pair:
        if sol1[pair[0]] == sol2[pair[1]]:
            continue
        else:
            return 0
    return 1


def intersect(index1, index2, solution1, solution2):
    add_index = []
    cor_index = []
    cor_index_pair = []
    for i in range(len(index2)):
        if index2[i] in index1:
            cor_index_pair.append((index1.index(index2[i]), i))
        else:
            add_index.append(index2[i])
            cor_index.append(i)
    new_index = index1 + add_index
    new_solution = []
    if len(add_index) == 0:
        for tmp1 in solution1:
            for tmp2 in solution2:
                # print(tmp1, tmp2, determine_inter(cor_index_pair, tmp1, tmp2))
                if determine_inter(cor_index_pair, tmp1, tmp2):
                    new_solution.append(tmp1)
    else:
        for tmp1 in solution1:
            for tmp2 in solution2:
                if determine_inter(cor_index_pair, tmp1, tmp2):
                    new_sol = copy.deepcopy(tmp1)
                    for i in cor_index:
                        new_sol.append(tmp2[i])
                    new_solution.append(new_sol)

    return new_index, new_solution


def read_path(file_name):
    f = open(file_name, "r")
    result_path = []
    for line in f.readlines():
        result_path.append(int(line.rstrip("\n").split(" ")[0]))
    return result_path


ttime1 = time.time()
fault_p = 106
filter_table = [read_truth_table("Margrethe_Diff_tables/diff_g_x0.txt")]
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x1.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x2.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x3.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x4.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x5.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x6.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x7.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x8.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x9.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x10.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x11.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x12.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x13.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x14.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x15.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x16.txt"))
filter_table.append(read_truth_table("Margrethe_Diff_tables/diff_g_x17.txt"))
sim_times, sim_diff_vals, sim_poss, sim_w_vecs = read_simulate_result("Mar_tmp_result/Margrethe_useful_dif_information_200000_0_699.txt")
print("Time for readding tables: ", time.time()-ttime1)
merge_path = read_path("Mar_tmp_result/Margrethe_merge_path_200000_0_699_8676.txt")
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


def filter_solution(test_indexes, dif_value, fault_pos, w_vec):
    choice = test_indexes.index(fault_pos)
    cor_solution = []
    for tmp in filter_table[choice]:
        if tmp[-1] == dif_value:
            cor_solution.append([tmp[i] ^ w_vec[i] for i in range(18)])
    return cor_solution


if __name__ == "__main__":
    # # structure [pos, solution]

    Inter_times = 0
    # # If no pair for better beginning point, read from table directly
    # begin_point = merge_path[0]
    # tmp_index = sim_times.index(begin_point)
    # tmp_dif_val = sim_diff_vals[tmp_index]
    # tmp_pos = sim_poss[tmp_index]
    # tmp_w_vec = sim_w_vecs[tmp_index]
    # tmp_solution_space = filter_solution(tmp_pos, tmp_dif_val, fault_p, tmp_w_vec)
    # print(len(tmp_solution_space))
    tmp_pos = [0, 2, 3, 4, 6, 16, 18, 19, 25, 27, 28, 29, 30, 31, 33, 38, 41, 44, 46, 54, 56, 64, 67, 68, 72, 73, 74, 77, 79, 80, 82, 83, 84, 86, 92, 93, 95, 96, 98, 102, 113, 118, 125, 127, 128, 130, 134, 135, 141, 143, 145, 147, 151, 156, 161, 164, 165, 166, 167, 168, 170, 171, 173, 178, 183, 185, 186, 187, 191, 194, 200, 202, 203, 205, 206, 207, 214, 222, 223, 235, 236, 237, 239, 240, 243, 245, 253, 254, 255, 260, 265, 266, 267, 271, 273, 276, 283, 285, 286, 288, 291, 299, 300, 303, 304, 306, 309, 310, 314, 316, 318, 319, 322, 324, 327, 329, 331, 335, 339, 341, 346, 349, 358, 365, 367, 369, 372, 373, 376, 378, 382, 385, 386, 387, 389, 390, 391, 393, 398, 405, 406, 408, 413, 416, 418, 421, 422, 424, 425, 431, 437, 440, 442, 444, 447, 448, 450, 451, 452, 454, 456, 460, 478, 482, 488, 489, 490, 491, 495, 497, 499, 513, 521, 525, 526, 530, 531, 532, 533, 534, 536, 552, 555, 562, 563, 564, 570, 573, 575, 577, 587, 589, 592, 593, 594, 596, 600, 602, 612, 615, 616, 617, 618, 619, 620, 621, 630, 635, 637, 639, 644, 647, 649, 651, 655, 659, 660, 664, 666, 667, 672, 676, 677, 681, 682, 684, 686, 687, 690, 691, 692, 696, 701, 703, 710, 717, 721, 722, 724, 731, 733, 734, 735, 739, 740, 751, 752, 754, 758, 760, 761, 762, 769, 774, 775, 776, 782, 785, 786, 788, 791, 794, 795, 801, 806, 808, 812, 815, 816, 822, 823, 825, 829, 831, 835, 839, 842, 848, 849, 850, 855, 856, 858, 861, 866, 871, 872, 873, 883, 889, 891, 893, 905, 906, 911, 912, 914, 917, 918, 922, 924, 927, 937, 938, 939, 943, 954, 956, 963, 964, 965, 966, 970, 974, 975, 976, 979, 981, 985, 986, 987, 995, 996, 997, 999, 1000, 1002, 1007, 1008, 1010, 1012, 1014, 1018, 1019, 1020, 1021, 1028, 1031, 1033, 1034, 1038, 1040, 1041, 1047, 1057, 1060, 1062, 1066, 1067, 1068, 1071, 1074, 1075, 1076, 1080, 1082, 1084, 1085, 1090, 1094, 1096, 1101, 1106, 1107, 1111, 1112, 1114, 1119, 1120, 1121, 1123, 1128, 1131, 1139, 1143, 1146, 1148, 1149, 1154, 1156, 1162, 1163, 1165, 1166, 1167, 1175, 1178, 1179, 1187, 1193, 1194, 1197, 1198, 1200, 1202, 1203, 1207, 1208, 1217, 1221, 1222, 1225, 1229, 1232, 1233, 1234, 1235, 1236, 1240, 1241, 1244, 1245, 1248, 1249, 1251, 1252, 1253, 1254, 1266, 1270, 1271, 1276, 1280, 1283, 1285, 1290, 1296, 1297, 1298, 1300, 1305, 1307, 1308, 1311, 1312, 1313, 1319, 1320, 1324, 1329, 1332, 1338, 1342, 1343, 1344, 1345, 1346, 1352, 1356, 1361, 1363, 1368, 1372, 1377, 1379, 1383, 1384, 1386, 1389, 1390, 1391, 1392, 1393, 1394, 1395, 1398, 1399, 1400, 1407, 1410, 1414, 1428, 1430, 1431, 1432, 1434, 1436, 1437, 1441, 1444, 1447, 1452, 1454, 1458, 1459, 1463, 1465, 1469, 1470, 1471, 1473, 1478, 1484, 1485, 1489, 1492, 1494, 1495, 1496, 1498, 1501, 1503, 1504, 1507, 1508, 1513, 1517, 1518, 1519, 1525, 1528, 1532, 1534, 1541, 1545, 1547, 1549, 1551, 1552, 1559, 1560, 1568, 1571, 1577, 1580, 1581, 1585, 1592, 1597, 1600, 1603, 1605, 1607, 1608, 1609, 1613, 1615, 1620, 1621, 1622, 1624, 1627, 1634, 1637, 1638, 1639, 1640, 1644, 1645, 1648, 1651, 1652, 1655, 1656, 1659, 1662, 1667, 1668, 1669, 1670, 1673, 1677, 1679, 1682, 1687, 1688, 1689, 1690, 1695, 1697, 1698, 1699, 1700, 1701, 1703, 1707, 1709, 1710, 1711, 1715, 1716, 1719, 1720, 1725, 1730, 1731, 1733, 1737, 1739, 1741, 1742, 1744, 1751, 1757, 1766, 1772, 1773, 1775, 1776, 1779, 1781, 1782, 1783, 1785, 1792, 1794, 1795, 1796, 1797, 1799, 1801, 1802, 1806, 1811, 1814, 1815, 1818, 1823, 1824, 1825, 1826, 1832, 1833, 1835, 1836, 1838, 1839, 1840, 1841, 1844, 1847, 1851, 1852, 1857, 1859, 1863, 1865, 1869, 1875, 1877, 1878, 1880, 1881, 1886, 1887, 1888, 1890, 1891, 1893, 1897, 1899, 1907, 1909, 1910, 1919, 1920, 1921, 1922, 1924, 1929, 1931, 1933, 1937, 1944, 1946, 1948, 1955, 1959, 1960, 1964, 1967, 1968, 1974, 1977, 1978, 1979, 1981, 1982, 1984, 1986, 1994, 1996, 1999, 2005, 2006, 2009, 2012, 2013, 2014, 2015, 2018, 2019, 2022, 2028, 2030, 2032, 2035, 2041, 2042]
    tmp_solution_space = [[0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1]]

    # Intersect the solution space according to the merged path
    t0 = time.time()
    for i in range(0, len(merge_path)):
        t1 = time.time()
        next_merge_point = merge_path[i]
        next_index = sim_times.index(next_merge_point)
        next_dif_val = sim_diff_vals[next_index]
        next_pos = sim_poss[next_index]
        next_w_vec = sim_w_vecs[next_index]
        next_solution_space = filter_solution(next_pos, next_dif_val, fault_p, next_w_vec)
        Inter_times += len(tmp_solution_space) * len(next_solution_space)
        tmp_pos, tmp_solution_space = intersect(tmp_pos, next_pos, tmp_solution_space, next_solution_space)
        # new_f = "tmp/checkpoint_%s.txt"%i
        # store_sol(new_f, tmp_index, tmp_solution_space)
        if len(tmp_solution_space) > 2**22:
            print("Too huge space!")
            break
        if i < 1000:
            print(i, next_merge_point, len(tmp_pos), len(tmp_solution_space), "Time used: ", time.time()-t1)
        if len(tmp_solution_space) < 1 or (len(tmp_solution_space) == 1 and len(tmp_solution_space[0]) == 2048):
            break
    print("Total time used: ", time.time()-t0)
    # print(tmp_pos, len(tmp_pos), len(tmp_solution_space))
    print("Total number of intersection:", math.log(Inter_times, 2), Inter_times)
    # print(tmp_solution_space[0])

    # Check each solution (In actual scenario, use keystream produced by solution to check)
    print(len(tmp_solution_space))
    for tmp_value in tmp_solution_space:
        flag = 1
        for i in range(len(tmp_pos)):
            if tmp_value[i] == test_key[tmp_pos[i]]:
                continue
            else:
                # print(i, tmp_value[i], test_key[tmp_pos[i]])
                flag = 0
                break
        # print(tmp_value)
        # print("Whether the guessed key is right? ", flag)
        if flag:
            print("The right key was found!")
            # print(tmp_value)