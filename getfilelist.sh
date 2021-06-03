setup finalcut Y5A1+3
python getfilelist.py  
cat file_list.txt | awk '{ printf("%s\n%s\n%s\n", $8, $9, $10) }' > rsync_list.txt 
