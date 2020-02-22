
import yaml
from src.download_data import retrieve_n100, retrieve_cams_reanalysis
from src.preprocess_data import preprocess_n100, preprocess_cams, unite_data


if __name__ == '__main__':
    try: 
        with open ('configuration.yml', 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print('Error reading the config file')
    
    if config['load_data']['n100']:
        retrieve_n100(config['raw']['n100'])

    if config['preprocess']['n100']:
        preprocess_n100(config['raw']['n100'], config['data']['n100'], config['cities'])

    if config['load_data']['cams']:
        retrieve_cams_reanalysis(config['data']['n100'], config['raw']['cams'], config['cities'])

    if config['preprocess']['cams']:
        preprocess_cams(config['raw']['cams'], config['data']['cams'], config['cities'])
    
    if config['preprocess']['unite']:
        unite_data(config['data']['n100'], config['data']['cams'], config['cities'], config['data']['final'])

