# swiftnav-multi

## Setting-up Piski
* To set the Piksi in simulation mode: [link](https://support.swiftnav.com/customer/en/portal/articles/2757369-piksi-multi---using-simulation-mode)

## Python
### Environment setup
1. Install Anaconda
2. Create and source the environment. If the environment is already created, just source it.
    ```sh
    conda create -n fly_out python=2
    source activate fly_out
    ```
3. Install required libraries
    ```sh
    pip install sbp
    ```

### Running the Code
Simply run the py file: (default port = \dev\ttyUSB0, default baud rate = 115200)
```sh
python read_sbp.py
```

For different ports of baud rates:
```sh
python read_sbp.py -p /path/to/port -b baud_rate
```
