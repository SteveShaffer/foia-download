# FOIA Downloader

A simple Python script for batch-downloading files from a FOIA request.

## Why?

[FOIA Online](https://foiaonline.regulations.gov) streamlines the process of requesting documents available under the Freedom of Information Act.
But what if you submit a request that results in thousands of documents?
Going through that list 50 documents at a time and downloading 20MB at a time would be very tedious.

FOIA Downloader is a simple Python script that automates the process of looking up and downloading each of the records for a particular request

## Setup

You'll need to install the following to get this to work:

* [Python 2.7.x](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/latest/installing.html)
* Requests `pip install requests`
* Beautiful Soup `pip install beautifulsoup4`

## Use

You'll need to get the ID of the FOIA request you wish to download.
You'll find this ID at the end of the web address after the `?objectId=`.
Copy that ID.

To start the download, copy the `foia-download.py` file into the directory on your computer where you want the downloaded files saved.
Then open a command prompt (Start Menu > All Programs > Accessories > Command Prompt) and type the following:

    python /path/to/foia-download.py 0123456789

but replace the `0123456789` with the request ID you found in the URL and `/path/to/` with the path to the `foia-download.py` file.

There's no error handling to handle when there's a network disruption or something like that.
But it writes the file index to a file called `foia-index.txt`.
So if you know Python, you should be able to edit the script so that you don't have to re-index and re-download everything if there's a network disruption.
