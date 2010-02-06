#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
setup(name="pardus-boot-manager-gtk",
      version="0.1",
      packages = ["boot_manager_gtk", "asma.addons"],
      scripts = ["boot-manager-gtk.py"],
      description= "Pardus Boot Manager's gtk port",
      author="Rıdvan Örsvuran",
      author_email="flasherdn@gmail.com"
)
