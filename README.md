# fforest
<p align="center">
    <img src="https://github.com/NicolasBi/fforest/blob/master/fforest/res/pictures/diagram_fforest.png?raw=true" alt="diagram_fforest"/>
    <br> Your database is split into multiple sub-databases. This configuration is the one mainly used by Data-Scientists and Researchers in Machine-Learning.
</p>

With the help of the <a href="http://webia.lip6.fr/~marsala/Salammbo/">Salammbô</a> software, **fforest** construct Decision Trees and Fuzzy Decision Trees from the sub-sub-train databases, using a handful of Triangular Norms.
These trees then produces multiple

## Installation
`fforest` is available on <a href="https://pypi.python.org/pypi/fforest">PyPI</a>, just run
```shell
$ pip install fforest
```
in a shell to install the software.
The package creates **1** new commands :
```shell
$ fforest
```

## Usage

## Requirements
* This software **doesn't work with Windows OSes**, this is due to the fact that Salammbô, the binary used to create Fuzzy-Trees only works with GNU/Linux distributions.
* This software can be run with **Python 3.5** and above. It hasn't been tested with other Python 3 versions, but due to type hints, it should works with Python 3.4.

## Dependencies
* docopt >= 0.6.2
* numpy >= 1.12.1

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
* Add the --max-instances-at-once parameter, which force some functions which loads entire databases in memory to only loads a precise amount of instances at once.
* Clean all the non-main entry points documentation inside the entry_points_documentation.xml file.
* The code inside the args_cleaner.py and init_environment.py modules is working but is very ugly and thus, difficult to maintain. A better idea is welcome.

## Acknowledgments
I would like to thanks the <a href="http://lfi.lip6.fr/web/">LFI team</a> from the <a href="https://www.lip6.fr/">LIP6 laboratory</a>, and specifically <a href="http://webia.lip6.fr/~marsala/christophe/Accueil.html">Mr. Marsala Christophe</a>, for helping me during the entire duration of my internship, and for offering me the knowledge and resources needed to build this software.

## License
This project is licensed under the !!! License - see the [LICENSE.txt](LICENSE.txt) file for details.

<p align="center">
    <img src="https://github.com/NicolasBi/fforest/blob/master/fforest/res/pictures/logo_upmc.png?raw=true" alt="logo_upmc" height="110" width="250" align="middle"/>
    <img src="https://github.com/NicolasBi/fforest/blob/master/fforest/res/pictures/logo_lip6.png?raw=true" alt="logo_lip6" align="middle"/>
    <img src="https://github.com/NicolasBi/fforest/blob/master/fforest/res/pictures/logo_lfi.png?raw=true" alt="logo_lfi" align="middle"/>
</p>
