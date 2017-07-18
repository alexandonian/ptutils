#!/usr/bin/env sh
sudo apt-get update
# We do this conditionally because it saves us some downloading if the
# version is the same.
if [[ "$TRAVIS_PYTHON_VERSION" == "2.7" ]]; then
    wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh;
else
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
fi
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update conda
# Useful for debugging any issues with conda
conda info -a

# Replace dep1 dep2 ... with your dependencies
conda create -y -n test-environment python=$TRAVIS_PYTHON_VERSION pip pytorch torchvision cuda80 -c soumith
source activate test-environment
python setup.py install
pip install -r requirements.txt