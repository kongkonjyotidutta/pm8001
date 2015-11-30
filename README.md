# Base version pm8001 driver Linux driver: 0.1.36-2201, Firmeware: 01.11.00.00 for Toshiba
In order to add a new version 
a) install pm8001.source.rpm
- pm8001.tgz, pm8001.spec
b) untar pm8001.tgz
c) change source/*
d) create a new tarball 
- #tar czvf pm8001.tgz source/ doc/ spec/
e) compile the new source code
# cd spec/
# rpmbuild -ba pm8001.spec
This will produce new pm8001.rpm along with new pm8001.source.rpm

To test:
a) unload the current pm8001 driver by removing the currently installed rpm package
#rpm -qa|grep pm8001
# rpm -e pm8001-1.36.rpm
This will also unload the pm8001 driver.
Install the new rpm:
# rpm -ivh pm8001-1.37.rpm
This will also load the new driver.

A note about the pm8001 firmware:
a) The firmware is contained in the same source directory under pm8001.tgz package.
b) It's version v1.11.00.00
c) The driver version is v1.36


