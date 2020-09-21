import os
import re

def get_count_line(in_file):
    tmp_file = 'tmp-comand_info.txt'
    comand_line = 'wc -l ' + in_file + ' > ' + tmp_file
    os.system(comand_line)
    pattern = '[0-9]+'

    infile = open(tmp_file, 'r')
    firstLine = infile.readline()
    infile.close()
    os.remove(tmp_file)

    result = re.search(pattern, firstLine)
    count_line = result.group(0)
    return count_line