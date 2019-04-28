#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 22:57:38 2018

@author: sumanthnandamuri
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from   torchvision import models

class SUMNet(nn.Module):
    def __init__(self,in_ch,out_ch):
        super(SUMNet, self).__init__()
        
        self.conv1     = nn.Conv2d(in_ch,64,3,padding=1)
        self.bn1       = nn.BatchNorm2d(64,eps=1e-5,momentum=0.1,affine=True,track_running_stats=True)
        self.conv2     = nn.Conv2d(64,128,3,padding=1)   
        self.bn2       = nn.BatchNorm2d(128,eps=1e-5,momentum=0.1,affine=True,track_running_stats=True)
        self.pool1     = nn.MaxPool2d(2, 2, return_indices = True)
        self.conv3a    = nn.Conv2d(128,256,3,padding=1) 
        self.bn3a       = nn.BatchNorm2d(256,eps=1e-5,momentum=0.1,affine=True,track_running_stats=True)
        self.conv3b    = nn.Conv2d(256,256,3,padding=1)
        self.bn3b       = nn.BatchNorm2d(256,eps=1e-5,momentum=0.1,affine=True,track_running_stats=True)
        self.pool2     = nn.MaxPool2d(2, 2, return_indices = True)
        self.conv4a    = nn.Conv2d(256,512,3,padding=1) 
        self.bn4a       = nn.BatchNorm2d(512,eps=1e-5,momentum=0.1,affine=True,track_running_stats=True)
        self.conv4b    = nn.Conv2d(512,512,3,padding=1)
        self.bn4b       = nn.BatchNorm2d(512,eps=1e-5,momentum=0.1,affine=True,track_running_stats=True)
        self.pool3     = nn.MaxPool2d(2, 2, return_indices = True)
        self.conv5a    = nn.Conv2d(512,512,3,padding=1) 
        self.bn5a       = nn.BatchNorm2d(512,eps=1e-5,momentum=0.1,affine=True,track_running_stats=True)
        self.conv5b    = nn.Conv2d(512,512,3,padding=1)
        self.bn5b       = nn.BatchNorm2d(512,eps=1e-5,momentum=0.1,affine=True,track_running_stats=True)
        self.pool4     = nn.MaxPool2d(2, 2, return_indices = True)     
        
        
        
        self.unpool4   = nn.MaxUnpool2d(2, 2)
        self.donv5b    = nn.Conv2d(1024, 512, 3, padding = 1)
        self.donv5a    = nn.Conv2d(512, 512, 3, padding = 1)
        self.unpool3   = nn.MaxUnpool2d(2, 2)
        self.donv4b    = nn.Conv2d(1024, 512, 3, padding = 1)
        self.donv4a    = nn.Conv2d(512, 256, 3, padding = 1)
        self.unpool2   = nn.MaxUnpool2d(2, 2)
        self.donv3b    = nn.Conv2d(512, 256, 3, padding = 1)
        self.donv3a    = nn.Conv2d(256,128, 3, padding = 1)
        self.unpool1   = nn.MaxUnpool2d(2, 2)
        self.donv2     = nn.Conv2d(256, 64, 3, padding = 1)
        self.donv1     = nn.Conv2d(128, 32, 3, padding = 1)
        self.output    = nn.Conv2d(32, out_ch, 1)        
       
        
    def forward(self, x):
        conv1          = F.relu(self.bn1(self.conv1(x)), inplace = True)
        conv2          = F.relu(self.bn2(self.conv2(conv1)), inplace = True)
        pool1, idxs1   = self.pool1(conv2)        
        conv3a         = F.relu(self.bn3a(self.conv3a(pool1)), inplace = True)
        conv3b         = F.relu(self.bn3b(self.conv3b(conv3a)), inplace = True)
        pool2, idxs2   = self.pool2(conv3b)
        conv4a         = F.relu(self.bn4a(self.conv4a(pool2)), inplace = True)
        conv4b         = F.relu(self.bn4b(self.conv4b(conv4a)), inplace = True)
        pool3, idxs3   = self.pool3(conv4b)
        conv5a         = F.relu(self.bn5a(self.conv5a(pool3)), inplace = True)
        conv5b         = F.relu(self.bn5b(self.conv5b(conv5a)), inplace = True)
        pool4, idxs4   = self.pool4(conv5b)
        
        unpool4        = torch.cat([self.unpool4(pool4, idxs4), conv5b], 1)
        donv5b         = F.relu(self.donv5b(unpool4), inplace = True)
        donv5a         = F.relu(self.donv5a(donv5b), inplace = True)
        unpool3        = torch.cat([self.unpool4(donv5a, idxs3), conv4b], 1)
        donv4b         = F.relu(self.donv4b(unpool3), inplace = True)
        donv4a         = F.relu(self.donv4a(donv4b), inplace = True)
        unpool2        = torch.cat([self.unpool3(donv4a, idxs2), conv3b], 1)
        donv3b         = F.relu(self.donv3b(unpool2), inplace = True)
        donv3a         = F.relu(self.donv3a(donv3b))
        unpool1        = torch.cat([self.unpool2(donv3a, idxs1), conv2], 1)
        donv2          = F.relu(self.donv2(unpool1), inplace = True)
        donv1          = F.relu(self.donv1(torch.cat([donv2,conv1],1)), inplace = True)
        output         = self.output(donv1)          
       
        return output