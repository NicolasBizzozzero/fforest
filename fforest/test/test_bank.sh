python3 ../../setup.py install
rm -rf bank
reset
fforest data/bank.csv --delimiter-input=';' --trees-in-forest 15 --have-header --class y
