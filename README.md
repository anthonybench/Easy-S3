# **S3 Bucket Upload Tool**
*Isaac Yep; BlackBerry - Data Architecture*

<br />

## Preface
This is a command line tool written in *Python*, purposed to upload files to an *AWS* destination, namely a file path within a target *bucket*.

As there are multiple use-cases for such a process to be automated, **a flag must be provided** to signal your use-case.

This tool was originally written to automate a component of the proccess [documented here](https://cylance.atlassian.net/wiki/spaces/DA/pages/787350066/Deployment+Run+Book).

**Note** that this tool's core dependency is the **Boto3** *Python* library. If you are unfamiliar with this library, it requires *AWS* credentials (see docs in references) set in your `~/.aws` directory.\
In `~/.aws/credentials`, ensure you have at least one *profile* with minimum fields as shown:
```
[cylancedev]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
aws_session_token = YOUR_SESSION_TOKEN
```
and in `~/.aws/config`, ensure you have something like:
```
[default]
region=us-east-1
```

<br />

## **Table of Contents**
- [Usage Help](#usage-help)
- [Single Local File](#single-local-file)
- [Multiple Local Files from Config](#multiple-local-files-from-config)

[References](#references)

<br /><hr>

## Usage Help
To get a succinct usage guide in your shell, use the `-h` flag:
```bash
$ python3 tobucket.py -h
```
If you make an invalid use of this tool, like providing a mistaken flag or none at all, you will get this usage message defaultly.

<br />

## Single Local File
To upload a single file from your local file system, use the `-s` flag:
```bash
$ python3 tobucket.py -s <src_path> <dest_bucket> <dest_path> <aws_credentialProfile>
```
- `src_path` - local file path to upload
- `dest_bucket` - target S3 bucket to upload to
- `dest_path` - target file path in that bucket
- `aws_credentialProfile` - profile name set in *AWS* config

<br />

## Multiple Local Files from Config
To upload multiple local files from a configuration, author a *json* file anywhere, it doesn't need to contain the `.json` file extension.\
The object therein will simply contain **AWS credentials profile names** as keys to dictate which AWS account is doing the uploading. The values of these keys will be objects containing **bucket names** as keys, with values as objects containing key-values pairs representing the t**ransactions**.\
In summary, a *profile name* contains *buckets*, which contain any number of *transactions* as `"<local_source_path>" : "<bucket_destination_path>"`:
```json
{
  "myProfile" : {

    "targetBucket" : {
      "./file1.txt" : "dir1/dir2/file1.txt",
      "./someDir/file2.txt" : "dir1/file2.txt",
      "./myDir/" : "dir1/"
    }

  }
}
```
This will dictate uploading `./file1.txt` to `dir1/dir2/file1.txt` at bucket `myBucket` under the `myProfile` credentials, and so on for the other transactions.\
**Note** that the `local_source_path` is relative to the python exectuion (workind directory) and not the config file location.\
The last transaction in the above example is a directory. You can send the contents (file tree preserved) to the destination, though you must **note that directory paths end with front-slashes '`/`'**.

To run this upload process, use the `-c` flag:
```bash
$ python3 toobucket.py -c <config_file_path>
```
- `config_file_path` - relative path to configuration file

<br />

## References
- [Boto3 Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [JSON Docs](https://docs.python.org/3/library/json.html)
- [S3 Docs](https://docs.aws.amazon.com/s3/index.html)
 
<br />

[Back to Table of Contents](#table-of-contents)
