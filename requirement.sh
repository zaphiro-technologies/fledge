#!//usr/bin/env bash

##--------------------------------------------------------------------
## Copyright (c) 2019 Dianomic Systems
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##--------------------------------------------------------------------

##
## Author: Ashish Jabble
##


set -e

sudo apt-get install avahi-daemon curl
sudo apt-get install cmake g++ make build-essential autoconf automake uuid-dev
sudo apt-get install libtool libboost-dev libboost-system-dev libboost-thread-dev libpq-dev libssl-dev libz-dev
sudo apt-get install python-dbus python-dev python3-dev python3-pip
sudo apt-get install postgresql
sudo apt-get install sqlite3 libsqlite3-dev
