

import argparse

import pickle

from main.org.core.utility.Chromosome_Generator import ChromosomeGenerator
from main.org.core.metaheuristics.NSGA_II_2D import main


"""
    this script is a wrapper for the MoLFI tool and can be used from the command line as following
    under the SB_Template_Extraction:
    run the MoLFI script with the required arguments:
        python3.6 path/to/MoLFI.py -l [logfile.log] -f [log_format] -p [serialize_file]

        Optional parameters are: the list of regex with -r/--regex

"""

cmdline = argparse.ArgumentParser(
    usage="\
    \t MoLFI.py --log logfile.txt --format '<ts> <level> <message>' --regex $'rx1' $'rx2' $'rx3' --pklfile serialze_file\n \
    \t--log: \t\t\t the log file\n \
    \t--format: \t\t a log format for log lines (e.g., <timestamp> <level> <message>)\n\
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
cmdline.add_argument('--format',
                     '-f',
                     action='store',
                     help=r"The log format for a line (e.g., <date> <message>)",
                     dest='aformat',
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
chrom_gen = ChromosomeGenerator(str(args.alog), str(args.aformat), regex=regx)
pareto = main(chrom_gen)

# serialize the pareto solution to a file
binary_file = open(args.apklfile, mode='wb')
pickle.dump(pareto, binary_file)
binary_file.close()
