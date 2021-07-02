#!/usr/bin/env python3

import sys
import json
from urllib.request import urlopen
import pandas as pd
from pathlib import Path

def first_val(v):
    try:
        return list(v.values())[0]
    except Exception as e:
        return v[0]

urlOrFile = sys.argv[1]

jsdata = ''
if Path(urlOrFile).exists():
    with Path(urlOrFile).open() as f:
        jsdata = f.read()
else:
    jsdata = urlopen(urlOrFile).read()

data = json.loads(jsdata)
data = [{k : first_val(v) for k, v in item.items()} for item in data]
df = pd.DataFrame(data)
print(df.to_csv(index=False))
