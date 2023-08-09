import os
import argparse
import shutil


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', nargs='+', dest='input', required=True,
                        help='input path list')
    parser.add_argument('-o', '--output', nargs='+', dest='output', required=True,
                        help='output path list')
    args = parser.parse_args()

    file_names = []

    for input_dir in args.input:
        if not os.path.exists(input_dir):
            raise Exception('The path ' + input_dir + ' doesn\'t exist!')
        file_names += [(name, input_dir) for name in os.listdir(input_dir)]

    file_names.sort(key=lambda x: int(x[0].split('.')[0].split('_')[1]))

    for i in range(len(file_names)):
        output_dir_index = i % len(args.output)
        output_dir = args.output[output_dir_index]
        file_name, input_dir = file_names[i]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        source = os.path.join(input_dir, file_name)
        target = os.path.join(output_dir, file_name)
        shutil.copyfile(source, target)


if __name__ == "__main__":
    main()
