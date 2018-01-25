
#import statements

import argparse
import boto3
import os
import sys
from pathlib import Path

#regionsCode

regions=['us-east-1','us-east-2','us-west-1','us-west-2','eu-west-1','eu-west-2','eu-west-3',
         'ca-central-1','eu-central-1','ap-northeast-1','ap-northeast-2','ap-southeast-1',
         'ap-southeast-2','ap-south-1','sa-east-1'];


#regionsName

regionsName=['US East\n(N. Virginia)','US East (Ohio)','US West \n(N.California)','US West (Oregon)','EU (Ireland)','EU (London)','EU (Paris)',
         'Canada (Central)','EU (Frankfurt)','Asia Pacific\n(Tokyo)','Asia Pacific\n(Seoul)','Asia Pacific\n(Singapore)',
         'Asia Pacific\n(Sydney)','Asia Pacific\n(Mumbai)','South America\n(São Paulo)'];



total=0;
#userName=os.getenv('username');
home=Path.home();


#methods



def StatusInstances(input): #instances state (running,stopped,terminated)
    try:
        count=0;
        zone=connect.describe_availability_zones();
        for zones in zone['AvailabilityZones']:
            zname=zones["ZoneName"]
            getStaIns=connects.instances.filter(Filters=[
            {
                'Name':'instance-state-name',
                'Values':[input]
                },
            {
                'Name':'availability-zone',
                'Values':[zname]
                }
            ]
                                            );
            for staIns in getStaIns:
                print(regionsName[i]+"\t"+zname+"\t"+staIns.instance_type+"\t\t"+staIns.id+"\t"+staIns.public_ip_address+"\t\t\t"+staIns.key_name);
                count=count+1;
        if count >=1:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"+str(count)+" "+input);
            total=count;
    except:
        print("");



def filterByTag(getNum): #filter by tags
    zone=connect.describe_availability_zones();
    for zones in zone['AvailabilityZones']:
        zname=zones["ZoneName"]
        getStaIns=connects.instances.filter(Filters=[
        {
            'Name':'instance-state-name',
            'Values':['running','stopped','terminated']
            },
        {
            'Name':'availability-zone',
            'Values':[zname]
            }
        ]
                                        );
        if getNum == 0: #all [tagged and untagged]
            for ins in getStaIns:
                if ins.tags:
                    print(regionsName[i]+"\t"+zname+"\t"+ins.instance_type+"\t\t"+ins.id+"\t"+ins.public_ip_address+"\t\t\t"+ins.key_name+"\t\tTAGGED");
                else:
                    print("\n\n"+regionsName[i]+"\t"+zname+"\t"+ins.instance_type+"\t\t"+ins.id+"\t"+ins.public_ip_address+"\t\t\t"+ins.key_name+"\t\tUNTAGGED");
        if getNum == 1: #tagged
            for ins in getStaIns:
                if ins.tags:
                    print("\n\n"+regionsName[i]+"\t"+zname+"\t"+ins.instance_type+"\t\t"+ins.id+"\t"+ins.public_ip_address);
                    for tag in ins.tags:
                            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t"+tag['Key']+"\t\t\t"+tag['Value']);

        if getNum == 2: #untagged
            for ins in getStaIns:
                if not ins.tags:
                    print("\n\n"+regionsName[i]+"\t"+zname+"\t"+ins.instance_type+"\t\t"+ins.id+"\t"+ins.public_ip_address);


def configure(): #creating configuration files
    path=str(home)+"\\.aws\\";
    accessKey=input("Enter the AWS ACCESS KEY ID:");
    secretKey=input("Enter the AWS SECRET ACCESS KEY:");
    if not os.path.exists(path):
        os.mkdir(path);
    createFile=open(path+"credentials","wb+");
    send="[default]\naws_access_key_id = "+accessKey+"\naws_secret_access_key = "+secretKey+"";
    createFile.write(send.encode());
    backupFile=open(path+".bak","wb+");
    backupFile.write(send.encode());
    print("\nConfig file updated.\n");


def checkConfig(): #checking for configuration files 
    access=0;
    path=str(home)+"\\.aws\\";
    if not os.path.exists(path):
        access=access+1;
    return access;


def createProfile(): #create new profile
    profilename=input("PROFILE NAME: ");
    accessKey=input("AWS ACCESS KEY ID: ");
    secretKey=input("AWS SECRET ACCESS KEY: ");
    path=str(home)+"\\.ResourceMonitor\\";
    if not os.path.exists(path):
        os.mkdir(path);
    createProfile=open(path+profilename,"wb+");
    send="[default]\naws_access_key_id = "+accessKey+"\naws_secret_access_key = "+secretKey+"";
    createProfile.write(send.encode());
    print("\nProfile created successfully.\n");


def restore(): #restoring the backup file
    path=str(home)+"\\.aws\\";
    backupFile=open(path+".bak","r");
    createFile=open(path+"credentials","wb+");
    default=backupFile.read();
    createFile.write(default.encode());
    
    


def profile(paths): #change profile
    path=str(home)+"\\.aws\\";
    if not os.path.exists(path):
        os.mkdir(path);
    openFile=open(str(home)+"\\.ResourceMonitor\\"+paths,"r");
    fileText=openFile.read();
    sendFile=open(path+"credentials","wb+");
    sendText=sendFile.write(fileText.encode());
    print("\nprofile changed.\n");

def deleteProfile(profileName): #delete profile
    os.remove(str(home)+"\\.ResourceMonitor\\"+profileName);
    print("\nProfile deleted successfully");

#argument parser

parser=argparse.ArgumentParser(description="Resource Monitor - AWS EC2",formatter_class=argparse.RawTextHelpFormatter);

parser.add_argument("options",help="instance state [ running | stopped | terminated | all ] \ntags [ tagged | untagged | tags ]\nconfiguration [ configure | createprofile | deleteprofile ]"
                    "\n\n[instance state]\n\nrunning = display all running instances\nstopped = display all stopped instances\nterminated = display all terminated instances"
                    "\nall = diplay all instances"
                    "\n\n[tags]\n\ntagged = display all tagged instances\nuntagged = display all untagged instances\ntags = display all tagged and untagged instances\n\n[Configuration]\n\nconfigure = configure authentication keys\ncreateprofile = create new profile"
                    "\ndeleteprofile = delete the created profile\n\n[ Config file location : C:\\Users\\..\\.ResourceMonitor ]");
parser.add_argument("--region",help="Regions");
parser.add_argument("--profile",help="Profile Name");

get=checkConfig();
args=parser.parse_args();

if args.options=="configure": #configure authentication keys
    configure();

elif args.options=="createprofile": #create new profile
    createProfile();

elif args.options=="deleteprofile": #delete profile
    profileName=input("PROFILE NAME: ");
    deleteProfile(profileName);

elif not get==0: #checking config files
    print("No config file detected. type > monitor configure");
    sys.exit();



#action for arguments

if args.options=="running":  #running
    if args.profile:
        profile(args.profile);
    if args.region:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY PAIR NAME\t\tTOTAL\n");
        connects=boto3.resource('ec2',args.region);
        connect=boto3.client('ec2',args.region);
        i=regions.index(args.region);
        StatusInstances("running");
    else:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY PAIR NAME\t\tTOTAL\n");
        for i in range(0,10):
            connects=boto3.resource('ec2',regions[i]);
            connect=boto3.client('ec2',regions[i]);
            StatusInstances("running");


if args.options=="stopped": #stopped
    if args.profile:
        profile(args.profile);
    if args.region:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY PAIR NAME\t\tTOTAL\n");
        connects=boto3.resource('ec2',args.region);
        connect=boto3.client('ec2',args.region);
        i=regions.index(args.region);
        StatusInstances("stopped");
    else:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY PAIR NAME\t\tTOTAL\n");
        for i in range(0,10):
            connects=boto3.resource('ec2',regions[i]);
            connect=boto3.client('ec2',regions[i]);
            StatusInstances("stopped");


if args.options=="terminated": #terminated
    if args.profile:
        profile(args.profile);
    if args.region:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY PAIR NAME\t\tTOTAL\n");
        connects=boto3.resource('ec2',args.region);
        connect=boto3.client('ec2',args.region);
        i=regions.index(args.region);
        StatusInstances("terminated");
    else:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY PAIR NAME\t\tTOTAL\n");
        for i in range(0,10):
            connects=boto3.resource('ec2',regions[i]);
            connect=boto3.client('ec2',regions[i]);
            StatusInstances("terminated");



if args.options=="all": #all [running,stopped,terminated]
    if args.profile:
        profile(args.profile);
    if args.region:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY PAIR NAME\t\tTOTAL\n");
        connects=boto3.resource('ec2',args.region);
        connect=boto3.client('ec2',args.region);
        i=regions.index(args.region);
        StatusInstances("running");
        StatusInstances("stopped");
        StatusInstances("terminated");
    else:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY PAIR NAME\t\tTOTAL\n");
        for i in range(0,10):
            connects=boto3.resource('ec2',regions[i]);
            connect=boto3.client('ec2',regions[i]);
            StatusInstances("running");
            StatusInstances("stopped");
            StatusInstances("terminated");

if args.options=="tagged": #tagged
    if args.profile:
        profile(args.profile);
    if args.region:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY NAME\t\tKEY VALUE\n");
        i=regions.index(args.region);
        connects=boto3.resource('ec2',args.region);
        connect=boto3.client('ec2',args.region);
        filterByTag(1);
    else:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY NAME\t\tKEY VALUE\n");
        for i in range(0,10):
            connects=boto3.resource('ec2',regions[i]);
            connect=boto3.client('ec2',regions[i]);
            filterByTag(1);


if args.options=="untagged": #untagged
    if args.profile:
        profile(args.profile);
    if args.region:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY NAME\t\tKEY VALUE\n");
        i=regions.index(args.region);
        connects=boto3.resource('ec2',args.region);
        connect=boto3.client('ec2',args.region);
        filterByTag(2);
    else:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY NAME\t\tKEY VALUE\n");
        for i in range(0,10):
            connects=boto3.resource('ec2',regions[i]);
            connect=boto3.client('ec2',regions[i]);
            filterByTag(2);

if args.options=="tags": #tags[tagged and untagged]
    if args.profile:
        profile(args.profile);
    if args.region:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY NAME\t\tKEY VALUE\n");
        i=regions.index(args.region);
        connects=boto3.resource('ec2',args.region);
        connect=boto3.client('ec2',args.region);
        filterByTag(0);
    else:
        print("\nREGION\t\tZONE\t\tINSTANCE TYPE\t\tINSTANCE ID\t\tPUBLIC IP ADDRESS\t\tKEY NAME\t\tKEY VALUE\n");
        for i in range(0,10):
            connects=boto3.resource('ec2',regions[i]);
            connect=boto3.client('ec2',regions[i]);
            filterByTag(0);

restore();
