import csv, os, datetime, ntpath

report_file_name = "C:\\ItauPython\\teste.csv"
report_delimiter = ';'
output_path = '.'
splited_files = []

def main():
    file_size = getsize(report_file_name)

    if file_size > 50:
        splitfile(report_file_name)
        for file in splited_files:
            formatfile(file)
    else:
        formatfile(report_file_name)

def getsize(filename):
    file_size = os.path.getsize(filename)
    return (file_size / (1024 ** 3))
    #return (file_size)

def splitfile(filename):
    with open(os.path.abspath(filename), "r", newline='', encoding="utf8") as originalFile:
        reader = csv.reader(originalFile, delimiter=report_delimiter)
        current_piece = 1
        output_file = os.path.join(output_path, str(current_piece) + ntpath.basename(filename))
        splited_files.append(str(current_piece) + ntpath.basename(filename))
        with open(os.path.abspath(output_file), "w", newline='', encoding="utf8") as output_file_open:
            current_out_writer = csv.writer(output_file_open, delimiter=report_delimiter)
            header = next(reader)
            current_out_writer.writerow(header)
        output_file_open.close()
        for row in enumerate(reader):
            if os.path.getsize(output_file) > 1073741824:
                current_piece += 1
                output_file = os.path.join(output_path, str(current_piece) + ntpath.basename(filename))
                splited_files.append(str(current_piece) + ntpath.basename(filename))
                with open(os.path.abspath(output_file), "a", newline='', encoding="utf8") as output_file_open:
                    current_out_writer = csv.writer(output_file_open, delimiter=report_delimiter)
                    current_out_writer.writerow(header)
                    current_out_writer.writerow(row[1])
                output_file_open.close()
            else:
                with open(os.path.abspath(output_file), "a", newline='', encoding="utf8") as output_file_open:
                    current_out_writer = csv.writer(output_file_open, delimiter=report_delimiter)
                    current_out_writer.writerow(row[1])
                output_file_open.close()
    os.remove(filename)

def formatfile(filename):
    current_piece = 'ft'
    cabecalho = '0' + str(datetime.datetime.now())
    with open(os.path.abspath(filename), "r", newline='', encoding="utf8") as originalFile:
        reader = csv.reader(originalFile, delimiter=report_delimiter)
        reader_to_list = list(reader)
        reader_to_list.remove(reader_to_list[0])
        total_registros = len(reader_to_list)
        for i, row in enumerate(reader_to_list):
            reader_to_list[i].insert(0, '1')
        reader_to_list.insert(0, ['0', cabecalho])
        reader_to_list.append(['9', str(total_registros)])
        output_file = os.path.join(output_path, str(current_piece) + ntpath.basename(filename))
        with open(os.path.abspath(output_file), "w", newline='', encoding="utf8") as output_file_open:
            current_out_writer = csv.writer(output_file_open, delimiter=report_delimiter)
            for row in reader_to_list:
                current_out_writer.writerow(row)
        output_file_open.close()
    originalFile.close()
    os.remove(filename)

if __name__ == '__main__':
    main()
