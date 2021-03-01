#!/bin/bash
filename='premium_accounts.csv'
#while read line
while IFS="," read -r username junk
do
#    echo "Record is : $line"
    text=$(lastlog -u $username 2> /dev/null | sed -n '2p')
    if [[ $text =~ .*Never.* ]]; then  # user who never logged in
        msg="Never logged in"
    elif [ -z "$text" ]; then  # unknown user
        msg="-"
    else
        set -- junk $text      # last login on record
        shift
        msg="$5 $9"            # ouput month and year of last login
    fi

    echo "$username,$msg"
done < <(tail -n +2 $filename)  # skip header line

