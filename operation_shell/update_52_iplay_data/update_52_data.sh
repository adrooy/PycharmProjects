#!/bin/bash

TIME=$(date +%Y-%m-%d_%H:%M:%S)
DATE=$(date +%Y-%m-%d)

echo $TIME', start update data in 52'
ssh mgmt@116.255.129.52 "cd /home/mgmt/update_52_iplay_data; python update_52_iplay_data.py $DATE"

#ssh mgmt@116.255.129.52 "cd /home/mgmt/update_52_iplay_data.bak; python test.py"
