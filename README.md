# WW3 Downloader & Processor

Allows you to download NetCDF files from the WW3 model (Ifremer), prepare them for GRIB2 conversion compatible with QtVlm, and concatenate them.

## Prerequisites

- Python 3.8+
- `requests`
- `xarray`
- `tqdm`
- `cdo` (for NetCDF → GRIB2 conversion)

Install Python dependencies:

```bash
pip install requests xarray tqdm
```

Install CDO (on Ubuntu/Debian):

```bash
sudo apt-get install cdo
```

## Usage

### 1. Download NetCDF files

You can download the files via HTTPS (default) or FTP (using the `--ftp` option).

#### a) Download via HTTPS

```bash
python dl_files.py --zone MANCHE-NORD-500M --days_fwd 2 --download_dir ww3_data
```

#### b) Download via FTP

Prepare a credentials file (e.g. `ftp_credentials.json`):

```json
{
  "user": "ext-marc_vagues",
  "password": "YOUR_PASSWORD_HERE"
}
```

Then run the command:

```bash
python dl_files.py --zone MANCHE-NORD-500M --days_fwd 2 --download_dir ww3_data --ftp --credentials ftp_credentials.json

```

- `--zone`: name of the zone (e.g., MANCHE-NORD-500M, FINIS-200M)
- `--days_fwd`: number of days to download starting from the start date
- `--ftp`: enables FTP download
- `--credentials`: path to the JSON file containing FTP credentials
- `--download_dir`: destination folder

### 2. Preprocess and concatenate the files

```bash
python process_files.py ww3_data/*.nc --output manchesud.nc --processed_dir processed_nc

```

- `--output` : name of the concatenated NetCDF file
- `--processed_dir` : folder for the processed NetCDF files

3. Convert to QtVlm-compatible GRIB2

Use the following command:

```bash
cdo -f grb2 copy manchesud.nc manchesud.grb2
```
