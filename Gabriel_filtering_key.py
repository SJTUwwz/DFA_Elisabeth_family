import copy
import math
import time
import os


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


test_delta_val = 15
fault_p = 0
filter_table = [read_truth_table("E4_Diff_tables/New_Small_h_x0_v%s.txt"%test_delta_val)]
filter_table.append(read_truth_table("E4_Diff_tables/New_Small_h_x1_v%s.txt"%test_delta_val))
filter_table.append(read_truth_table("E4_Diff_tables/New_Small_h_x2_v%s.txt"%test_delta_val))
filter_table.append(read_truth_table("E4_Diff_tables/New_Small_h_x3_v%s.txt"%test_delta_val))
sim_times, sim_diff_vals, sim_poss, sim_w_vecs = read_simulate_result("tmp_result_file/Gabriel_useful_dif_information_0_80000_15.txt")
merge_path = read_path("useful_result/Gabriel_merge_path_0_80000_(39, 2265).txt")
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


def filter_solution(test_indexes, dif_value, fault_pos, w_vec):
    choice = test_indexes.index(fault_pos)
    cor_solution = []
    for tmp in filter_table[choice]:
        if tmp[-1] == dif_value:
            cor_solution.append([(tmp[i]-w_vec[i]) % 16 for i in range(4)])
    return cor_solution


def store_sol(file_name, tmp_pos, tmp_sol):
    f = open(file_name, "w")
    f.write(str(tmp_pos)+"\n")
    for sol in tmp_sol:
        f.write(str(sol)+"\n")
    f.close()


def read_sol(file_name, del_flag):
    f = open(file_name, "r")
    lines = f.readlines()
    tmp_pos = lines[0].rstrip("\n").strip("[").strip("]")
    tmp_pos = [int(x) for x in tmp_pos.split(",")]
    tmp_sol = []
    for i in range(1, len(lines)):
        t = lines[i].rstrip("\n").strip("[").strip("]")
        tmp_sol.append([int(x) for x in t.split(",")])
    if del_flag:
        os.remove(file_name)
    return tmp_pos, tmp_sol


if __name__ == "__main__":
    # # structure [pos, solution]

    Inter_times = 0
    # # create the beginning point
    # time0 = 63398
    # time1 = 78208
    # index0 = sim_times.index(time0)
    # index1 = sim_times.index(time1)
    # test_dif_val0 = sim_diff_vals[index0]
    # test_dif_val1 = sim_diff_vals[index1]
    # test_pos0 = sim_poss[index0]
    # test_pos1 = sim_poss[index1]
    # test_w_vec0 = sim_w_vecs[index0]
    # test_w_vec1 = sim_w_vecs[index1]
    # # print(index0, index1)
    # # print(test_dif_val0, test_dif_val1)
    # # print(test_pos0, test_pos1)
    # # print(test_w_vec0, test_w_vec1)
    # test_solution0 = filter_solution(test_pos0, test_dif_val0, fault_p, test_w_vec0)
    # test_solution1 = filter_solution(test_pos1, test_dif_val1, fault_p, test_w_vec1)
    # Inter_times += len(test_solution0)*len(test_solution1)
    # t1 = time.time()
    # new_index, new_solution = intersect(test_pos0, test_pos1, test_solution0, test_solution1)
    # print(new_index)
    # print(len(new_solution))
    # print("Time used: ", time.time()-t1)
    # store_sol("tmp/useful1.txt", new_index, new_solution)
    #
    # print(len(merge_path), merge_path[0])
    # # read beginning point
    # tmp_pos, tmp_solution_space = read_sol("tmp/useful1.txt", 0)

    # # If no pair for better beginning point, read from table directly
    begin_point = merge_path[0]
    tmp_index = sim_times.index(begin_point)
    tmp_dif_val = sim_diff_vals[tmp_index]
    tmp_pos = sim_poss[tmp_index]
    tmp_w_vec = sim_w_vecs[tmp_index]
    tmp_solution_space = filter_solution(tmp_pos, tmp_dif_val, fault_p, tmp_w_vec)

    # Intersect the solution space according to the merged path
    t0 = time.time()
    for i in range(1, len(merge_path)):
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
        if i < 400:
            print(i, next_merge_point, len(tmp_pos), len(tmp_solution_space), "Time used: ", time.time()-t1)
        if len(tmp_solution_space) > 2**22:
            print("Too huge space!")
            break
        if len(tmp_solution_space) < 1 or (len(tmp_solution_space) == 1 and len(tmp_solution_space[0]) == 512):
            break
    print("Total time used: ", time.time()-t0)
    print("Test delta_val:", test_delta_val)
    print(len(tmp_pos), len(tmp_solution_space))
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