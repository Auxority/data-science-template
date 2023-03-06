import subprocess
import sys

def install_dependencies():
    print('Installing pip dependencies...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'chardet', 'pandas', 'numpy', 'matplotlib', '--quiet'])
    print('Finished installing pip dependencies...')

def read_csv(file_name: str, file_encoding: str = None):
    import chardet
    import pandas as pd

    path = f'../data/{file_name}'

    with open(path, 'rb') as f:
        data = f.read(1000)

    if (not file_encoding):
        print('Detecting encoding...')
        result = chardet.detect(data)
        file_encoding = result['encoding']
        print(f'Found encoding: {file_encoding} ({result["confidence"] * 100:.2f}% certainty)')

    return pd.read_csv(path, encoding=file_encoding)