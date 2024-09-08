# Banke-RS - Tool for Analyzing the Banking Market

A tool for analyzing the banking market and the performance of individual banks, developed as part of the Computational Finance seminar at Petnica Science Center in 2024.

People involved: [Jovan Ivković](https://github.com/jovanivko), Đorđe Simić, [Marko Milenković](https://github.com/MarkoMile), and mentor Jasna Atanasijević.

* See [Usage](#usage) for instructions on how to use this repository.
* See [Example](#example) for a demonstration of the program.

# Capabilities

The program gathers data from the NBS (National Bank of Serbia) website on the balance sheets and income statements of individual banks for the years 2022 and 2023. This data is analyzed, processed, and visualized within the program. Banks are clustered using the k-means and PCA methods.

Data shown for the entire market:
* TOTAL ASSETS 2023, ASSET GROWTH, TOTAL DEPOSITS 2023, DEPOSIT GROWTH, TOTAL LOANS 2023, LOAN GROWTH

Data shown for individual banks:
* RANK BY ASSETS, TOTAL ASSETS, NET INTEREST MARGIN, RETURN ON EQUITY, LIQUIDITY RATIO, IMPAIRMENT RATE

# Example

<p align="center">
<img src="media/banke-rs-example-hq.gif" alt="banke-rs-example">
</p>

# Usage

### Prerequisites
Before running the program, make sure you have the following:

* Python 3.x
* Install the required packages from `requirements.txt`

To install the packages, run the following command:  
```pip install -r requirements.txt```

### Running the Program
After installing the packages, you can run the program with the following command:  
```python ./gui.py```.

Note: The first time you run the program, it may take some time to download and process the data.
