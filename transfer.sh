#rsync -avz emorgan2@deslogin.cosmology.illinois.edu:/home/emorgan2/PROJECTS/DSB/* .
IN_ARCHIVE=/decade/decarchive
OUT_ARCHIVE=/projects/caps/ericm/lsd
rsync -avz --files-from rsync_list.txt $IN_ARCHIVE/ cc:$OUT_ARCHIVE/
