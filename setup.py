from cx_Freeze import setup, Executable

base = 'Win32GUI'

executables = [
    Executable("gui.py", base=base)
]

setup(
    name="Organizador de Arquivos",
    version="1.0",
    description="Organiza os arquivos em pastas, dependendo de suas extensões.",
    executables=executables,
)
