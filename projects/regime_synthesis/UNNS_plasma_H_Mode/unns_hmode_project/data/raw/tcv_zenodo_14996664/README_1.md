# Environment Setup Guide

This guide explains how to create a self-contained Python virtual environment, install the necessary libraries (including `ipykernel`), and register the kernel so you can run Jupyter notebooks with a consistent environment.

## Prerequisites

- **Python 3:** Make sure Python 3 is installed on your system.
- **pip:** Ensure that pip is installed and up-to-date.

## Step 1: Create a Virtual Environment

Open your terminal and run the following command to create a virtual environment. Replace `LHenv` with your desired environment name:

```bash
python3 -m venv LHenv
```

## Step 2: Activate the Virtual Environment

Open your terminal and run the following command to create a virtual environment `LHenv`

* on MacOS-Linux
```bash
source LHenv/bin/activate
```
* on Windows
```bash
LHenv\Scripts\activate
```

## Step 3: Install the required libraries

```bash
pip install -r requirements.txt
```
