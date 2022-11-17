import os
dirs = ['imgs','imgs2','imgsr','wavs','wavr','framesr','imgsr2']
for i in dirs:
	os.system(f"rm {i}/*")
