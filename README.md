# PremiumReport

Identifes all users who currently have a premium account on Oscar, based on their group membership.

Note: the group names associated with each of the various premium accounts are hard-coded. This portion of the code should be checked before use to ensure that all active premium groups are included, since these can be added to the system without notice.

## Output
File is output as a plain text csv file with a header line (filename: premium_accounts.csv). Contents are as follows:

Column 1: Username  
Column 2: Name  
Column 3: Email address  
Column 4: User's Primary Group  
Column 5: priority account  
Column 6: priority+ account  
Column 7: pri-gpu account  
Column 8: pri-gpu+ account  
Column 9: pri-gpu++ account  
Column 10: gpu-he account  
Column 11: gpu-he+ account  
Column 12: pri-bigmem account  

For each premium account type, if the user has that account type (i.e., is a member of a corresponding group), a value of "1" is reported. If the user does no have that account type, a value of "0" is reported.

If a user is missing information in the directory (e.g., no email address on record on Oscar), a value of "NA" is returned for that field.

## Usage
Required python packages: pandas

python PremiumReports.py
