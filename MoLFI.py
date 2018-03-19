

import argparse

import pickle

from main.org.core.utility.Chromosome_Generator import ChromosomeGenerator
from main.org.core.metaheuristics.NSGA_II_2D import main


"""
    this script is a wrapper for the MoLFI tool and can be used from the command line as following
    under the SB_Template_Extraction:
    run the MoLFI script with the required arguments:
        python3.6 path/to/MoLFI.py -l [logfile.log] -c [msg_pos] -s [char_separator] -p [serialize_file]

        Optional parameters are: the list of regex with -r/--regex

"""

cmdline = argparse.ArgumentParser(
    usage="\
    \t MoLFI.py --log logfile.txt --seperator 'char' --column msg_pos --regex $'rx1' $'rx2' $'rx3' --pklfile serialze_file\n \
    \t--log: \t\t\t the log file\n \
    \t--seperator: \t\t a specific charchter (string) that seperates the columns of the log file\n\
    \t--column: \t\t the index of the log messages column\n \
    \t--pklfile: \t\t the file where to save the serialized generated templates\n \
    \t--regex: \t\t a list of regular expressions that detects domain knowledge variables",
    description='MoLFI: Multi-Objective Log Message Format Identification:\n \
                                Identify Log Message Formats from a given log file.')
cmdline.add_argument('--log',
                     '-l',
                     action='store',
                     help=r'the log file to analyze',
                     dest='alog',
                     required=True
                     )
cmdline.add_argument('--separator',
                     '-s',
                     action='store',
                     help=r"The separator between the log's columns",
                     dest='aseparator',
                     required=True
                     )
cmdline.add_argument('--column',
                     '-c',
                     action='store',
                     help=r"The column number of the log messages",
                     dest='acolumn',
                     required=True
                     )
cmdline.add_argument('--regex',
                     '-r',
                     action='store',
                     help=r'The list of Domain Knowldge regular expressions',
                     dest='aregex',
                     nargs="*",
                     required=False
                     )
cmdline.add_argument('--pklfile',
                     '-p',
                     action='store',
                     help=r"The pickle file where to save the serialized object",
                     dest='apklfile',
                     required=True
                     )

args = cmdline.parse_args()

# if all the requirement arguments are provided, start the process

if args.aregex:
    regx = args.aregex

else:
    regx = None

# Load log messages
chrom_gen = ChromosomeGenerator(str(args.alog), int(args.acolumn), str(args.aseparator), regex=regx)
pareto = main(chrom_gen)

# serialize the pareto solution to a file
binary_file = open(args.apklfile,mode='wb')
my_pickled_mary = pickle.dump(pareto, binary_file)
binary_file.close()
