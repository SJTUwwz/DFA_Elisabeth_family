import time
# Read the filter table
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


if __name__ == "__main__":
    f = open("distribution/Eb4_dh_distribution.txt", "w")
    t1 = time.time()
    total_count = [0 for i in range(16)]
    for pos in range(5):
        for del_value in range(1, 16):
            # read the table and compute the size of candidate value set for each possible case (different \Delta h)
            f_table = read_truth_table("Eb4_Diff_tables/New_Small_h_x"+str(pos)+"_v"+str(del_value)+".txt")
            tmp_count = [0 for i in range(16)]
            for term in f_table:
                tmp_count[term[6]] += 1
                total_count[term[6]] += 1
            # print("Pos:", pos, "Delta val:", del_value, "Distribution:", tmp_count)
            f.write("x"+str(pos)+"\t"+str(del_value)+"\t"+str(tmp_count)+"\n")
            print(pos, del_value, time.time()-t1)
    print(total_count)
    f.write("Total distribution: "+str(total_count)+"\n")
    f.close()