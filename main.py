from sys import path
from pathlib import Path
path.append(str(Path(__file__).parent) + '/src')
from warmuppy.main import main
main()
