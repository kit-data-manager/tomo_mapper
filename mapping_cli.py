import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from tomo_mapper.mapping_main import run_cli

if __name__ == '__main__':
    run_cli()