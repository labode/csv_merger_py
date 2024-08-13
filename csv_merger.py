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


def read_csv(file_name):
    data = []

    with open(file_name) as csv_file:
        # TODO: Possible extension => Let user supply delimiter (and header yes/no)
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            # Exclude header line
            if row[0] == 'Id' and row[1] == 'Inner' and row[2] == 'Media' and row[3] == 'Outer':
                continue
            else:
                identifier = int(row[0])
                # Convert decimal values from german to english format
                value_1 = row[1].replace(',', '.')
                value_1 = float(value_1)
                value_2 = row[2].replace(',', '.')
                # If we have no value for row2, there is no externa, so media diameter = outer diameter
                if value_2 == '':
                    value_2 = row[3].replace(',', '.')
                value_2 = float(value_2)
                value_3 = row[3].replace(',', '.')
                value_3 = float(value_3)

                data.append([identifier, value_1, value_2, value_3])

    return data


def write_csv(data, target_file):
    with open(target_file, 'w', newline='') as csv_file:
        data_writer = csv.writer(csv_file, delimiter=',')
        data_writer.writerow(['Id', 'Inner', 'Media', 'Outer'])
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
                comb = [data[i][0], data[i][1], data[i][2], data[i][3]]
                while data[i][0] == data[i+1][0]:
                    comb[1] += data[i + 1][1]
                    comb[2] += data[i + 1][2]
                    comb[3] += data[i + 1][3]
                    j += 1
                    i += 1
                    if i == size - 1:
                        break
                comb[1] = round(comb[1] / j, 3)
                comb[2] = round(comb[2] / j, 3)
                comb[3] = round(comb[3] / j, 3)
                return_data.append(comb)
                i += 1
            else:
                return_data.append(data[i])
                i += 1

    return return_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge all csv files from a directory')
    parser.add_argument('directory', action='store', type=str, help='Directory containing .csv files')
    parser.add_argument('-f', '--filename', action='store', type=str, required=False, default='merged',
                        help='Name of output file')
    parser.add_argument('-a', '--average', action='store_true', required=False, help='Calculate average of values')

    args = parser.parse_args()

    directory = args.directory
    filename = args.filename
    average = args.average

    file_list = list_dir(directory, '.csv')

    header = get_header(file_list[0])

    dataset = []

    for file_entry in file_list:
        file_data = read_csv(file_entry)
        for entry_row in file_data:
            dataset.append(entry_row)

    print(str(len(dataset)) + ' datasets read')

    if average:
        dataset = average_measurements(dataset)
        print(str(len(dataset)) + ' averaged datasets created')

    write_csv(dataset, filename + '.csv')
