#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 10:53:40 2018

@author: abhi28577
"""

import boto3

# Source Class/Methods

class ClientLocator:
    def __init__(self,client):
        self._client=boto3.client(client,region_name='ap-southeast-2')

    
    def get_client(self):
        return self._client

#   Accessing Inherited Methods
class EC2Client(ClientLocator):
    def __init__(self):
        super().__init__('ec2')
        