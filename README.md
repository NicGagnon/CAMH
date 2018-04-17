# CAMH
Research Informatics 

XNAT FTP Integration – The XNAT system can be enabled to communicate with an established MRFTP to allow for automated upload of data. This completes chain from scanner data acquisition to secure database. 
  - set_up.sh - Shell script to set up environment for following 3 scripts
  - dm_sftp.py - Connects with FTP server and pulls fMRI data from subject provided
  - dm_link.py - Creates symbolic links with projects pulled from FTP server and creates hospital naming convention
  - dm_xnat_upload.py - Uploads fMRI data to XNAT 
  
XNAT2BIDS - Develop pipeline to convert dicom files from XNAT to Brain Imaging Data Structure 
  - dicom_pull.py - Pulls target label from dicom header and stores list
  - json_builder.py - Reads through aforemention list and builds json configuration file 
  
