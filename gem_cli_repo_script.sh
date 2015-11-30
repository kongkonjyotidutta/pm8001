#!/bin/sh

stty -F /dev/ttyS1 speed 115200 pass8 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke time 5

echo -ne 'getboardid\r' > /dev/ttyS1

#for i in `seq 1 1`
for i in `seq 1 4100`
do
 echo "TEST_STEP $i"
 logger "TEST_STEP $i"

 echo -ne 'suppress_credit 1\r' > /dev/ttyS1
# usleep 300000
 ./fwdownloader -d 0 -cli getboardid

done


