#LF: This is my first spec file for pm8001 rpm

BuildRoot:              %{_tmppath}/%{name}-root
Summary: 		GNU pm8001
License: 		GPL
Name: 			pm8001
Version:                0.1.36.e5 	
Release: 		1
Source0: 		%{name}-%{release}.%{version}_src.tar.bz2
Prefix:                 /lib 
Group: 			kernel/drivers

%description
The GNU pm8001 driver build and install pm8001 SAS HBA driver to Linux kernel
%prep
%setup -c 
%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
modprobe libsas
modprobe -r pm8001
install -D pm8001.ko $RPM_BUILD_ROOT/usr/bin/pm8001.ko
install -D pm8001install $RPM_BUILD_ROOT/usr/share/doc/pm8001/pm8001install
install -D release.txt $RPM_BUILD_ROOT/usr/share/doc/pm8001/release.txt
install -D aap1img.bin $RPM_BUILD_ROOT/lib/firmware/aap1img.bin
install -D iopimg.bin $RPM_BUILD_ROOT/lib/firmware/iopimg.bin
install -D ilaimg.bin $RPM_BUILD_ROOT/lib/firmware/ilaimg.bin
install -D istrimg.bin  $RPM_BUILD_ROOT/lib/firmware/istrimg.bin
##install -D PMC\ Driver\ User\ Guide\ \(2\).pdf $RPM_BUILD_ROOT/usr/share/doc/pm8001/PMC\ Driver\ User\ Guide\ \(2\).pdf
cp pm8001.ko /lib/modules/$(uname -r)/kernel/drivers/scsi/.
modprobe libsas
insmod /lib/modules/$(uname -r)/kernel/drivers/scsi/pm8001.ko
depmod -a
modinfo pm8001

%clean
rm -rf $RPM_BUILD_ROOT

%post
modprobe -r pm8001
modprobe libsas
cp /usr/bin/pm8001.ko /lib/modules/$(uname -r)/kernel/drivers/scsi/.
rm /usr/bin/pm8001.ko
modprobe libsas
insmod /lib/modules/$(uname -r)/kernel/drivers/scsi/pm8001.ko
depmod -a
modinfo pm8001


%files
%defattr(-,root,root,-)
/usr/bin/pm8001.ko
/lib/firmware/aap1img.bin
/lib/firmware/iopimg.bin
/lib/firmware/istrimg.bin
/lib/firmware/ilaimg.bin

%doc %attr(0444,root,root) 
/usr/share/doc/pm8001/pm8001install
/usr/share/doc/pm8001/release.txt
