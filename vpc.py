#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 11:12:53 2018

@author: abhi28577
"""

class VPC:
    def __init__(self,client):
        self._client=client
        """ :type : pyboto3.ec2 """
    
# Method to create Virtual Private Cloud against User
    def create_vpc(self):
        print("Creating VPC.....")
        return self._client.create_vpc(CidrBlock='10.0.0.0/16')
    
# Method to Tag Name and Id to VPC/Subnets
    def add_name_tag(self, resource_id, resource_name):
        print('Adding ' + resource_name + ' tag to the ' + resource_id)
        return self._client.create_tags(Resources=[resource_id], Tags=[{'Key': 'Name','Value': resource_name}])

#Method to Create Internet Gateway for VPC
    def create_internet_gateway(self):
        print('Creating an Internet Gateway to VPC...')
        return self._client.create_internet_gateway()
    
# Method to attach Internet Gateway to VPC post creation of Internet Gateway
    def attach_internet_gateway_to_vpc(self, vpc_id, igw_id):
        print('Attaching Internet Gateway ' + igw_id + ' to VPC ' + vpc_id)
        return self._client.attach_internet_gateway(InternetGatewayId=igw_id,VpcId=vpc_id)

# Method to create Subnet
    def create_subnet(self, vpc_id, cidr_block):
        print('Creating a subnet for VPC' + vpc_id + ' with CIDR block ' + cidr_block)
        return self._client.create_subnet(VpcId=vpc_id,CidrBlock=cidr_block)

# Method to create Public Route Table
    def create_public_route_table(self, vpc_id):
        print('Creating public Route Table for VPC ' + vpc_id)
        return self._client.create_route_table(VpcId=vpc_id)

# Method to create Route for Internet Gateway to Public Route Table
    def create_internet_gateway_route_to_public_route_table(self, rtb_id, igw_id):
        print('Adding route for IGW ' + igw_id + ' to Route Table ' + rtb_id)
        return self._client.create_route(RouteTableId=rtb_id,GatewayId=igw_id,DestinationCidrBlock='0.0.0.0/0')

# Method to Associate Subnet to the Route Table
    def associate_subnet_with_route_table(self, subnet_id, rtb_id):
        print('Associating subnet ' + subnet_id + ' with Route Table ' + rtb_id)
        return self._client.associate_route_table(SubnetId=subnet_id,RouteTableId=rtb_id)

# Method to Assign IP Addresses to Subnet Automatically
    def allow_auto_assign_ip_addresses_for_subnet(self, subnet_id):
        return self._client.modify_subnet_attribute(SubnetId=subnet_id,MapPublicIpOnLaunch={'Value': True})

    
        
        