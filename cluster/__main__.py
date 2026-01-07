"""
An application for clustering datasets

This file is the main entry-point for the imager application.  When you 'run the 
folder', this is the file that is executed. This file works as traffic cop that 
directs the application to the correct entry point.  It allows you to launch the 
GUI, or to do something simple from the command line.

Author: Walker M. White (wmw2)
Date:   October 26, 2024
"""
# To handle command line options
import argparse
import introcs
import os.path

def parse():
    """
    Returns: the command line arguments

    This function uses argparse to handle the command line arguments.  The benefit of
    argparse is the built-in error checking and help menu.
    """
    parser = argparse.ArgumentParser(prog='cluster',description='Application to cluster a CSV file.')
    parser.add_argument('file', type=str, nargs='?', help='the data set to process')
    parser.add_argument('k', type=str, nargs='?', help='initial cluster size')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v','--view',  dest='dim', nargs='?', const=2, default=-1, 
                       type=int, help='visualize clustering on a dataset of the given dimension')
    group.add_argument('-t','--test',  action='store_true',  
                       help='run a unit test on the cluster algorithm')
    group.add_argument('-g','--grade', action='store_true',  help='grade the assignment')
    group.add_argument('-o','--output', type=str,  help='output csv file')
    result = parser.parse_args()
    
    if result.dim == -1 and not result.test and not result.grade:
        if not result.file:
            parser.error('file is required when no flags are set.')

    if not result.k is None:
        try:
            kval = result.k
            kval = int(kval)
            assert kval > 0
        except:
            parser.error('k must be an int > 0.')

    if result.dim != -1:
        if not result.dim in [2,3]:
            parser.error('DIM must be either 2 or 3 (dimension).')
    
    return result


def get_clusters(filename,k,output):
    """
    Computes clusters on the given data set

    Parameter filename: The dataset file to use
    Precondition: dataset is a filename string or None

    Parameter k: The number of initial clusters
    Precondition: k is a int > 0
    
    Parameter output: The output file
    Precondition: output is a string or None
    """
    from tools import compute
    table = compute(filename,k)
    
    if output:
        if not os.path.splitext(output)[1]:
            output = output+'.csv'
        introcs.write_csv(table,output)
    else:
        print('\t'.join(table[0]))
        for row in table[1:]:
            print(str(row[0])+'\t'+'\t'.join(map(lambda x: '%.4f' % x,row[1:])))


def launch_gui(filename,k,dim):
    """
    Launches the gui application with the given dataset (if specified)

    Parameter filename: The dataset file to use immediately after launch
    Precondition: dataset is a filename string or None

    Parameter k: The number of initial clusters
    Precondition: k is a int > 0

    Parameter dim: The view dimension
    Precondition: dim is 2 or 3
    """
    print(dim)
    if dim == 2:
        from plot2 import Visualizer
    elif dim == 3:
        from plot3 import Visualizer
    
    Visualizer.launch(filename,k)


def unittest():
    """
    Runs a unittest on the Image and Editor classes
    """
    from a6test import test_all
    test_all()


def grade(output):
    """
    Grades the assignment.

    Parameter output: The output file for storing feedback
    Precondition: output is a filename string or None
    """
    try:
        import grade
        grade.grade(output)
    except:
        print('The grading program is not currently installed.')


def execute():
    """
    Executes the application, according to the command line arguments specified.
    """
    args = parse()
    filename = args.file
    try:
        kval = args.k
        kval = int(kval)
    except:
        kval = 3
    
    # Switch on the options
    if args.test:
        unittest()
    elif args.grade:
        grade(file)
    elif args.dim != -1:
        launch_gui(filename,kval,args.dim)
    else:
        get_clusters(filename,kval,args.output)


# Do it
execute()
