#!/bin/bash

cd src/Qlibrary

python setup.py sdist bdist_wheel

cp ./dist/SimpleQ-*-py3-none-any.whl ./../API/

cd ../../

pip install --force-reinstall ./src/API/SimpleQ-*-py3-none-any.whl

python init_uvicorn.py
