#!/usr/bin/python

# This file has 3 functions
#   - Run Dicom_pull
#   - Extract the series description categorize them as either anat, func or dwi
#   - Write to master JSON file that will act as the config file for dcm2bids based on whats in each category

import csv
import sys
import json
import subprocess

def sd2bids(sd_list, path):
  data = {'descriptions': []}
  T1, T2, DTI, EPI, FieldMap = (0,0,0,0,0)

  for sd in sd_list:
    sd = str(sd)[3:len(sd)-4]
    print(sd)

    if "T1" in sd:
      if T1 == 0:
        data['descriptions'].append({
          'dataType': 'anat',
          'modalityLabel': 'T1w',
          'criteria': {
          'SeriesDescription': '*T1*'
          }
          })
        T1 = 1
    elif "T2" in sd:
      if T2 == 0:
        data['descriptions'].append({
          'dataType': 'anat',
          'modalityLabel': 'T2w',
          'criteria': {
          'SeriesDescription': '*T2*'
          }
          })
        T2 = 1
    elif "DTI" in sd:
      if DTI == 0:
        data['descriptions'].append({
          'dataType': 'dwi',
          'modalityLabel': 'dwi',
          'criteria': {
          'SeriesDescription': '*DTI*'
          }
          })
        DTI = 1
    elif "EPI" in sd:
      if "Resting" in sd[sd.index("EPI") + len("EPI"):] and EPI == 0:
        data['descriptions'].append({
          'dataType': 'func',
          'modalityLabel': 'bold',
          'customLabels': 'task-rest',
          'criteria': {
          'SeriesDescription': '*EPI' + sd[sd.index("EPI") + len("EPI"):len(sd)-1] + '*'
          }
          })
        EPI = 1
      elif "Resting" not in sd[sd.index("EPI") + len("EPI"):]: 
        data['descriptions'].append({
          'dataType': 'func',
          'modalityLabel': 'bold',
          'customLabels': 'task-' + sd[sd.index("EPI") + len("EPI_"):],
          'criteria': {
          'SeriesDescription': '*EPI' + sd[sd.index("EPI") + len("EPI"):] + '*'
          }
          })
    elif "FieldMap" in sd:
      if FieldMap == 0:
        data['descriptions'].append({
          'dataType': 'fmap',
          'modalityLabel': 'fmap',
          'criteria': {
          'SeriesDescription': '*FieldMap*'
          }
          })
        FieldMap = 1
  with open(path + "xnat2bids.json", 'w') as outfile:
    json.dump(data, outfile)

def json_builder(subjectID):
  sd_list = []
  ID = subjectID.split("_")
  path = '/external/rprshnas01/BIDS/test_run/proj/' + str(ID[0]) + "_" + str(ID[1]) + '/' + subjectID + '/'
  with open(path + "series_description.csv", 'r') as sd_csv:
    sd_reader = csv.reader(sd_csv)
    sd_list = list(sd_reader)[1:]
    sd2bids(sd_list, path)

if __name__ == "__main__":
  subjectID = (sys.argv[1])
  dcmpull_path = '/external/rprshnas01/BIDS/test_run/bin/dicom_pull.py'
  #subprocess.Popen(['python', dcmpull_path, subjectID])
  json_builder(subjectID)

