import csv, os, datetime, ntpath, sys

report_file_name = "C:\\ItauPython\\teste.csv"
report_delimiter = ';'
output_path = '.'
splited_files = []
splited_files_size = 1073741824

def main():
    file_size = getsize(report_file_name)

    if file_size > 50:
        splitfile(report_file_name)
        for file in splited_files:
            formatfile(file, str(sys.argv[1]))
    else:
        formatfile(report_file_name, str(sys.argv[1]))

def getsize(filename):
    file_size = os.path.getsize(filename)
    return (file_size / (1024 ** 3))

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
            if os.path.getsize(output_file) > splited_files_size:
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

def formatfile(filename, tablename):
    current_piece = 'ft'
    cabecalho = tablename + '_' + str(datetime.datetime.now())
    with open(os.path.abspath(filename), "r", newline='', encoding="utf8") as originalFile:
        reader = csv.reader(originalFile, delimiter=report_delimiter)
        next(reader, None)
        tamanho = sum(1 for row in reader)
        originalFile.seek(0)
        next(reader, None)
        output_file = os.path.join(output_path, str(current_piece) + ntpath.basename(filename))
        with open(os.path.abspath(output_file), "w", newline='', encoding="utf8") as output_file_open:
            current_out_writer = csv.writer(output_file_open, delimiter=report_delimiter)
            current_out_writer.writerow(['0', cabecalho])
            for row in reader:
                current_out_writer.writerow(['1'] + row)
            current_out_writer.writerow(['9', str(tamanho)])
        output_file_open.close()
    originalFile.close()
    os.remove(filename)

if __name__ == '__main__':
    main()
