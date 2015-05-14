#  _________________________________________________________________________
#
#  Acro: A Common Repository for Optimizers
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the README.txt file in the top Acro directory.
#  _________________________________________________________________________

import sys
from random import *

numAminoAcids=20
numRotamers=4

def energy():
  return -1.0

numPeptides = eval(sys.argv[1])
ofilename = sys.argv[2]

ofile = open(ofilename,'w')

ofile.write("#\n")
ofile.write("# Generated by gendata\n")
ofile.write("# This file assumes that all rotamers are represented at all\n")
ofile.write("# positions.  However, the input format can allow for a \n")
ofile.write("# flexible representation, since each rotamer is labeled\n")
ofile.write("# with the corresponding amino acid label.\n")
ofile.write("#\n")
ofile.write("\n")

ofile.write("#\n")
ofile.write("# Number of peptides\n")
ofile.write("#\n")
ofile.write("param n := " + `numPeptides` + ";\n")
ofile.write("\n")

ofile.write("#\n")
ofile.write("# The amino acids that are considered for each side chain site\n")
ofile.write("#\n")
ofile.write("set ValidAminoAcids := \n")
for i in range(0,numPeptides):
  for j in range(0,20):
    ofile.write("(" + `i+1` + "," + `j+1` + ")\n")
ofile.write(";\n")
ofile.write("\n")

ofile.write("#\n")
ofile.write("# Boltzman Protein-Rotamer energies\n")
ofile.write("#\n")
ofile.write("param B_inter := [*,*]\n")
for i in range(0,numPeptides):
  for j in range(0,20):
    val = energy()
    ofile.write(`i+1` + " " + `j+1` + " " + `val` + "\n")
ofile.write(";\n")
ofile.write("\n")

ofile.write("#\n")
ofile.write("# Boltzman Rotamer-Rotamer energies\n")
ofile.write("#\n")
ofile.write("param B_intra := [*,*,*,*]\n")
for i in range(0,numPeptides):
  for j in range(0,20):
    for ii in range(0,numPeptides):
      for jj in range(0,20):
        if i < ii:
	   val = energy()
           ofile.write(`i+1` + " " + `j+1` + " " + `ii+1` + " " + `jj+1` + " " + `val` + "\n")
ofile.write(";\n")
ofile.write("\n")

ofile.write("#\n")
ofile.write("# Number of rotamers for each peptide\n")
ofile.write("#\n")
ofile.write("param rCount := \n")
total=0
for i in range(0,numAminoAcids):
  total=total+numRotamers+i
for i in range(0,numPeptides):
  ofile.write(`i+1` + " " + `total` + "\n")
ofile.write(";\n")
ofile.write("\n")


ofile.write("#\n")
ofile.write("# Protein-Rotamer energies and Rotamer amino acid labels\n")
ofile.write("#\n")
ofile.write("param: ValidInterIndicesRR: E_inter RotamerLabel :=\n")
for i in range(0,numPeptides):
  k = 0
  next = numRotamers
  aa = 1
  for j in range(0,total):
    val = energy()
    ofile.write(`i+1` + " " + `j+1` + " " + `val` + " " + `aa` + "\n")
    k = k+1
    if k == next:
       next = next + numRotamers+aa
       aa = aa + 1
ofile.write(";\n")
ofile.write("\n")

ofile.write("#\n")
ofile.write("# Rotamer-Rotamer energies\n")
ofile.write("#\n")
ofile.write("param: ValidIntraIndicesRR: E_intra := \n")
for i in range(0,numPeptides):
  for j in range(0,total):
    for ii in range(0,numPeptides):
      for jj in range(0,total):
        if i < ii:
	   val = energy()
           ofile.write(`i+1` + " " + `j+1` + " " + `ii+1` + " " + `jj+1` + " " + `val` + "\n")
ofile.write(";\n")
ofile.write("\n")

