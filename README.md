# swiftnav-multi
This repository includes Python and C code for reading multiple messages from Swift-Nav Piksi Multi. All the codes are tested in Linux environments and instructions are for Linux only.

## Setting-up Piski
For debugging purposes, Piksi can be configured to work in simulation mode so that you do not have to go outside with a GPS antenna for testing your codes.

With Piksi Multi connected to your computer and Swift Console running:
* Click the *Settings* tab
* In the *Simulator* section, you will see a value for *enabled*. Click on this.
* Set the value of *enabled* to *True* by selecting True from the drop-down menu right part of the tab.
* Then click *Save to Flash*

The official documentation can be found [here](https://support.swiftnav.com/customer/en/portal/articles/2757369-piksi-multi---using-simulation-mode).

## Modifying the code
This code only processes LLH position, velocity, baseline solution, and UTC. For other messages, refer the [SPB Manual](https://support.swiftnav.com/customer/en/portal/articles/2492810-swift-binary-protocol) for additional messages. For finding the elements in a message, check relevant h file in c/include/libsbp of [sbp library](https://github.com/swift-nav/libsbp.git). For example, *SBP_MSG_POS_LLH* is in *navigation.h*.

## Python Code
SBP library has issues with working with Python 3 as of writing of this code. So it is necessary to use Python 2. Below instructions assume that [conda](https://www.anaconda.com/download/) has already been installed.

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

## C-Code
### Dependencies
Piksi sends messages using a custom protocol called Swaiftnav Binary Protocol (SBP). Running this C-code needs the installation of few dependencies.
* sbp-lip : for parsing the SBP messages
* lib-serial : for communicating with Piksi through the serial port

#### SBP Library - [sbp-lib](https://github.com/swift-nav/libsbp.git)
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

#### Serial Port Library - [lib-serial](https://sigrok.org/wiki/Libserialport)
1. Clone the [repo](git://sigrok.org/libserialport)
    ```
    git clone git://sigrok.org/libserialport
    ```
2. Install required packages
    ```
    sudo apt-get -y install autoconf
    sudo apt-get -y install libtool
    ```
3. Build the library
    ```
    cd libserialport
    ./autogen.sh
    ./configure
    make
    sudo make install
    ```

#### On 64-bit Systems
On 64-bit systems, you might need to install below packages.
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

2. Running (see Troubleshooting below for issues)
    ```
    ./read_rtk -p /dev/ttyUSB0
    ```

### Troubleshooting
1.  Error: "libserialport.so.0: cannot open shared object" - solution: configure dynamic linker run-time bindings
    ```
    sudo ldconfig /usr/local/lib
    ```
2. Cannot open the serial port (replace /path/to/ports with your actual port, eg:  sudo chmod 777 /dev/ttyUSB0)
    ```
    sudo chmod 777 /path/to/port
    ```
