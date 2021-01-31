# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

import os
import re
import time
import pytz
import json
import uuid
import math
import base64
import sqlite3
import pymysql
import datetime
import itertools
import dateutil.rrule
import dateutil.relativedelta

from enum import Enum
from copy import deepcopy
from sodapy import Socrata
from dateutil import parser
from functools import partial
from dotenv import load_dotenv
from operator import itemgetter
from itertools  import groupby, chain
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from pydantic import BaseModel, Field
from fastapi import FastAPI, status, Body
from fastapi import Depends, Path, Query, APIRouter
from fastapi import Response, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request

# Environment variables
if os.path.exists(".env.development"):
    load_dotenv(dotenv_path='.env.development')
