import re


def fixed_incorrect_html_field(input_file: str, output_file: str):
    '''
    "2391.19","Success","authorize"
    "1734.02","500 proxy
    Content-Type: text/html
    Connection: close

    <!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1","authorize"
    :return:
    "2391.19","Success","authorize"
    "1734.02","500 proxy Content-Type: text/html  Connection: close <!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1","authorize"

    '''

    pattern_start_line = r'^"\d+\.\d{2}","'
    pattern_end_line = r'"$'
    pattern_backslash_dblquater = r'\\"'

    fw = open(output_file, 'w')
    error_line = ''

    with open(input_file) as fr:
        line = fr.readline()
        line_number = 1
        while line:
            line = line.rstrip()
            line = re.sub(pattern_backslash_dblquater, '', line)
            is_start_line_correct = re.search(pattern_start_line, line)
            is_end_line_correct = re.search(pattern_end_line, line)

            if is_start_line_correct and is_end_line_correct:
                # print('correct line' +  str(line_number) )
                if error_line:
                    fw.write(error_line + '\n')
                    #print('error line' + str(error_line) + 'end error\n')
                    error_line = ''
                fw.write(line + '\n')
            else:
                if line == '--':
                    print('line -- line num : ' + str(line_number))
                    line = ''

                if line:
                    error_line = error_line + line

                if is_end_line_correct:
                    fw.write(error_line + '\n')
                    #print('error line' + str(error_line) + 'end error\n')
                    error_line = ''

               # print('line_num = ' + str(line_number))

            line_number += 1
            line = fr.readline()

    fw.close()


def fixed_incorrect_html_field_v2(input_file: str, output_file: str):
    '''
    "2391.19","Success","authorize"
    "1734.02","500 proxy
    Content-Type: text/html
    Connection: close

    <!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1","authorize"
    :return:
    "2391.19","Success","authorize"
    "1734.02","500 proxy Content-Type: text/html  Connection: close <!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1","authorize"

    '''
    pattern_backslash_dblquater = r'\\"'
    with open(input_file, "r") as fr:
        fw = open(output_file, 'w')
        for line in fr:

            line = line.rstrip()
            line = re.sub(pattern_backslash_dblquater, '', line)

            if line == '--':
                continue

            if line.endswith('"authorize"'):
                line += '\n'

            fw.write(line )
        fw.close()

