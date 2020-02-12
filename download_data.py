from subprocess import call

if True:
    call(['mkdir', '-p', 'data/n100_concentrations'])
    call(['wget', 'https://filesender.funet.fi/download.php?token=7c45b344-bea1-429e-82c2-ec8302f994eb&files_ids=100330', 
          '-O', 'data/n100_concentrations/aerosol.zip'])
    call(['unzip', 'data/n100_concentrations/aerosol.zip', '-d', 'data/n100_concentrations'])
    call(['rm', 'data/n100_concentrations/aerosol.zip'])

