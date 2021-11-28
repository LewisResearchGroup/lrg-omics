#!/bin/bash

if [[ $1 = '--version' ]]; then
    echo "lrg_fake_maxquant.sh v0"
    exit 256

elif [[ $1 == *.xml ]]; then
    mkdir combined
    mkdir combined/txt
    touch combined/txt/210913-Mario__mqpar_no_FDR.xml   
    touch combined/txt/evidence.txt       
    touch combined/txt/matchedFeatures.txt   
    touch combined/txt/maxquant.out                       
    touch combined/txt/ms3Scans.txt    
    touch combined/txt/msms.txt     
    touch combined/txt/'Oxidation (M)Sites.txt'   
    touch combined/txt/peptides.txt        
    touch combined/txt/summary.txt   
    touch combined/txt/time.txt
    touch combined/txt/allPeptides.txt                  
    touch combined/txt/libraryMatch.txt
    touch combined/txt/modificationSpecificPeptides.txt
    touch combined/txt/msmsScans.txt
    touch combined/txt/mzRange.txt
    touch combined/txt/parameters.txt
    touch combined/txt/proteinGroups.txt
    touch combined/txt/tables.pdf
    touch maxquant.err
    touch maxquant.out
fi

exit 5
