import group
import pwd
import subprocess
import pandas as pd

# DEFINE FUNCTIONS
def get_members(account_type):
    """ 
    Returns a list of the usernames for all users with the
    given Linux group membership.
    """
    username=[]
    for groupname in account_type
        group=grp.getgrnam(groupname)
        username.extend(group.gr_mem)
    return username 

################
# MAIN PROGRAM
################
# declarations
users_priority=[]

# constants
# oscar group names for premium account types
# priority accounts
priority=['priority','priority1','priority2','priority3','priority4',
          'priority5','priority6','priority7','priority8','priority9']
priorityp=['priority+','priority+1']
# premium GPU accounts
prigpu=['pri-gpu','pri-gpu1']
prigpup=['pri-gpu+','pri-gpu+1']
gpuhe=['gpu-he','gpu-he1']
# bigmem accounts
pribigmem=['pri-bigmem','pri-bigmem1']

# determine users belonging to each premium account groups
print(priority)
#users_priority=get_members(priority)

# create single list of all users and account types


# for each user with a premium account, determine
# name

# email address

# primary group affiliation

# write out dtaa as a csv file
print(users_priority)

