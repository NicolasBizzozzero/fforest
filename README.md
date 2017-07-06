# fforest
A set of tools useful for doing experiments with **fuzzy forests**.

<p align="center">
    <img src="https://github.com/NicolasBi/fforest/blob/master/fforest/res/pictures/diagram_fforest.png?raw=true" alt="diagram_fforest"/>
</p>

## Installation
`fforest` is available on <a href="https://pypi.python.org/pypi/fforest">PyPI</a>, just run
```shell
$ pip install fforest
```
in a shell to install the software.
The package creates **5** new commands :
```shell
$ fforest
$ fforest_preprocessing
$ fforest_initialization
$ fforest_learning
$ fforest_reduction
```

## Usage

## Requirements
* This software **doesn't work with Windows OSes**, this is due to the fact that Salammbo, the binary used to create Fuzzy-Trees only works with Linux distributions.
* This software can be run with **Python 3.5** and above. I do not have tested it with other Python 3 versions, but due to type hints, I suppose that it can't works with Python 2.

## Dependencies
* docopt >= 0.6.2

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
* Implement other format for the input database (each format must be changed to the CSV format during the preprocessing phase)
* Round floating values with https://stackoverflow.com/a/1317578
* Add the file `environment.json` at the root of the main directory, which will contains infos about the database, and must be created right after the preprocessing phase. This file'll then be loaded by each entry point thereafter.
* Add the --max-instances-at-once parameter, which force certains functions which loads entire databases in memory to only loads a precise amount of instances at once.
* Add the parameter --last-phase which stop the software if the precised phase is completed.
* Add the parameter --resume-phase which resume the software to precised phase.
* All entry-points (except the main) should do one phase each instead of starting to a specific phase.
* Improve the speed of the KRM algorithm. It's to slow (more than 2 hour for adult.data).

## Acknowledgments
I would like to thanks the <a href="http://lfi.lip6.fr/web/">LFI team</a> from the <a href="https://www.lip6.fr/">LIP6 laboratory</a>, and specifically <a href="http://webia.lip6.fr/~marsala/christophe/Accueil.html">Mr. Marsala Christophe</a>, for helping me during the entire duration of my internship, and for offering me the knowledge and resources needed to build this software.

## License
This project is licensed under the !!! License - see the [LICENSE.txt](LICENSE.txt) file for details.

<p align="center">
    <img src="https://github.com/NicolasBi/fforest/blob/master/fforest/res/pictures/logo_upmc.png?raw=true" alt="logo_upmc" height="110" width="250" align="middle"/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <img src="https://github.com/NicolasBi/fforest/blob/master/fforest/res/pictures/logo_lip6.png?raw=true" alt="logo_lip6" align="middle"/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <img src="https://github.com/NicolasBi/fforest/blob/master/fforest/res/pictures/logo_lfi.png?raw=true" alt="logo_lfi" align="middle"/>
</p>
