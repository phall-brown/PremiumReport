import grp
import pwd
import subprocess
import pandas as pd

# DEFINE FUNCTIONS
def get_members(group_list):
    """ 
    Returns a list of the usernames for all users with the
    given Linux group membership.
    """
    username=[]
    for groupname in group_list:
        try: 
            group=grp.getgrnam(groupname)
            username.extend(group.gr_mem)
        except:
            pass
 
    return username 

def get_account_types(username):
    """
    Returns a list of current account types associated with the specified user.
    """
    accounts=[]
    # Define premium account types (based on Linux groups)
    # Priority accounts
    priority=['priority','priority1','priority2','priority3','priority4',
             'priority5','priority6','priority7','priority8','priority9']
    priorityp=['priority+','priority+1']
    # Premium GPU accounts
    prigpu=['pri-gpu','pri-gpu1']
    prigpup=['pri-gpu+','pri-gpu+1']
    gpuhe=['gpu-he','gpu-he1']
    # Bigmem accounts
    pribigmem=['pri-bigmem','pri-bigmem1']
 
    # Get list of all groups to which user belongs
    proc=subprocess.Popen(['id','-Gn',username],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           encoding='utf-8')
    out,err=proc.communicate()
    groups=list(out.strip('\n').split(" ")) 
    
    # Determine if user belongs to any groups associated with premium accounts 
    for group in priority:
      if group in groups:
        accounts.append('priority')
    for group in priorityp:
      if group in groups:
        accounts.append('priority+')
    for group in prigpu:
      if group in groups:
        accounts.append('pri-gpu')
    for group in prigpup:
      if group in groups:
        accounts.append('pri-gpu+')
    for group in gpuhe:
      if group in groups:
        accounts.append('gpu-he')

    # Add indicator to handle users with no premium account(s)
    if not accounts:
      accounts.append('-')

    return accounts

def get_user_name(username):
    """
    Returns user's name
    """
    tmp=[]

    try:
      tmp=pwd.getpwnam(username)
      try:
        output=tmp.pw_gecos.split(',')[0]
      except:
        output='NA'
    except:
      output='NA'

    return output

def get_user_email(username):
    """ 
    Returns user's email address
    """
    tmp=[]

    try:
      tmp=pwd.getpwnam(username)
      try:
        output=tmp.pw_gecos.split(',')[4]
      except:
        output='NA'
    except:
      output='NA'

    return output

def get_group(username):
    """ 
    Returns user's name
    """
    tmp=[]

    try:
      tmp=pwd.getpwnam(username)
      try:
        gid=tmp.pw_gid
        tmp=grp.getgrgid(gid)
        output=tmp.gr_name
      except:
        output='NA'
    except:
      output='NA'

    return output

##############
# MAIN PROGRAM
##############

# declarations
username=[]
name={}
email={}
accounts={}
primary={}

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

# determine users with premium accounts
username.extend(get_members(priority))
username.extend(get_members(priorityp))
username.extend(get_members(prigpu))
username.extend(get_members(prigpup))
username.extend(get_members(gpuhe))
username=list(set(username))                  # eliminate duplicates
username.sort()                               # sort alphabetically

# for each user, determine name, email address, premium account type
for user in username:
    name[user]=get_user_name(user)
    email[user]=get_user_email(user)
    accounts[user]=get_account_types(user)
    primary[user]=get_group(user)
 
# write out dtaa as a csv file
print(username)
print(name)
print(email)
print(accounts)
print(primary)

