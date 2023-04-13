# Temporary repository for the 2023 retreat


As said in the title, this will be removed soon.
If you want to keep some of the examples here, please make sure to save it.


## Environments

We plan to have the examples run on Linux - this can be pure Linux or WSL (Windows Subsystem for Linux).

The file `environment.yml` contains the environment we will use for the examples.

To create the environment, run on the Linux/WSL command line:

    conda env create -f environment.yml

The environment will be called `multiretreat`.
To activate it, run:

    conda activate multiretreat

This can take a while, as it will install all the packages.

If you have mamba installed, you can also run:

    mamba env create -f environment.yml

### Optional

There is also an environment for running on Windows, which is called `environment_win.yml`.
To create the environment, run on the Windows command line:

    conda env create -f environment_win.yml

This can take a while, as it will install all the packages.


## Scripts

TODO: explain
