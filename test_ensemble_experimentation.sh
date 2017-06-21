ensemble_experimentation ../../bank.csv --delimiter=';' --trees-in-forest 15 --have-header --class y

ensemble_experimentation ../../bank-additional.csv --delimiter=';' --trees-in-forest 15 --have-header --class y

ensemble_experimentation ../../adult.data --delimiter=',' --trees-in-forest 15 --class -1

ensemble_experimentation ../../australian.dat --delimiter=' ' --trees-in-forest 15 --class -1

ensemble_experimentation ../../segment.dat --delimiter=' ' --trees-in-forest 15 --class -1

ensemble_experimentation ../../yeast.data --delimiter=' ' --trees-in-forest 11 --class -1 --id 0
