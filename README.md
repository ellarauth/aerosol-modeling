# aerosol-modeling
Aerosol concentration modeling based on satellite data

Log in to https://ecmwf.int

Save credentials at https://api.ecmwf.int/v1/key/ to `$HOME/.ecmwfapirc`

Run src code (load data etc):
1. Configure as you wish in `configuration.yml`
2. Run `python main.py`

Save credentials at https://api.ecmwf.int/v1/key/ to $HOME/.ecmwfapirc

If using conda:
```
git clone https://github.com/hd4niel/aerosol-modeling.git
cd aerosol-modeling
conda env create -f environment.yml
conda activate inar
jupyter lab
conda deactivate inar
```
New dependencies
```
conda env export --no-builds | grep -v "^prefix: " > environment.yml
```
Remove environment
```
conda env remove --name inar
```
