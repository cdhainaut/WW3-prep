import argparse
from pathlib import Path
import requests
import datetime as dt
import json
import ftplib
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(
        description="Download WW3 NetCDF files from IFREMER."
    )
    parser.add_argument(
        "--ftp",
        action="store_true",
        help="Download via FTP instead of HTTPS",
    )
    parser.add_argument(
        "--credentials",
        type=str,
        default="ftp_credentials.json",
        help="JSON containing FTP credentials (if using FTP)",
    )

    parser.add_argument(
        "-z",
        "--zone",
        default="MANCHE-NORD-500M",
        help="Zone to download (e.g., MANCHE-NORD-500M or FINIS-200M)",
    )
    parser.add_argument(
        "-d",
        "--days_fwd",
        type=int,
        default=3,
        help="How many days forward from today to download (0 = today, 2 = +2 days)",
    )
    parser.add_argument(
        "--start_date",
        type=str,
        default=None,
        help="Start date in YYYY-MM-DD format (default: tomorrow UTC)",
    )
    parser.add_argument(
        "--download_dir", default="ww3_data", help="Directory to save downloaded files"
    )
    args = parser.parse_args()

    zone = args.zone
    days_fwd = args.days_fwd
    download_dir = Path(args.download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)

    base_url = f"https://data-dataref.ifremer.fr/marc/ww3/{zone}/best_estimate/2025/"

    # Determine start date
    if args.start_date:
        start_date = dt.datetime.strptime(args.start_date, "%Y-%m-%d").replace(
            tzinfo=dt.timezone.utc
        )
    else:
        today = dt.datetime.utcnow().date()
        start_date = dt.datetime.combine(
            today, dt.time(0), tzinfo=dt.timezone.utc
        ) + dt.timedelta(days=1)

    # Generate target filenames
    target_files = []
    for delta in range(0, days_fwd + 1):
        day = start_date + dt.timedelta(days=delta)
        date_str = day.strftime("%Y%m%d")
        for hour in range(24):
            filename = f"MARC_WW3-{zone}_{date_str}T{hour:02d}Z.nc"
            target_files.append(filename)

    downloaded_files = []
    if args.ftp:
        # Lecture des identifiants
        with open(args.credentials, "r") as f:
            creds = json.load(f)
            ftp_host = "ftp.ifremer.fr"
            ftp_user = creds["user"]
            ftp_pass = creds["password"]
            ftp_dir = f"/MARC_WW3/{zone}/best_estimate/2025/"

            with ftplib.FTP(ftp_host) as ftp:
                ftp.login(ftp_user, ftp_pass)
                ftp.cwd(ftp_dir)
                for filename in tqdm(target_files, desc="FTP download WW3"):
                    local_path: Path = download_dir / filename
                    if local_path.exists():
                        downloaded_files.append(str(local_path))
                        continue
                    try:
                        with open(local_path, "wb") as f:
                            ftp.retrbinary(f"RETR {filename}", f.write)
                        downloaded_files.append(str(local_path))
                    except Exception as e:
                        print(f"Error FTP download {filename}: {e}")
    else:
        # Download files
        for filename in tqdm(target_files, desc="Downloading WW3 files"):
            url = base_url + filename
            local_path = download_dir / filename
            if local_path.exists():
                downloaded_files.append(str(local_path))
                continue
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(response.content)
                    downloaded_files.append(str(local_path))
            except Exception as e:
                print(f"Error downloading {filename}: {e}")


if __name__ == "__main__":
    main()
