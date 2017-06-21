ensemble_experimentation ../../bank.csv --delimiter=';' --trees-in-forest 100 --have-header --class y

ensemble_experimentation ../../bank-additional.csv --delimiter=';' --trees-in-forest 100 --have-header --class y

# Voir bug_2
ensemble_experimentation ../../adult.data --delimiter=',' --trees-in-forest 100 --class -1

ensemble_experimentation ../../australian.dat --delimiter=' ' --trees-in-forest 100 --class -1

ensemble_experimentation ../../segment.dat --delimiter=' ' --trees-in-forest 100 --class -1

# /!\ Si je mets 12 arbres ou plus, tout plante
ensemble_experimentation ../../yeast.data --delimiter=' ' --trees-in-forest 11 --class -1 --id 0
