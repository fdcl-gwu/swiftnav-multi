# swiftnav-multi
This repository includes Python and C code for reading multiple messages from Swift-Nav Piksi Multi. All the codes are tested in Linux environments and instructions are for Linux only.

The provided codes can perform following tasks
* read multiple messages from the Multi ([C](#c-code)/[Python](#python-code))
* read and write settings without the console ([Python](#changing-the-settings-without-the-console))

## Setting-up Multi
For debugging purposes, Multi can be configured to work in simulation mode so that you do not have to go outside with a GPS antenna for testing your codes.

With Multi connected to your computer and Swift Console running:
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
Install required libraries
    ```
    pip install sbp
    ```

### Running the Code
Simply run the py file (default port = \dev\ttyUSB0, default baud rate = 115200). For issues, see troubleshooting.
```
python2 read_sbp.py
```

For different ports or baud rates:
```
python read_sbp.py -p /path/to/port -b baud_rate
```

### Changing the Settings without the Console
1. To rest:
  ```
  python2 reset_multi.py -p /path/to/port -b baud_rate
  ```
2. To write settings to Multi from an ini file
  ```
  python2 write_from_ini_file.py -f /path/to/ini/file
  ```
  There are few ini files saved in settings_files directory. These files are
  first saved through the SwiftNav Console. Usually those files are tied to
  serial number of the GPS. So you need different files for different GPS units.
3. Running the code through bash files
  There are few bash files added so that you do not need to manually type all
  the arguments.
  ```
  sudo chmod +x name/of/the/bashfile
  ./name/of/the/bashfile
  ```


## C-Code
### Dependencies
Multi sends messages using a custom protocol called Swaiftnav Binary Protocol (SBP). Running this C-code needs the installation of few dependencies.
* sbp-lib : for parsing the SBP messages
* lib-serial : for communicating with Multi through the serial port

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
3. Error: AttributeError: 'module' object has no attribute 'Struct' - solution
   python SBP libraries need specific versions of "construct" and "requests-futures" libraries.
    ```
    sudo pip install construct==2.9.33
    sudo pip install requests-futures==0.9.5
    ```
