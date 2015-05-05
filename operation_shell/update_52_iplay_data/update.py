#!/usr/bin/python
        
import os
process_shell = "sh /home/mgmt/update_52_iplay_data/update_52_data.sh"
result = os.popen(process_shell).readlines()
result = filter(lambda ch: ch in '0123456789', result[-1].strip())
print result
