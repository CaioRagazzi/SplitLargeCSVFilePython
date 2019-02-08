import csv, os, datetime

reportFilename = "teste.csv"
reportDelimiter = ';'
outputPath = '.'
splitedFiles = []

def main():
    tamanhoArquivo = getSize(reportFilename)

    if tamanhoArquivo > 10:
        splitFile(reportFilename)
        for file in splitedFiles:
            formatFile(file)
    else:
        formatFile(reportFilename)

def getSize(filename):
    tamanhoarquivo = os.path.getsize(filename)
    return (tamanhoarquivo / (1024 ** 3))
    #return (tamanhoarquivo)

def splitFile(filename):
    with open(filename, "r", newline='', encoding="utf8") as originalFile:
        reader = csv.reader(originalFile, delimiter=reportDelimiter)
        current_piece = 1
        outputFile = os.path.join(outputPath, str(current_piece) + filename)
        splitedFiles.append(str(current_piece) + filename)
        with open(outputFile, "w", newline='', encoding="utf8") as outputFileOpen:
            current_out_writer = csv.writer(outputFileOpen, delimiter=reportDelimiter)
            header = next(reader)
            current_out_writer.writerow(header)
        outputFileOpen.close()
        for row in enumerate(reader):
            if os.path.getsize(outputFile) > 104857600:
                current_piece += 1
                outputFile = os.path.join(outputPath, str(current_piece) + filename)
                splitedFiles.append(str(current_piece) + filename)
                with open(outputFile, "a", newline='', encoding="utf8") as outputFileOpen:
                    current_out_writer = csv.writer(outputFileOpen, delimiter=reportDelimiter)
                    current_out_writer.writerow(header)
                    current_out_writer.writerow(row[1])
                outputFileOpen.close()
            else:
                with open(outputFile, "a", newline='', encoding="utf8") as outputFileOpen:
                    current_out_writer = csv.writer(outputFileOpen, delimiter=reportDelimiter)
                    current_out_writer.writerow(row[1])
                outputFileOpen.close()
    os.remove(filename)

def formatFile(filename):
    current_piece = 'ft'
    cabecalho = '0' + str(datetime.datetime.now())
    with open(filename, "r", newline='', encoding="utf8") as originalFile:
        reader = csv.reader(originalFile, delimiter=reportDelimiter)
        reader_to_list = list(reader)
        reader_to_list.remove(reader_to_list[0])
        total_registros = len(reader_to_list)
        for i, row in enumerate(reader_to_list):
            reader_to_list[i].insert(0, '1')
        reader_to_list.insert(0, ['0', cabecalho])
        reader_to_list.append(['9', str(total_registros)])
        outputFile = os.path.join(outputPath, str(current_piece) + filename)
        with open(outputFile, "w", newline='', encoding="utf8") as outputFileOpen:
            current_out_writer = csv.writer(outputFileOpen, delimiter=reportDelimiter)
            for row in reader_to_list:
                current_out_writer.writerow(row)
    outputFileOpen.close()
    originalFile.close()
    os.remove(filename)

if __name__ == '__main__':
    main()
