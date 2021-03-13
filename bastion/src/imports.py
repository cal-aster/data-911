# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

import os
import jwt
import json
import yaml
import boto3
import shutil
import sqlite3
import pymysql
import requests

from stat import *
from pathlib import Path
from copy import deepcopy
from hashlib import sha256
from dotenv import load_dotenv
from datetime import datetime, timedelta

from typing import List, Dict, Union
from pydantic import BaseModel, Field
from starlette.requests import Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, Body, HTTPException
from fastapi import Depends, Path, Query, File, UploadFile

from werkzeug.security import safe_str_cmp
from werkzeug.utils import secure_filename

# Environment variables
if os.path.exists(".env.development"):
    load_dotenv(dotenv_path='.env.development')