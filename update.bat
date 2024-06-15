echo off
title Update Ip list
pip install pydivert requests netaddr bs4
python retrieve_iprange.py
pause