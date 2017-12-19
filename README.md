# swiftnav-multi

## Setting-up Piski
* To set the Piksi in simulation mode: [link](https://support.swiftnav.com/customer/en/portal/articles/2757369-piksi-multi---using-simulation-mode)

## C
### Installing sbp-lib
1. Clone the official [sbp library](https://github.com/swift-nav/libsbp.git)
    ```
    git clone https://github.com/swift-nav/libsbp.git
    ```
2. Install dependencies
    ```
    sudo apt-get -y install build-essential pkg-config cmake doxygen check
    ```
3. Create a build directory
    ```
    cd libsbp/c
    mkdir build
    cd build
    ```
4. Build and install
    ```
    cmake ../
    make
    sudo make install
    ```

### Dependencies
#### Serial Port Library - [lib-serial](https://sigrok.org/wiki/Libserialport)
1. Clone the [repo](git://sigrok.org/libserialport)
    ```
    git clone git://sigrok.org/libserialport
    ```
2. Install required packages
    ```
    sudo apt-get -y install autoconf
    sudo apt-get -y install libtool
3. Build the library
    ```
    cd libserialport
    ./autogen.sh
    ./configure
    make
    sudo make install
    ```

#### On 64-bit Systems

  ```
  sudo apt-get -y install libgtk2.0-0:i386 libidn11:i386 libglu1-mesa:i386
  sudo apt-get -y install libpangox-1.0-0:i386 libpangoxft-1.0-0:i386
  ```

### Running the code
1. Compiling
    ```
    mkdir build
    cd build
    cmake ../
    make
    ```

2. Running
    ```
    ./read_rtk -p /dev/ttyUSB0
    ```

## Python
### Environment setup
1. Install Anaconda
2. Create and source the environment. If the environment is already created, just source it.
    ```
    conda create -n fly_out python=2
    source activate fly_out
    ```
3. Install required libraries
    ```
    pip install sbp
    ```

### Running the Code
Simply run the py file: (default port = \dev\ttyUSB0, default baud rate = 115200)
```
python read_sbp.py
```

For different ports or baud rates:
```
python read_sbp.py -p /path/to/port -b baud_rate
```
