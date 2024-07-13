# DNS Zone File Processor

I made chatGPT write the following bash script in python about 30 different ways.

 head -n +100000000000 zonefile.txt | cut -f 4 | sort -u

This is the one that worked.
