
#!/usr/bin/python

#Load 3 modules
# - module load dicomtools/0.8.6
# - module load PYTHON/2.7
# - module load mricrogl/20180412

import sys
import csv
import os
import subprocess
import re

def project_setup(subjectID):
    data = subjectID.split("_")
    path = '/external/rprshnas01/BIDS/test_run/proj/' + str(data[0]) + "_" + str(data[1])
    if not os.path.isdir(path):
        subprocess.Popen(['mkdir', path])
    subprocess.Popen(['mkdir', path + '/' + subjectID])
    subprocess.Popen(['touch', path + '/' + subjectID + '/' + "series_description.csv"])
    with open(path + '/' + subjectID + '/' + "series_description.csv", "w") as sd:
        writer = csv.writer(sd)
        writer.writerow(["Series_Description"])
    subprocess.Popen(['touch', path + '/' + subjectID + '/' + "xnat2bids.json"])



def get_directory(subjectID):
    data = subjectID.split("_")
    dcm_dir = "/external/rprshnas01/nip/rdrshxnatv02/xnat/archive/" + str(data[0]) + "_" + str(data[1]) + "/arc001/" + subjectID + "/SCANS"
    dcmdump_dir = "/external/rprshnas01/BIDS/test_run/bin/dicomdump.exe"
    series_description_csv = "/external/rprshnas01/BIDS/test_run/proj/" + str(data[0]) + "_" + str(data[1]) + '/' + subjectID + "/series_description.csv"
    dcmwindow_dir = '\\external\\rprshnas01\\BIDS\\test_run\\bin\\dicomdump.exe'
    return dcm_dir, dcmdump_dir, series_description_csv, dcmwindow_dir

def push_to_csv(subjectID):
    project_setup(subjectID)
    dcm_dir, dcmdump_dir, series_description_csv, dcmwindow_dir = get_directory(subjectID)
    scanlist = os.listdir(dcm_dir)
    print(scanlist)
    for scan in scanlist:
        dicom = os.listdir(dcm_dir + "/" + scan + "/DICOM")[0]
        full_dicom_path = os.path.join(dcm_dir + '/' + scan + '/DICOM/' + dicom)
        with open(series_description_csv, "a") as sd_csv:
            fieldnames = ["Series_Description"]
            writer = csv.DictWriter(sd_csv, fieldnames = fieldnames, lineterminator = '\n')
            print(full_dicom_path)
            result = subprocess.Popen(['dicomdump', full_dicom_path, "-k", "SeriesDescription"], stdout=subprocess.PIPE).communicate()[0]
            if not full_dicom_path.endswith('.dcm'):
                dicom = os.listdir(dcm_dir + "/" + scan + "/DICOM")[1]
                full_dicom_path = os.path.join(dcm_dir + '/' + scan + '/DICOM/' + dicom)
                print("=*****=" + full_dicom_path + "=*****=")
                result = subprocess.Popen(['dicomdump', full_dicom_path, "-k", "SeriesDescription"], stdout=subprocess.PIPE).communicate()[0]
            sd = re.search("\[[^()]+]", str(result)).group(0)
            #print "THIS IS THE STDOUT " + str(result)
            writer.writerow({'Series_Description': sd})
            print("***********************************")

if __name__ == "__main__":
    subjectID = (sys.argv[1])
    push_to_csv(subjectID)
