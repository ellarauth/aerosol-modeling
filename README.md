# aerosol-modeling
Aerosol concentration modeling based on satellite data

Run source code:
1. Configure as you wish in `configuration.yml`
2. Run `python main.py`

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
In case of problems with the environment:
```
conda create -n inar python=3.5.6
conda install -c anaconda pyyaml
conda install -c conda-forge cfgrib
conda install -c conda-forge ecmwf-api-client
conda install -c conda-forge jupyterlab
etc ...
conda activate inar
```

## Data Retrieval

1. Log in to https://ecmwf.int

2. Save credentials at https://api.ecmwf.int/v1/key/ to `$HOME/.ecmwfapirc`

3. Specify `load_data` in `configuration.yml`

4. Run `python main.py`

### CAMS Reanalysis

Reanalysis data documentation

https://confluence.ecmwf.int/display/CKB/CAMS%3A+Reanalysis+data+documentation

Data

https://apps.ecmwf.int/data-catalogues/cams-reanalysis/?stream=oper&levtype=ml&expver=eac4&type=an&class=mc

Efficiently retrieve daily data

https://confluence.ecmwf.int/display/WEBAPI/CAMS+Reanalysis+daily+retrieval+efficiency

Atmospheric model (we use 60, i.e. 10m above ground)

https://www.ecmwf.int/en/forecasts/documentation-and-support/60-model-levels

Reference CAMS: _'Generated using Copernicus Atmosphere Monitoring Service Information 2020'._

https://confluence.ecmwf.int/pages/viewpage.action?pageId=58131166  

### N100

Datasource:

In situ by INAR

### Retrieve data on disks

Faster transfer speeds for future reference, released recently

https://ads.atmosphere.copernicus.eu/

### Large File Storage

https://git-lfs.github.com/

Install (debian):
```
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
```

List files
```
git lfs ls-files
```

To download them (after installing lfs)
```
git lfs pull
```