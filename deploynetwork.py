#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 11:27:14 2018

@author: abhi28577
"""

from vpc import VPC
from ec2 import EC2
from client_locator import EC2Client


def main():
    
# Create VPC
    ec2_client = EC2Client().get_client()
    vpc=VPC(ec2_client)
    
    vpc_response= vpc.create_vpc()
    print('VPC Created:' + str(vpc_response))

# Adding Name to Newly Created VPC Id
    vpc_name='AbhiCloudNet'
    vpc_id= vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id,vpc_name)
    print("Name of VPC:" + vpc_name + "and VPC Id:" + vpc_id)
    
# Creating Internet Gateway
    InternetGateway = vpc.create_internet_gateway()
    InternetGatewayId = InternetGateway['InternetGateway']['InternetGatewayId']

# Attaching Internet Gateway to VPC
    vpc.attach_internet_gateway_to_vpc(vpc_id,InternetGatewayId)

# Creating Public Subnet
    Public_Subnet_Response = vpc.create_subnet(vpc_id,'10.0.1.0/24')
    PublicSubnetId = Public_Subnet_Response['Subnet']['SubnetId']
    print("Public Subnet Created Successfully")

# Attaching Name/Tag to Public Subnet
    Public_Subnet_Name='AbhiPublicSubnet'    
    vpc.add_name_tag(PublicSubnetId,Public_Subnet_Name)
    print("Name of Public Subnet:" + Public_Subnet_Name + "and VPC Id:" + PublicSubnetId)


# Creating Public Route Table
    Public_Route_Table = vpc.create_public_route_table(vpc_id)
    RouteTableId = Public_Route_Table['RouteTable']['RouteTableId']
    
# Creating Route for Internet Gateway to Public Route Table
    vpc.create_internet_gateway_route_to_public_route_table(RouteTableId,InternetGatewayId)

# Associating Subnet to Route Table
    vpc.associate_subnet_with_route_table(PublicSubnetId,RouteTableId)

# Auto Allocation of IP Address to Subnet
    vpc.allow_auto_assign_ip_addresses_for_subnet(PublicSubnetId)
    
# Creating Private Subnet
    Private_Subnet_Response = vpc.create_subnet(vpc_id,'10.0.2.0/24')
    PrivateSubnetId = Private_Subnet_Response['Subnet']['SubnetId'] 
    print("Private Subnet Created Successfully" + PrivateSubnetId)

# Attaching Name/Tag to Private Subnet
    Private_Subnet_Name='AbhiPrivateSubnet'    
    vpc.add_name_tag(PrivateSubnetId,Private_Subnet_Name)
    print("Name of Private Subnet:" + Private_Subnet_Name + "and VPC Id:" + PrivateSubnetId)

# Creating Ec2 Instance
    ec2=EC2(ec2_client)

# Create Key-Value Pair
    key_pair_name = 'Abhi-KeyPair'
    EC2_KeyPairName=ec2.Create_Key_Pair(key_pair_name)
    print("New Key-Pair" + key_pair_name +  "of EC2 Instance:" + str(EC2_KeyPairName))

# Creating Security Group for Public
    Public_Security_Group_Name='Abhi-Public-Security-Group'
    PublicDescription='Public Security Group for Public Subnet Internet Access'
    VpcId = vpc_id
    EC2_PublicSecurityResponse = ec2.Create_Security_group(Public_Security_Group_Name,PublicDescription,VpcId)
    Public_Security_Group_Id = EC2_PublicSecurityResponse['GroupId']
    print("Security Group Id:" + Public_Security_Group_Id)
    
# Adding Authorization to Security Group using Inbound Rule
    ec2.add_inbound_rule_to_security(Public_Security_Group_Id)
    print("Added Inbound Rule to Public Security:" + Public_Security_Group_Name)
    
 # Creating StartUp Script on EC2 Instance
    User_Data = """#!/bin/bash
                    yum update -y
                    yum -y install httpd
                    service httpd start
                    chkconfig httpd on
                    echo "<html><body><h2>Hello World</h2></body></html>" > /var/www/html/index.html"""

# Defining Updated Amazon Machine Image(AMI)
    AMI_Id  = 'ami-39f8215b'

#  Launching Public EC2 Instance(s)    
    ec2.ec2_launch_instance(AMI_Id,key_pair_name,1,1,Public_Security_Group_Id,PublicSubnetId,User_Data)
    print('Ec2 Instance Launched Successfully with Latest AMI for Public Network:' + AMI_Id)
   
# Creating Security Group for Private
    Private_Security_Group_Name='Abhi-Private-Security-Group'
    PrivateDescription='Private Security Group for Public Subnet Internet Access' 
    VpcId = vpc_id
    EC2_PrivateSecurityResponse = ec2.Create_Security_group(Private_Security_Group_Name,PrivateDescription,VpcId)
    Private_Security_Group_Id = EC2_PrivateSecurityResponse['GroupId']
   
 # Adding Authorization to Security Group using Inbound Rule
    ec2.add_inbound_rule_to_security(Private_Security_Group_Id)
    print("Added Inbound Rule to Pfivate Security:" + Private_Security_Group_Name)   

# Launching Private EC2 Instance(s)
    ec2.ec2_launch_instance(AMI_Id,key_pair_name,1,1,Private_Security_Group_Id,PrivateSubnetId,"""""")
    print('Ec2 Instance Launched Successfully with Latest AMI for Private Network:' + AMI_Id)
    
# Describing EC2 Instances
    EC2_Describe_Response = ec2.describe_ec2_instances()
    print("EC2 Description:" + EC2_Describe_Response)


    
if __name__ == '__main__':
    main()
    