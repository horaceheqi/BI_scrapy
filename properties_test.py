#!/usr/bin/env python
# -*- coding:utf-8 -*

from mingyan.core.propertiesutils import Properties
import os

print(os.path.dirname(__file__))
dictProperties = Properties(os.path.dirname(__file__)+"/config.properties").getProperties()
print(dictProperties['startpage'])
