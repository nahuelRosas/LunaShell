#!/usr/bin/sudo ./bin/python3
import os
from utils.add_repositories import add_repositories
from utils.install_package import install_package
from utils.upgrade_system_all import upgrade_system_all

os.system("clear")
install_package("git")
add_repositories()
upgrade_system_all()

