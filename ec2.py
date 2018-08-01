#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 15:46:23 2018

@author: abhi28577
"""

class EC2:
    def __init__(self,client):
        self._client=client
        """ :type : pyboto3.ec2 """
    
    def Create_Key_Pair(self,key_name):
        print("Creating Key-Pair:" + key_name)
        return self._client.create_key_pair(KeyName=key_name)
    
    def Create_Security_group(self,group_name,description,vpc_id):
        print("Creating Security Group with Group Name:" + group_name + " Description:" + description + " VPC Id:" + vpc_id)
        return self._client.create_security_group(GroupName=group_name,Description=description,VpcId=vpc_id)
    
    def add_inbound_rule_to_security(self,Security_Group_Id):
        print('Adding Inbound Security Group using Group Id:' + Security_Group_Id)
        self._client.authorize_security_group_ingress(GroupId=Security_Group_Id, 
                                                      IpPermissions=[
                                                           {
                                                            'IpProtocol': 'tcp',
                                                            'FromPort':80,
                                                            'ToPort':80,
                                                            'IpRanges':[{'CidrIp': '0.0.0.0/0'}]
                                                            },
                                                           {
                                                            'IpProtocol':'tcp',
                                                            'FromPort':22,
                                                            'ToPort':22,
                                                            'IpRanges':[{'CidrIp': '0.0.0.0/0'}]                                                            
                                                            }
                                                              ]
                                                      )
    
    
    def ec2_launch_instance(self,image_id,key_name,min_count,max_count,Security_Group_Id,subnetId,user_data):
        print('Launching EC2 Instance(s).....')
        return self._client.run_instances(
                ImageId=image_id,
                KeyName=key_name,
                MinCount=min_count,
                MaxCount=max_count,
                InstanceType='t2.micro',
                SecurityGroupIds=[Security_Group_Id],
                SubnetId=subnetId,
                UserData=user_data
            )                                    
    
    def describe_ec2_instances(self):
        print('Describe EC2 Instances.....')
        return self._client.describe_instances()

