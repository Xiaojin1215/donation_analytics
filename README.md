# Donation Analytics

## Introduction
This challenge was implemented by Python. All of the functions were included in 
`donation-analytics.py`
## Algorithms

For the data structure, I mainly chose two dictionaries:

1. Donor information:
    * Key: donor_id, which is "NAME, ZIP_CODE". 
    * Value: the minimum donation year so far of this donor 
2. Recipient information:
    * Key: recipient_id, which is "CMTE_ID, ZIP_CODE, YEAR"
    * Value: List of donation amount of this recipient_id

We read data from the input file line by line, and kept updating these two dictionaries to decide if current line was from a repeat donor. If so, then generate one line of output to output file. If not, then continue to process other data.

## Directory structure 

The directory structure looks like this:

     ├── README.md
     ├── run.sh
     ├── src
     │   └── donation-analytics.py
     ├── input
     │   └── percentile.txt
     │   └── itcont.txt
     ├── output
     |   └── repeat_donors.txt
     ├── insight_testsuite
         └── run_tests.sh
         └── tests
             └── test_1
             |   ├── input
             |   │   └── percentile.txt
             |   │   └── itcont.txt
             |   |__ output
             |   │   └── repeat_donors.txt
             ├── my_test
                 ├── input
                 │   └── percentile.txt
                 │   └── itcont.txt
                 |── output
                     └── repeat_donors.txt
The foler `input` is used to save all input files, `output` is used to save output files. Python script is saved in `src` folder. `insight_testsuite` is used for test.        
## How to run

For the python script, you can use the following line to run: `python ./src/donation_analytics.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt`

Or you can just use `./run.sh` to run

##Author
This code challenge was made by Xiaojin Liu. If you have any questions, please feel free ton contact me through email: <xiaojinliumail@gmail.com>

