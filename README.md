# Behavioral Data Processing Tools
Scripts to organize acknowledge and Matlab log files

### These scripts are provided as-is and nothing is guaranteed. A basic knowledge of python is assumed for editing the files

# Behavioral Data Organization Scripts

These scripts are intended to:
1. convert BIOPAC acquisition (.acq) files to a more universal csv format
2. Move/store matlab log.txt files in their corresponding participant folders (NOT BIDS FORMAT)

## Limitations

The scripts only have a couple of things to consider:
1. the acq conversion mimics the folder organisation that it converts from. CSV files will be stored in a separate but similar folder system next to the acq folders.
2. the Matlab move script assumes a filesystem similar to this:
* {participant number}/
  * bh/
    * {participant number}_A/
      * *log.txt
    * {participant number}_B/
      * *log.txt
With basic knowledge of python it can be easily modified however

### Prerequisites

The scripts are written to be run in Python 2.7.x
The modules used are included by default on many systems, but if errors are raised just install the needed modules

## Authors

* **Zachary Traylor** - *CNAPS Lab, LSU* - [CNAPS LSU](https://github.com/cnapslab)

