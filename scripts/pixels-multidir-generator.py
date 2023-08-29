import os
import argparse
import shutil


# The script copies all files in ${input}/${table}/${suffix}/ directory to ${output}/${table}/${suffix}/
# input, output and suffix should be designated, while table is detected automatically.
# For example, we execute the following script:
# cd pixels-duckdb
# python scripts/pixels-multidir-generator.py -i /data/tpch-300 -o /data1/tpch-300-partition1 /data2/tpch-300-partition2
# The input path layout is:
# input:
#
# /data/tpch-300
# ----lineitem
# --------v-o-ordered
# ------------ a_1.pxl
# ------------ a_2.pxl
# ----customer
# --------v-o-ordered
# ------------ a_1.pxl
# ------------ a_2.pxl
# We will create the same path layout in the output path:
# output:
#
# /data1/tpch-300-partition1
# ----lineitem
# --------v-o-ordered
# ------------ a_1.pxl
# ----customer
# --------v-o-ordered
# ------------ a_1.pxl
#
# /data2/tpch-300-partition2
# ----lineitem
# --------v-o-ordered
# ------------ a_2.pxl
# ----customer
# --------v-o-ordered
# ------------ a_2.pxl

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', nargs='+', dest='input', required=True,
                        help='input path list')
    parser.add_argument('-o', '--output', nargs='+', dest='output', required=True,
                        help='output path list')
    parser.add_argument('-s', '--suffix', dest='suffix', default="v-0-ordered",
                        help='The suffix path of the input and output path')
    parser.add_argument('-v', dest='verbose', action='store_true', help='output the command')
    args = parser.parse_args()

    tables = set()
    for input_dir in args.input:
        tables.update(set(os.listdir(input_dir)))

    verbose = {}

    # input_dir must be existed, but input_dir_suffix doesn't have to be existed (this might happen when input is
    # also multiple dirs)
    for table in tables:
        file_names = []
        for input_dir in args.input:
            input_dir_suffix = os.path.join(input_dir, table, args.suffix)
            if not os.path.exists(input_dir):
                raise Exception('The path ' + input_dir_suffix + ' doesn\'t exist!')
            if os.path.exists(input_dir_suffix):
                file_names += [(name, input_dir_suffix) for name in os.listdir(input_dir_suffix)]

        file_names.sort(key=lambda x: int(x[0].split('.')[0].split('_')[1]))

        for output_dir in args.output:
            output_dir_suffix = os.path.join(output_dir, table, args.suffix)
            if not os.path.exists(output_dir_suffix):
                os.makedirs(output_dir_suffix)
            if table not in verbose:
                verbose[table] = []
            verbose[table].append('"' + output_dir_suffix + "/*.pxl\"")

        for i in range(len(file_names)):
            output_dir_index = i % len(args.output)
            output_dir = args.output[output_dir_index]
            file_name, input_dir_suffix = file_names[i]

            output_dir_suffix = os.path.join(output_dir, table, args.suffix)
            if not os.path.exists(output_dir_suffix):
                os.makedirs(output_dir_suffix)

            source = os.path.join(input_dir_suffix, file_name)
            target = os.path.join(output_dir_suffix, file_name)
            if not os.path.exists(target):
                shutil.copyfile(source, target)

    if args.verbose:
        print('-' * 10 + "Copy the below commands to the benchmark template " + '-' * 10)
        for table, paths in verbose.items():
            path_str = '[' + ','.join(paths) + ']'
            cmd_prefix = "CREATE VIEW " + table + " AS SELECT * FROM pixels_scan("
            cmd_suffix = ");"
            print(cmd_prefix + path_str + cmd_suffix)
if __name__ == "__main__":
    main()
