
import yaml
from src.download_data import retrieve_n100, retrieve_cams_reanalysis


if __name__ == '__main__':
    try: 
        with open ('configuration.yml', 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print('Error reading the config file')
    
    if config['load_data']['n100']:
        retrieve_n100(config['data']['n100'])

    if config['load_data']['temp']:
        retrieve_cams_reanalysis(config['data']['temp'])
