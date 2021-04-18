import setuptools
from pathlib import Path
import wheel

sources_dir = 'src'

def data_files():
    files = [str(f) for f in Path(sources_dir, "data").glob("*") if f.is_file()]
    return [('actions_gui-data', files)]

setuptools.setup(name='warmuppy',
    version='0.1',
    description="A vocal warmup helper",
    author="Alessandro Grassi",
    author_email="alessandro@aggro.it",
    url="https://github.com/xstasi/warmuppy",
    package_dir={
        '': 'src'
    },
    package_data={
        '':['*','ui/*', 'resources/*']
    },
    data_files=data_files(),
    entry_points={
        'gui_scripts':['warmuppy = warmuppy.main:main']
    },
    packages=['warmuppy'],
)
