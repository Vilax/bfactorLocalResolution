# bfactorLocalResolution

This repository contains the program to carry out the matching between local resolution (from any method) and bfactor (from a pdb of x rays or cryoem).

# Installation

The installation of bfactorLocalResolution is quite simple:

1) Download this repository. Open a terminal and launch

```
git clone https://github.com/Vilax/bfactorLocalResolution.git
```

2) Open de folder bfactorLocalResolution and execute the file install.sh. This file will download xmipp and will install it for you, as well as, it will create a virtual enviroment with all required dependencies to run bfactorLocalResolution

```
cd bfactorLocalResolution
. install.sh
```

# Execution/use

To launch the program it only requires to active the virtual enviroment. You can do that as it follows


```
source env/bin/activate
```

Now, to launch the program

```
python bfactor.py
```



# Troubleshooting

If the error comes from the compilation of xmipp, perhaps one of the next libraries is needed. At least in ubuntu:

```
sudo apt-get install gcc-5 g++-5 cmake openjdk-8-jdk libxft-dev libssl-dev libxext-dev libxml2-dev\
 libreadline6 libquadmath0 libxslt1-dev libopenmpi-dev openmpi-bin  libxss-dev libgsl0-dev libx11-dev\
 gfortran libfreetype6-dev scons libfftw3-dev libopencv-dev curl git
```

If you work in OpenSuse, perharps you need to substitute the command export by setenv in the file (xmipp/build/xmipp.bashrc). Fill the following paths with the paths contained in the xmipp.bashrc 

```
setenv XMIPP_HOME path_to_xmipp_home
setenv XMIPP_SRC path_to_xmipp_src
setenv PATH path
setenv PYTHON_PATH path_to_python
```



