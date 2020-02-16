import os
import pathlib

dirname = os.path.dirname(__file__)

def create_folders():
    # create folder if not exists
    if not os.path.exists(os.path.join(dirname, 'dist/by_tester')):
        pathlib.Path(os.path.join(dirname, 'dist/by_tester')).mkdir(parents = True, exist_ok = True) 
    
    if not os.path.exists(os.path.join(dirname, 'dist/by_alphabet')):
        pathlib.Path(os.path.join(dirname, 'dist/by_alphabet')).mkdir(parents = True, exist_ok = True) 
    
    if not os.path.exists(os.path.join(dirname, 'dist/by_alphabet_describe')):
        pathlib.Path(os.path.join(dirname, 'dist/by_alphabet_describe')).mkdir(parents = True, exist_ok = True) 