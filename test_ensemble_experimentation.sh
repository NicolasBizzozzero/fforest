ensemble_experimentation ../data_backup/bank.csv --delimiter=';' --trees-in-forest 15 --have-header --class y

ensemble_experimentation ../data_backup/bank-additional.csv --delimiter=';' --trees-in-forest 15 --have-header --class y

ensemble_experimentation ../data_backup/adult.data --delimiter=',' --trees-in-forest 15 --class -1

ensemble_experimentation ../data_backup/australian.dat --delimiter=' ' --trees-in-forest 15 --class -1

ensemble_experimentation ../data_backup/segment.dat --delimiter=' ' --trees-in-forest 15 --class -1

ensemble_experimentation ../data_backup/yeast.data --delimiter=' ' --trees-in-forest 11 --class -1 --id 0
