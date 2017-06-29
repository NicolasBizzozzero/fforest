python3 ../../setup.py install
rm -rf bank bank-additional adult australian segment yeast
reset
fforest data/bank.csv --delimiter-input=';' --trees-in-forest 15 --have-header --class y
fforest data/bank-additional.csv --delimiter-input=';' --trees-in-forest 15 --have-header --class y
fforest data/adult.data --delimiter-input=',' --quoting-input none --trees-in-forest 15 --class -1
fforest data/australian.dat --delimiter-input=' ' --quoting-input nonnumeric --trees-in-forest 15 --class -1
fforest data/segment.dat --delimiter-input=' ' --quoting-input nonnumeric --trees-in-forest 15 --class -1
fforest data/yeast.data --delimiter-input=' ' --quoting-input none --trees-in-forest 11 --class -1 --id 0
