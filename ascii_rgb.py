#!/usr/bin/python3
import argparse
import logging
import os
import sys

codes = {
'COLOR_NC':    '\e[0m',
'BLACK':       '\e[0;30m',
'GRAY':        '\e[1;30m',
'RED':         '\e[0;31m',
'LIGHT_RED':   '\e[1;31m',
'GREEN':       '\e[0;32m',
'LIGHT_GREEN': '\e[1;32m',
'BROWN':       '\e[0;33m',
'YELLOW':      '\e[1;33m',
'BLUE':        '\e[0;34m',
'LIGHT_BLUE':  '\e[1;34m',
'PURPLE':      '\e[0;35m',
'LIGHT_PURPLE':'\e[1;35m',
'CYAN':        '\e[0;36m',
'LIGHT_CYAN':  '\e[1;36m',
'LIGHT_GRAY':  '\e[0;37m',
'WHITE':       '\e[1;37m'
}

matrix = []

def show_palette():
    text = "#!/bin/bash\n"

    ordered_keys = ['WHITE',
    'LIGHT_GRAY',
    'BLUE',
    'LIGHT_BLUE',
    'LIGHT_PURPLE',
    'PURPLE',
    'LIGHT_RED',    
    'RED',
    'CYAN',
    'LIGHT_CYAN',
    'YELLOW',
    'LIGHT_GREEN',
    'GREEN',    
    'BROWN',
    'GRAY',
    'BLACK']
    for key in ordered_keys:
        text += "echo -e '" + codes[key] + "@@@@@@@@@@@@@@@@@@@@@@ " + key + "';\n"

    f = open('palette','w').write(text)
    os.system('chmod u+x palette')
    os.system('./palette')

def get_args():
    parser = argparse.ArgumentParser(description='Colorize your ASCII art')
    
    parser.add_argument("--ascii", help="input ASCII art file")
    parser.add_argument("--colors", help="input colors file")
    parser.add_argument("--out", help="output bash script with colored ASCII art")
    parser.add_argument("--debug", "-d", help="debug", action="store_true")
    parser.add_argument("--show", "-s", help="show colored ascii art", action="store_true")
    parser.add_argument("--palette", "-p", help="show color palette", action="store_true")
    args = parser.parse_args()
    return args

def color_text(args):

    colored_ascii=args.ascii+'.sh'
    if args.out:
        colored_ascii = args.out
    text = ''

    i=0
    for line in open(args.ascii,'r').readlines():
        logging.debug("Parsing line: %s", line)
        j=0
        for character in line:
            if character == '\n':
                break
            logging.debug("'%s', i: %d, j: %d, color: %s" % (character,i,j,matrix[i][j])) 
            close_echo = "';"
            if j == (len(line)-1):
                close_echo = "\n\';"
            
            escaped_character = character
                
            text += "echo -n -e '"+codes[matrix[i][j]]+escaped_character+close_echo+"\n"
            j+=1
        text += "echo;\n"
        i+=1

    text = "#!/bin/bash\n\n"+text
    f = open(colored_ascii,'w').write(text)
    os.system('chmod u+x %s' % colored_ascii)
    return colored_ascii

def parse_colors(args):
    desired_colors=args.ascii+'.colors'
    if args.colors:
        desired_colors=args.colors
    lines = open(desired_colors,'r')
    for line in lines:
        # a line if of the form: color,start_line,start_column,end_line,end_column
        content = line.split(',')
        color = content[0]
        start_line = int(content[1])-1
        start_column = int(content[2])-1
        end_line = int(content[3])-1
        end_column = int(content[4][:-1])-1 # get rid of newline
        logging.debug(content)
        logging.debug("start line: %d, start column: %d; end line: %d, end column: %d" % (start_line, start_column, end_line, end_column))
        while start_column < min(len(matrix[start_line]),end_column):
            matrix[start_line][start_column] = color
            start_column += 1

def init_matrix(args):
    lines = open(args.ascii, 'r').readlines()
    i=0
    for line in lines:
        matrix.append([])
        for character in line:
            matrix[i].append('COLOR_NC')
        i+=1

def set_logging(args):
    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG
    logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)

def main():
    args = get_args()

    if args.palette:
        show_palette()
        return
    set_logging(args)
    init_matrix(args)
    parse_colors(args)
    colored_ascii = color_text(args)

    if args.show:
        os.system('./'+colored_ascii)

if __name__ == '__main__':
    sys.exit(main())

