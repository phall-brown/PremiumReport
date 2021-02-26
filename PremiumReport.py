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

def get_premium(username,groupnames):
    account=[]
# Get list of all groups to which user belongs
    proc=subprocess.Popen(['id','-Gn',username],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           encoding='utf-8')
    out,err=proc.communicate()
    groups=list(out.strip('\n').split(" ")) 
    for group in groupnames:
        if group in groups:
            account.append('Y')
    if not account:
        account.append('-')

    return account

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
    for group in gpuhe:
      if group in groups:
        accounts.append('pri-bigmem')

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

def get_lastlogin(username):
    """
    Returns month and year of last login
    """
# Get list of all groups to which user belongs
    proc=subprocess.Popen(['lastlog','-u',username],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           encoding='utf-8')
    out,err=proc.communicate()
#    groups=list(out.strip('\n').split(" ")) 
#    for group in groupnames:
#        if group in groups:
#            account.append('Y')
#    if not account:
#        account.append('-')

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
account_priority={}
account_priorityp={}
account_prigpu={}
account_prigpup={}
account_gpuhe={}
account_pribigmem={}

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
# Bigmem accounts
pribigmem=['pri-bigmem','pri-bigmem1']

# determine users with premium accounts
username.extend(get_members(priority))
username.extend(get_members(priorityp))
username.extend(get_members(prigpu))
username.extend(get_members(prigpup))
username.extend(get_members(gpuhe))
username.extend(get_members(pribigmem))
username=list(set(username))                  # eliminate duplicates
username.sort()                               # sort alphabetically

# for each user, determine name, email address, premium account type
for user in username:
    name[user]=get_user_name(user)
    email[user]=get_user_email(user)
    accounts[user]=get_account_types(user)
    primary[user]=get_group(user)
    account_priority[user]=get_premium(user,priority)
    account_priorityp[user]=get_premium(user,priorityp)
    account_prigpu[user]=get_premium(user,prigpu)
    account_prigpup[user]=get_premium(user,prigpup)
    account_gpuhe[user]=get_premium(user,gpuhe)
    account_pribigmem[user]=get_premium(user,pribigmem)

# convert dicts to pandas dataframes 
name_df=pd.DataFrame.from_dict(name,orient='index',columns=['Name'])
email_df=pd.DataFrame.from_dict(email,orient='index',columns=['Email'])
primary_df=pd.DataFrame.from_dict(primary,orient='index',columns=['Group'])
account_priority_df=pd.DataFrame.from_dict(account_priority,orient='index',columns=['priority'])
account_priorityp_df=pd.DataFrame.from_dict(account_priorityp,orient='index',columns=['priority+'])
account_prigpu_df=pd.DataFrame.from_dict(account_prigpu,orient='index',columns=['pri-gpu'])
account_prigpup_df=pd.DataFrame.from_dict(account_prigpup,orient='index',columns=['pri-gpu+'])
account_gpuhe_df=pd.DataFrame.from_dict(account_gpuhe,orient='index',columns=['gpu-he'])
account_pribigmem_df=pd.DataFrame.from_dict(account_pribigmem,orient='index',columns=['pri-bigmem'])

# combine dataframes into a single dataframe
data=pd.concat([name_df,email_df,primary_df,account_priority_df,account_priorityp_df,
               account_prigpu_df,account_prigpup_df,account_gpuhe_df,account_pribigmem_df],
               axis=1,ignore_index=False) 
 
# write out data as a csv file
#print(accounts)
#print(data)

data.to_csv('premium_accounts.csv')
