# CrimeCurbingSystem
## Capstone project

**These instructions are generic. They are a guide to installing the necessary
software to continue working on this project, or run the project as is.**

----------
### QuickStart
----------

1. Download the latest release https://github.com/emmagperez/CrimeCurbingSystem/
2. Download python 2.7.x, https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi
   
#### Windows Only
3. Download python 3.5.x, or greater https://www.python.org/ftp/python/3.6.3/python-3.6.3.exe
- This is due to TensorFlow requiring 3.5.x, or greater, to be installed on Windows.
  - Skip to, **Windows Python/TensorFlow-GPU Installation**
4. Open a command prompt and run the following commands to install required python modules
#### If you want to use your GPU instead of CPU to train your neural network, skip the tensorflow command below. 
###### See Requirements to use TensorFlow-GPU below.
```pip install numpy
pip install imutils
pip install pillow
pip install opencv-python
pip install tensorflow
pip install keras
```
----------
#### TensorFlow for Windows/TensorFlow-GPU Installation
----------
1. Open a command prompt and run the following commands to install required python modules for Windows
#### If you want to use your GPU instead of CPU to train your neural network, skip the tensorflow command below.
###### See Requirements to use TensorFlow-GPU below.
```pip3 install numpy
pip3 install imutils
pip3 install pillow
pip3 install opencv-python
pip3 install tensorflow
pip3 install keras
```
##### Requirements to use TensorFlow-GPU
- NVidia GPU, compatibility can be verified here, https://developer.nvidia.com/cuda-gpus
- CUDA Toolkit 8.0, download link, https://developer.nvidia.com/cuda-downloads
- VisualStudio, this can be obtained from [UTC's OnTheHub site](https://e5.onthehub.com/WebStore/Security/Signin.aspx?ws=a0de2013-c39b-e011-969d-0030487d8897&vsro=8&rurl=%2fWebStore%2fProductsByMajorVersionList.aspx%3fws%3da0de2013-c39b-e011-969d-0030487d8897%26vsro%3d8)
  - You can also acquire additional software from this site. **UTC Students Only**
1. Follow the instructions [here](https://www.tensorflow.org/install/), for your OS.
