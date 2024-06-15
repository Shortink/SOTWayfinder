echo off
title Update Ip list
pip install -r requirements.txt
cls
python retrieve_iprange.py
pause