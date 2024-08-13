import argparse
import os
import csv


def list_dir(path, filetype=''):
    files = os.listdir(path)

    if filetype != '':
        data = []
        for file in files:
            if file.endswith(filetype):
                data.append(path + '/' + file)
        return data
    else:
        data = []
        for file in files:
            data.append(path + '/' + file)
        return data


def get_header(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        first_line = next(reader)

    return first_line


def read_csv(file_name, skip_header=True):
    data = []

    with open(file_name) as csv_file:
        # TODO: Possible extension => Let user supply delimiter
        reader = csv.reader(csv_file, delimiter=';')

        if skip_header:
            next(reader, None)
        for row in reader:
            i = 0
            line = []
            for entry in row:
                # The first value is the (numerical!) identifier (id)
                if i == 0:
                    line.append(int(entry))
                # All following values are measurements
                else:
                    if entry == '':
                        value = 0
                    else:
                        value = entry.replace(',', '.')
                        value = float(value)
                    line.append(value)

                i += 1

            data.append(line)

    return data


def write_csv(data, target_file, first_row):
    with open(target_file, 'w', newline='') as csv_file:
        data_writer = csv.writer(csv_file, delimiter=',')
        if first_row:
            data_writer.writerow(first_row)
        for row in data:
            data_writer.writerow(row)


def average_measurements(data):
    # Sort array
    data = sorted(data)
    # Count entries
    size = len(data)

    return_data = []

    i = 0
    # For every entry => While the next entry has the same id => combine
    while i < size:
        # if this is the last entry in our array, we do not have to check, if the next one has the same id, duh
        if i == size - 1:
            return_data.append(data[i])
            i += 1
        else:
            if data[i][0] == data[i+1][0]:
                j = 1
                comb = data[i]
                while data[i][0] == data[i+1][0]:
                    k = 1
                    while k < len(data[i]):
                        comb[k] += data[i + 1][k]
                        k += 1
                    j += 1
                    i += 1
                    if i == size - 1:
                        break

                k = 1
                while k < len(comb):
                    comb[k] = round(comb[k] / j, 3)
                    k += 1

                return_data.append(comb)
                i += 1
            else:
                return_data.append(data[i])
                i += 1

    return return_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge all csv files from a directory into a single file. '
                                                 'This program expects the .csv files to contain a header line and '
                                                 'each following line to start with a numerical (int) identifier and '
                                                 'an arbitrary number of numerical values (int or float, will be '
                                                 'converted to float). Empty fields will be converted to 0. '
                                                 'Right now the german format is expected, i.e. '
                                                 'values delimited by a ; and , as a decimal separator. The output '
                                                 'will be a single file in standard .csv format with , as delimiter '
                                                 'and . as decimal separator.')
    parser.add_argument('directory', action='store', type=str, help='Directory containing .csv files')
    parser.add_argument('-f', '--filename', action='store', type=str, required=False, default='merged',
                        help='Name of output file')
    parser.add_argument('-a', '--average', action='store_true', required=False, help='Calculate average '
                                                                                     'values per identifier')
    parser.add_argument('--no_header', action='store_true', default=False, required=False, help='Set this '
                                                                                                'option if your files '
                                                                                                'do not contain a '
                                                                                                'header line')
    # TODO: Allow standard .csv format (delimiter = , and decimal separator = .)

    args = parser.parse_args()

    directory = args.directory
    filename = args.filename
    average = args.average
    no_header = args.no_header

    file_list = list_dir(directory, '.csv')

    if no_header:
        # Placeholder, so the variable exists
        header = None
    else:
        header = get_header(file_list[0])

    dataset = []

    for file_entry in file_list:
        if no_header:
            file_data = read_csv(file_entry, False)
        else:
            file_data = read_csv(file_entry)
        for entry_row in file_data:
            dataset.append(entry_row)

    print(str(len(dataset)) + ' datasets read')

    if average:
        dataset = average_measurements(dataset)
        print(str(len(dataset)) + ' averaged datasets created')

    write_csv(dataset, filename + '.csv', header)
