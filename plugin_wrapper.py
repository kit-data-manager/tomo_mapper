# run_mapping.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from tomo_mapper.mapping_main import run_cli

if __name__ == "__main__":
    # Extract arguments from the command line
    sys.argv = ["mapping_cli", "sem"] + sys.argv[1:]

    # Call the run_cli function
    run_cli()
