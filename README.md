# WW3 Downloader & Processor

Permet de télécharger des fichiers NetCDF issus du modèle WW3 (Ifremer), de les préparer pour une conversion GRIB2 compatible QtVlm, et de les concaténer.

## Prérequis

- Python 3.8+
- `requests`
- `xarray`
- `tqdm`
- `cdo` (pour la conversion NetCDF → GRIB2)

Installer les dépendances Python :

```bash
pip install requests xarray tqdm
```

Installer CDO (sous Ubuntu/Debian) :

```bash
sudo apt-get install cdo
```

## Utilisation

1. Télécharger les fichiers NetCDF

```bash
python dl_https.py--zone MANCHE-NORD-500M --days_fwd 2 --download_dir ww3_data
```

- `--zone` : nom de la zone (ex : MANCHE-NORD-500M, FINIS-200M)
- `--days_fwd` : nombre de jours à télécharger à partir de la date de départ
- `--download_dir` : dossier de destination

2. Prétraiter et concaténer les fichiers

```bash
python process_files.py ww3_data/*.nc --output manchesud.nc --processed_dir processed_nc

```

- `--output` : nom du fichier NetCDF concaténé
- `--processed_dir` : dossier pour les fichiers NetCDF traités

3. Conversion en GRIB2 compatible QtVlm

Utiliser la commande suivante :

```bash
cdo -f grb2 copy manchesud.nc manchesud.grb2
```
