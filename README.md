# AWS RESOURCE MONITORING

This script is used to monitor the EC2 instances details in all the regions and accounts simultaneously.

## Problems in Exisiting System (AWS CLI TOOL)


In the exisiting system, the user will not able to monitor the instances details in all the regions and accounts at the same time. And also
the user need to configure the Authentication keys every time, when they want to monitor the instances in different account.

## Built with
```
Languages used: PYTHON

Libraries used: argparser boto3
```

## System Requirements

```
Supported OS : WINDOWS LINUX
INTERNET CONNECTION REQUIRED
```

## Prerequisites


```
Python 3.6.4
boto3
```

### Installing

Install python from the link given below.

```
Python 3.6.4 - https://www.python.org/
```

To install boto3, open command prompt and enter the following command.

```
pip install boto3
```

## Configure EC2 Authentication keys

Open command prompt and enter the following command

```
monitor.py configure
```
Now it will ask SECRET ACCESS KEY, ACCESS KEY ID.

```
AWS Access Key ID : your_access_key_id
AWS Secret Access Key: your_secret_access_key

```

## Running the script

open command prompt and enter the following command.

```
monitor.py --help
```
This will display the usage commands.

Usage commands:

```
usage: monitor.py [-h] [--region REGION] [--profile PROFILE] options

Resource Monitor - AWS EC2

positional arguments:
  options            instance state [ running | stopped | terminated | all ]
                     tags [ tagged | untagged | tags ]
                     configuration [ configure | createprofile | deleteprofile ]

                     [instance state]

                     running = display all running instances
                     stopped = display all stopped instances
                     terminated = display all terminated instances
                     all = diplay all instances

                     [tags]

                     tagged = display all tagged instances
                     untagged = display all untagged instances
                     tags = display all tagged and untagged instances

                     [Configuration]

                     configure = configure authentication keys
                     createprofile = create new profile
                     deleteprofile = delete the created profile

                     [ Config file location : C:\Users\..\.ResourceMonitor ]

optional arguments:
  -h, --help         show this help message and exit
  --region REGION    Regions
  --profile PROFILE  Profile Name
  
```

## Demo

* TO DISPLAY ALL RUNNING INSTANCES

```
monitor running

```

* TO DISPLAY ALL RUNNING INSTANCES IN SPECIFIC REGION

```
monitor running --region us-west-1
```

* TO DISPLAY ALL TAGGED INSTANCES

```
monitor tagged

```

* TO DISPLAY BOTH TAGGED AND UNTAGGED INSTANCES IN SPECIFIC REGION

```
monitor tags --region us-east-2

```

## Multiple Profiles

When you have multiple accounts, you don't need to change the authentication keys each time, save your keys in profile. 
so next time, just enter the profile name to switch to that account.

* To CREATE PROFILE

```
monitor createprofile
```

* TO DELETE PROFILE

```
monitor deleteprofile
```

* TO MONITOR THE INSTANCES ON DIFFERENT PROFILE

  
  EXAMPLE : TO MONITOR THE RUNNING INSTANCES IN DIFFERENT PROFILE

```
monitor running --profile test
```
