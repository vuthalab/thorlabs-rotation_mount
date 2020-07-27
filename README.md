# Python code to control ELL14K rotation mount
Author: Sarina Xi

This Python code is written to control the [ELL14K rotation mount](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12829).  

All the constants and commands are gotten from the communication manual available on the Thorlabs website for this product. 
Refer to that if you would like to add functions and modify commands. 

Note: Put a sufficient time delay between commands that you send. If you don’t do so, then the machine might skip over commands and actions. 
Furthermore, if you are doing a series of commands in a short amount time, errors in the position of the rotation mount can accumulate. 
