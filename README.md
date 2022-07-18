[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ivoa/modelinstanceinvot-code/package)

### Python Workflow

This project contains code sample for processing annotated VOTables.
- We are using the annotation [syntax](https://github.com/ivoa-std/ModelInstanceInVot) that has been designed after the 2021 workshop.\n",

### Table of content
- `jupyter`: Four notebook running the MIVOT parser in differdent contexts
- `mivot_code`: all Python code
- `tests`: Unt test suite
- `photdm_builder` Simple scipt building photometric calibrations (PhotDM) instances from SVO-PFS output
- `data` : old stuff that will be soon thrown away

### Runnig some code

#### From Jupyter
```shell
# if not already done
pip3 install jupyter-lab
pip3 install -r requirements.txt

cd jupyter
jupyter-lab
# jump to your browser
```
#### From a clone
```shell
git clone git@github.com:ivoa/modelinstanceinvot-code.git

# if not already done
pip3 install -r requirements.txt

cd modelinstanceinvot-code/mivot-code/examples

# Let's get MANGO instances
python example.1.xtapdb.meas_ass.py 
```
#### From PIP

The package contains only standalone module; this a client for the XTapDB service (https://xcatdb.unistra.fr/xtapdb) which provides on the fly anotated VOTables. 

```shell
pip install git+ssh://github.com:ivoa/modelinstanceinvot-code.git

xtapdb-client 'select * from catalogueentry'
```
