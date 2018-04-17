#
# This document aims to set up the environment in order to run dm_sftp, dm_link, and dm_xnat_upload
# Steps needed after running this script are to : Add the Program ID to the tigr_lab yml file and
# create a project on XNAT in order to provide an upload destination
# 
# Takes Program ID as argument
if [ -z "$1" ]
	then
		echo "Error. Please provide Program ID"
		exit 1
fi

PROGRAM_ID=$1
PROJECT_ARCHIVE=$PROGRAM_ID"_CMH"
PROGRAM_YAML=$PROGRAM_ID"_settings.yml"
PROJECT_DIR="/external/rprshnas01/nip/datman-projects"
CONFIG_DIR="/usr/local/bin/datman/config"

#This part will set up the .yml file for the project by setting the MRUSER, MRFOLDER, and Contact Name
echo "FTP to XNAT environment set up" 
read -p "MRUSER: `echo $'\n> '`" MRUSER
read -p "MRFOLDER: `echo $'\n> '`" MRFOLDER
read -p "PI NAME: `echo $'\n> '`" FULLNAME

while true; do
    read -p "Is the following information correct (y/n)? `echo $'\n> '` MRUSER = $MRUSER
    													 `echo $'\n> '` MYFOLDER = $MRFOLDER
    													 `echo $'\n> '` PI NAME = $FULLNAME 
    													 `echo $'\n> '`" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
# Copies the template settings file for the study
cp $CONFIG_DIR/template_settings.yml $CONFIG_DIR/$PROGRAM_YAML
sed -i "s/TEMP_PROJECTID/$PROGRAM_ID/g" $CONFIG_DIR/$PROGRAM_YAML
sed -i "s/TEMP_ARCHIVE/$PROJECT_ARCHIVE/g" $CONFIG_DIR/$PROGRAM_YAML
sed -i "s/TEMP_USER/$MRUSER/g" $CONFIG_DIR/$PROGRAM_YAML
sed -i "s/TEMP_FOLDER/$MRFOLDER/g" $CONFIG_DIR/$PROGRAM_YAML
sed -i "s/TEMP_CONTACT/$FULLNAME/g" $CONFIG_DIR/$PROGRAM_YAML
echo "Yaml file is set up!"

#This part will set up the external environment to save the dicoms and zips. Make sure to get the password for the mrftppass.txt from tigr_lab
if [ -d "$PROJECT_DIR/$PROGRAM_ID" ]; then
  exit
fi

mkdir $PROJECT_DIR/$PROGRAM_ID
mkdir -p $PROJECT_DIR/$PROGRAM_ID/data/dcm
mkdir $PROJECT_DIR/$PROGRAM_ID/data/dicom
mkdir $PROJECT_DIR/$PROGRAM_ID/data/zips
mkdir $PROJECT_DIR/$PROGRAM_ID/metadata
touch $PROJECT_DIR/$PROGRAM_ID/metadata/mrftppass.txt

while true; do 
	read -sp 'Password for project: ' PSSWRD
	read -p "Is this correct (y/n)? `echo $'\n> '` $PSSWRD
									`echo $'\n> '`" yn
	case $yn in 
		[Yy]* ) break;;
		[Nn]* ) continue;;
		* ) echo "Please answer yes or no.";;
	esac
done

echo $PSSWRD >> $PROJECT_DIR/$PROGRAM_ID/metadata/mrftppass.txt
touch $PROJECT_DIR/$PROGRAM_ID/metadata/scans.csv
echo "source_name							target_name" >> $PROJECT_DIR/$PROGRAM_ID/metadata/scans.csv
touch $PROJECT_DIR/$PROGRAM_ID/metadata/upload_check.csv
echo "Session ID" >> $PROJECT_DIR/$PROGRAM_ID/metadata/upload_check.csv
echo "Basic environment is set up."
