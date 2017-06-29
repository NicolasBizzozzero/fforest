rm -rf bank bank-additional adult australian segment yeast
fforest fforest/test/data/bank.csv --delimiter-input=';' --trees-in-forest 15 --have-header --class y
fforest fforest/test/data/bank-additional.csv --delimiter-input=';' --trees-in-forest 15 --have-header --class y
fforest fforest/test/data/adult.data --delimiter-input=',' --quoting-input none --trees-in-forest 15 --class -1
fforest fforest/test/data/australian.dat --delimiter-input=' ' --quoting-input nonnumeric --trees-in-forest 15 --class -1
fforest fforest/test/data/segment.dat --delimiter-input=' ' --quoting-input nonnumeric --trees-in-forest 15 --class -1
fforest fforest/test/data/yeast.data --delimiter-input=' ' --quoting-input none --trees-in-forest 11 --class -1 --id 0
