import os
import django
from datetime import datetime, timedelta

# django config setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# population script
from files.models import *

def populate():
    # create users first
    # create cases
    # create files not linked to cases
    # run analysis on files 
    # link files to cases
    # add changelog entries to files
    # add changelog entries to cases
    # add user access records