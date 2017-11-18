#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:33:15 2016

@author: mlasserre
"""

from __future__ import division

__author__ = "MOIRA LASSERRE"
__credits__ = ["MOIRA_LASSERRE"]
__license__ = "MIT"
__version__ = "1.0dev"
__maintainer__ = "MOIRA_LASSERRE"
__email__ = "mlasserre@pasteur.edu.uy"
__status__ = "Development"


from cogent.util.option_parsing import parse_command_line_parameters, make_option
from cogent import LoadSeqs

script_info = {}
script_info['brief_description'] = "Keep only variable sites from alignment"
script_info['script_description'] = "From a fasta alignment file, create a new fasta with only the variant nucleotides, leaving out the constant sites."
script_info['script_usage'] = [\
 ("",
  "Get variable sites from sequences in a fasta file and write results to out.fasta.",
  "%prog -i in.fasta -o out.fasta")]
script_info['output_description']= "Fasta file"
script_info['required_options'] = [\
    make_option('-i','--input_dir',type="existing_filepath",help='the input fasta'),\
    make_option('-o','--output_dir',type="string",help='the output fasta')
]
#script_info['optional_options'] = [\
 # Example optional option
 #make_option('-o','--output_dir',type="new_dirpath",help='the output directory [default: %default]'),\
#] --> later: can extract the constant on a separate file too, maybe
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    
    fastaInput = opts.input_dir
    fastaOut = opts.output_dir
    out = open(fastaOut, 'w')

   


    
    onlyVars = getVariable(fastaInput)    
    onlyVars[0]
    out.writelines(str(onlyVars))
        
    out.close()
    

def getVariable(aln):
    
    pyAln = LoadSeqs(aln)
    return pyAln.filtered(lambda x: len(set(x)) > 1)
    

if __name__ == "__main__":
    main()
    
    
    
    
    