# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:24:58 2015

@author: dimitris
"""

import re

s = "Indicated Power [kW]"
s[s.find("[")+1:s.find("]")]
m = re.search(r"\[([A-Za-z0-9_]+)\]", s)
if m:
    found = m.group(1)
    
found