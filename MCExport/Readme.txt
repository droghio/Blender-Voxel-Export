Notes:
    You will need blender 2.68 or newer to use this script, this also means
    all dependancy must be installed with python3 tools.

    I built this using Blender 2.69 which uses python3.3.
    This guide will assume this configuration keep in mind these commands will vary slightly
    for different versions of blender.

Install instructions:
    I've tried to package as much as possible into the addon itself, but you still need
    a few packages.

    Namely,    
        --numpy - version 1.8.0
        --pickle

    Both of these need to be installed to your python3.3 site packages.
    
    On Fedora this is done with the python3-pip tool.
    If you don't have this already grab it:
        sudo yum install python3-pip

    Then...
        python3-pip install numpy
