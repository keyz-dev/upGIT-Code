import os, sys
from app import main

if hasattr(sys, 'real_prefix'):
    base_python_path = sys.real_prefix
else:
    base_python_path = sys.base_prefix

os.environ["TCL_LIBRARY"] = os.path.join(base_python_path, 'tcl', 'tcl8.6')
os.environ["TK_LIBRARY"] = os.path.join(base_python_path, 'tcl', 'tk8.6')

if __name__ == "__main__":
    main.main()
    
    