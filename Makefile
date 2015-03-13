#
# this is a simple and Makefile, for PodCastXDL
# Just to install it to /usr/local/bin/
# 
# Writen by: levi0x0 (Fri Mar 6 22:02:51 2015)
#  

FIX=/usr/local/bin/

install:
	@echo "[+] Installing PodCastXDL.."
	install -Dm775 ./bin/PodCastXDL.py  ${FIX}podcastXDL


uninstall:
	@echo "[+] Removing PodCastXDL.."
	rm -f /usr/local/bin/podcastXDL
