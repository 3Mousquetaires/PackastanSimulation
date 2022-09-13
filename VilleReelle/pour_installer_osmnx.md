== POUR INSTALLER CETTE LIB A LA CON ==
 * installer conda
 * depuis l'anaconda powershell prompt :
    `conda config --prepend channels conda-forge`
    `conda create -n ox --strict-channel-priority osmnx`
    `conda activate ox` 
    (aucune idée de si c'est nécessaire)

 * maintenant avec pip :
    `pip install osmnx`
    Si problèmes sur Fiona
    `pip install pipwin`
    `pipwin install gdal`
    `pipwin install fiona`
    `pip install osmnx`

