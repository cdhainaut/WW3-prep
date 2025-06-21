import argparse
from pathlib import Path
import xarray as xr
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", help="List of files to process")
    parser.add_argument(
        "-o",
        "--output",
        default="for_grib.nc",
        help="Output concatenated file",
    )
    parser.add_argument(
        "-p",
        "--processed_dir",
        default="processed_nc",
        help="Directory for processed NetCDF files",
    )
    args = parser.parse_args()

    downloaded_files = args.files
    processed_files = []

    # === GRIB2-compatible variable renaming ===
    VAR_MAP = {
        "ucur": "UGRD",  # ocean current zonal
        "vcur": "VGRD",  # ocean current meridional
        "hs": "swh",  # significant wave height
        "dp": "pwd",  # peak wave direction
    }

    processed_dir = Path(args.processed_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)

    for file in tqdm(downloaded_files, desc="Processing files"):
        try:
            file_path = Path(file)
            ds = xr.open_dataset(file_path)
            available_vars = set(ds.data_vars)

            selected_keys = [k for k in VAR_MAP if k in available_vars]

            if not selected_keys:
                print(f"Skipping {file_path}: no matching variables found.")
                ds.close()
                continue

            # Rename variables
            subset = ds[selected_keys].rename({k: VAR_MAP[k] for k in selected_keys})

            output_path = processed_dir / file_path.name
            subset.to_netcdf(output_path, format="NETCDF4_CLASSIC")
            processed_files.append(output_path)
            ds.close()

        except Exception as e:
            print(f"Error processing {file}: {e}")

    # === Combine all processed .nc files ===
    if processed_files:
        print("Combining all processed NetCDF files...")
        datasets = [xr.open_dataset(str(f)) for f in processed_files]
        combined_ds = xr.concat(datasets, dim="time")
        combined_ds.to_netcdf(args.output, format="NETCDF4_CLASSIC")
        print(f"Saved: {args.output} (ready for GRIB conversion)")
    else:
        print("No files to process.")


if __name__ == "__main__":
    main()
