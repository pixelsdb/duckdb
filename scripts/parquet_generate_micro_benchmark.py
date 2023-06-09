from os import path, mkdir
sf = 300
root_path = "benchmark/tpch/parquet/micro-benchmark"
sf_path = path.join(root_path, "tpch_" + str(sf))
if not path.exists(sf_path):
    mkdir(sf_path)
for i in range(1, 8):
    if i < 10:
        f = open(path.join(sf_path, "parquet_q0" + str(i) + "_tpch_" + str(sf) + ".benchmark"), "w")
    else:
        f = open(path.join(sf_path, "parquet_q" + str(i) + "_tpch_" + str(sf) + ".benchmark"), "w")

    f.writelines("template benchmark/tpch/parquet/parquet_micro_benchmark.benchmark.in\n")
    f.writelines("SF_NUMBER=" + str(sf) + "\n")
    f.writelines("SF_NUMBER_UNDERSCORE=" + str(sf) + "\n")
    if i < 10:
        f.writelines("QUERY_NUMBER_PADDED=0" + str(i) + "\n")
    else:
        f.writelines("QUERY_NUMBER_PADDED=" + str(i) + "\n")
