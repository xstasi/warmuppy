import setuptools
import wheel # noqa
import os
import PySide6
from pathlib import Path
from distutils.command.build import build
from subprocess import Popen, PIPE

ui_dir = os.path.join('src', 'warmuppy', 'ui', 'dialogs')
resources_dir = os.path.join('src', 'warmuppy', 'resources')


class MyBuilder(build):
    @staticmethod
    def qt_tool_wrapper(qt_tool, args):
        # Taking care of pyside2-uic, pyside2-rcc, and pyside2-designer
        # listed as an entrypoint in setup.py
        pyside_dir = os.path.dirname(PySide6.__file__)
        exe = os.path.join(pyside_dir, 'Qt', 'libexec', qt_tool)

        cmd = [exe] + args
        proc = Popen(cmd, stderr=PIPE)
        out, err = proc.communicate()
        if err:
            msg = err.decode("utf-8")
            print("Error: {}\nwhile executing '{}'".format(msg, ' '.join(cmd)))
        return proc.returncode

    def uic(self, a, b):
        self.qt_tool_wrapper("uic", ['-g', 'python', '-o', b, a])

    def rcc(self, a, b):
        self.qt_tool_wrapper("rcc", ['-g', 'python', '-o', b, a])

    def run(self):
        for ui_file in list(Path(ui_dir).glob('*.ui')):
            ui_file_name = str(ui_file)[0:-3]
            print(f"Compiling UI file {ui_file_name}")
            self.uic(f"{ui_file_name}.ui", f"{ui_file_name}.py")
        for resource_file in list(Path(resources_dir).glob('*.qrc')):
            file_name = str(resource_file)[0:-4]
            print(f"Compiling resource file {file_name}")
            self.rcc(f"{file_name}.qrc", f"{file_name}.py")
        super().run()


setuptools.setup(name='warmuppy',
                 version='0.4',
                 description="A vocal warmup helper",
                 author="Alessandro Grassi",
                 author_email="alessandro@aggro.it",
                 url="https://github.com/xstasi/warmuppy",
                 package_dir={
                     '': 'src'
                 },
                 package_data={
                     '': ['*', 'ui/*', 'ui/dialogs/*', 'resources/*']
                 },
                 entry_points={
                     'gui_scripts': ['warmuppy = warmuppy.main:main']
                 },
                 cmdclass={'build': MyBuilder},
                 packages=['warmuppy'],
                 )
