#=====================================
# Automation Component;
#   AWS to Linux Deployment Run Book
# -- Isaac Yep
#=====================================
import boto3
import sys
import os
import json

'''
This script automates uploads files to S3 buckets
in lieu of the process documented here:

https://cylance.atlassian.net/wiki/spaces/DA/pages/787350066/Deployment+Run+Book

Usage:
-- Print this usage guide again
$ python3 tobucket.py -h

-- Upload single local file to an S3 destination
$ python3 tobucket.py -s <src_path> <dest_bucket> <dest_path> <aws_credentialProfile>
// The <destination_file_path> begins from <dest_bucket>

-- Upload mulitple local files to an S3 destination from a config file
$ python3 tobucket.py -c <config_file_path>
// Configuration must be a json file, though need not contain extension
// See README.md for configuration formatting
'''


#----------------------------------------------------
#   Global
#----------------------------------------------------
# AWS Parameters
session = boto3.Session(profile_name='cylancedev')
s3 = session.resource('s3')

# Utility: Usage Message
def usageMessage():
  print("\n\n----------\n  Usage  \n-----------")
  print("-- Print this usage guide again")
  print("$ python3 {0} -h\n".format(__file__))
  print("-- Upload single local file to an S3 destination")
  print("$ python3 {0} -s <src_path> <dest_bucket> <dest_path> <aws_credentialProfile>".format(__file__))
  print("// The <dest_path> begins from <dest_bucket>/\n")
  print("-- Upload multiple local files to an S3 destination from 'config.json'")
  print("$ python3 {0} -c <config_file_path>".format(__file__))
  print("// Configuration must be a json file, though need not contain extension")
  print("// See README.md for configuration formatting\n")

# Utility: Upload and Report
def upload(bkt, src, dest, profile):
  session = boto3.Session(profile_name=profile)
  s3 = session.resource('s3')
  if src[-1] == '/':        ## Directory
    for paths in os.walk(src):
      for f in paths[2]:
        if paths[0] == './':
          source = "./{0}".format(f)
          destination = f
        else:
          if paths[0][-1] == '/': 
            source = "{0}{1}".format(paths[0], f)
            destination = source.lstrip('./')
          else:
            source = "{0}/{1}".format(paths[0], f)
            destination = source.lstrip('./')
        tokens = [i for i in src.split('/') if (i != '..') and (i != '') and (i != '.')]
        if len(tokens) > 1:
          print("Uploading: {0} --> {1}:{2} as {3}".format('./'+destination, bkt, dest+tokens[-1]+'/'+f, profile))
          s3.Bucket(bkt).upload_file(source, (dest+tokens[-1]+'/'+f).replace(' ', '_'))
        else:
          print("Uploading: {0} --> {1}:{2} as {3}".format('./'+destination, bkt, dest+destination, profile))
          s3.Bucket(bkt).upload_file(source, dest+destination)
  else:                     ## Single File
    print("Uploading: {0} --> {1}:{2} as {3}".format(src, bkt, dest, profile))
    s3.Bucket(bkt).upload_file(src, dest)


#----------------------------------------------------
#   Main
#----------------------------------------------------
def main():
  if len(sys.argv) == 1:    ## no args provided
    usageMessage()
    sys.exit()

  option = (sys.argv[1]).lower()
  if option == '-h':        ## help
    usageMessage()
  elif option == '-s':      ## single local file upload
    if len(sys.argv) < 6:
      print("Error: missing arguments for {0}".format(__file__))
    else:
      upload(sys.argv[3], sys.argv[2], sys.argv[4], sys.argv[5])
  elif option == '-c':      ## multiple local files upload from config.json
    if len(sys.argv) < 3:
      print("Error: missing arguments for {0}".format(__file__))
    else:
      if sys.argv[2][len(sys.argv[2])-5:] == '.json':
        config = json.load(open(sys.argv[2]))
      else:
        config = json.load(open(sys.argv[2]+'.json'))
      for profile in config.keys():
        for bucket in config[profile]:
          for src in config[profile][bucket].keys():
            upload(bucket, src.replace(' ', '_'), config[profile][bucket][src], profile)
  else:                     ## bad args provided
    usageMessage()


#----------------------------------------------------
#   Entry
#----------------------------------------------------
if __name__ == "__main__":
  main()
