# fforest
A set of tools useful for doing experiments with fuzzy forests.

[[https://github.com/NicolasBi/fforest/fforest/res/pictures/diagram_fforest.png|alt=diagram_fforest]]

## Installation
`fforest` is available on PyPi, just run
```shell
$ pip install fforest
```
in a shell to install the software.
The package creates 5 new commands :
```shell
$ fforest
$ fforest_preprocessing
$ fforest_initialization
$ fforest_learning
$ fforest_reduction
```

## Usage

## Requirements
* This software doesn't work with Windows OSes, this is due to the fact that reading CSV files with a Windows system does not operate correctly.
* This software can be run with Python 3.5 and above. I do not have tested it with other Python 3 versions, but due to type hints, I suppose that it can't works with Python 2.

## Dependencies
* docopt >= 

## Contributing
1. Fork the project.
2. Create your feature branch : `git checkout -b my-new-feature`.
3. Commit your changes : `git commit -am 'Added some cool feature !'`.
4. Push to the branch  : `git push origin my-new-feature`.
5. Submit a pull request.

## Todo
* Implement the `guess` option for the parameter --have-header with the help of this code snippet : https://docs.python.org/3/library/csv.html#csv.Sniffer.has_header
* Implement the `guess` option for the parameters --delimiter, --quoting, --quote-character and --encoding.
* Add more messages related to the verbosity
* Add some progress bars with the package : https://pypi.python.org/pypi/progressbar2
* Rewrite all path processing code with the package : https://pypi.python.org/pypi/path.py
* Save each directory path in the `env` module
* Save each database path in the `env` module
* Implement other format for the input database (each format must be changed to the CSV format during the preprocessing phase)
* Add a variable `completed_phase` in the `env` module.
* Add the file `environment.json` at the root of the main directory, which will contains infos about the database, and must be created right after the preprocessing phase. This file'll could then be loaded by each entry point thereafter.

## Acknowledgments
I would like to thanks the LFI team from the LIP6 laboratory, and specifically Mr. Marsala Christophe, for helping me during the entire duration of my internship, and for offering me the knowledge and resources needed to build this software.
