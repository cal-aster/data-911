# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

import re
import csv
import json
import yaml
import uuid
import requests

from math import isnan
from sodapy import Socrata
from dateutil import parser
from datetime import datetime
from urllib.request import urlretrieve