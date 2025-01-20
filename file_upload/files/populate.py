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
    user1 = User.objects.create_user(username="detective1", password="password1")
    user2 = User.objects.create_user(username="detective2", password="password2")

    # create cases
    # case 1, no referenced cases
    case1 = Case.objects.create(
        type_of_crime = "assault",
        date_opened = datetime(2025, 1, 20), # yy
        last_updated = datetime(2025, 1, 20, 12, 42),
        location = "Town",
        created_by = user1,
        assigned_users = [user1, user2],
        reviewers = [user1]
        )
    # case 2, references case 1
    case2 = Case.objects.create(
        type_of_crime = "theft",
        date_opened = datetime(2025, 1, 19), # yy
        last_updated = datetime(2025, 1, 20, 10, 56),
        location = "Town",
        created_by = user1,
        assigned_users = [user1, user2],
        reviewers = [user1],
        references = case1
        )
    # create files not linked to cases

    # run analysis on files 
    # link files to cases
    # add changelog entries to files
    # add changelog entries to cases
    # add user access records

if __name__  == "__main__":
    print("populating Files database")
    try:
        populate()
    except:
        print("error in populating database!")
    else:
        print("Database populated successfully!")