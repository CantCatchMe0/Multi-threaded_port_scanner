# Multi-threaded_port_scanner (Python)
This is a python based multi-thread TCP port scanner. it is mean to scan for open ports of a target host, and try to get the banner.

# Features
Using ThreadPoolExecutor to increase the scanning speed.
Support url and ip as input of target
Will try to read the Banner information return by the port
Use colorama to highlight the open ports

# Installation and Dependencies
Make sure you installed Python 3.x

```bash
git clone [https://github.com/CantCatchMe0/PyPortScanner.git](https://github.com/CantCatchMe0/PyPortScanner.git)
cd PyPortScanner
pip install -r requirements.txt
