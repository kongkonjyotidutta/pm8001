#xyr build defines
%define _xyr_package_name     pm8001
%define _xyr_package_source   pm8001.tgz
%define _xyr_package_version  0.1.36.xrtx
%define _xyr_build_number     1
%define _xyr_pkg_url          http://svnca/WW/os-group/pm8001/trunk
#xyr end defines

#This is spec file for pm8001 rpm

# Default to build current running kernel.  To build
# for a different kernel use --define 'KVER <kernel>'
%if 0%{?!KVER:1}
%define _devrpm %(rpm -q kernel-devel | grep -v 'package kernel-devel is not installed' | /usr/lib/rpm/redhat/rpmsort -r | head -n 1)
%if %(test -z "%{?_devrpm}" && echo 0 || echo 1)
%global KVER %(rpm -q --qf '%{VERSION}-%{RELEASE}.%{ARCH}\\n' %{_devrpm} | head -n 1)
%endif
%endif

%if %(test -z "%{?KVER}" && echo 1 || echo 0)
%global KVER %(uname -r)
%endif


%{?!BUILD_VER: %{expand:
%global BUILD_VER %{?_xyr_build_number}%{?!_xyr_build_number:1}
}}

%global PKGVER %{?_xyr_package_version}%{?!_xyr_package_version:0.1.36.F07}

BuildRoot:              %{_tmppath}/%{name}-root
Summary: 		GNU pm8001
License: 		GPL
Name: 			%{_xyr_package_name}
Version:                %{PKGVER}
Release: 		%{BUILD_VER}
Source0: 		%{_xyr_package_source}
Prefix:                 /
Group: 			kernel/drivers
%{?_xyr_pkg_url:%{expand:
Url:			%_xyr_pkg_url
}}

BuildRequires:		kernel-devel

%description
The GPL pm8001 SAS HBA driver from kernel.org backported to the Linux
kernel version %{KVER} and enhanced with Xyratex additions.

%prep
%setup -c

%build
cd source
make KVER=%{KVER}

%install
cd source
# for some reason, on RHEL-5 RPM_BUILD_ROOT doesn't get set
if [ -z "$RPM_BUILD_ROOT" ] ; then
	export RPM_BUILD_ROOT="%{buildroot}" ;
fi
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
install -D pm8001.ko $RPM_BUILD_ROOT/lib/modules/%{KVER}/updates/kernel/drivers/scsi/pm8001.ko
install -D pm8001install $RPM_BUILD_ROOT/usr/share/doc/pm8001/pm8001install
install -D release.txt $RPM_BUILD_ROOT/usr/share/doc/pm8001/release.txt
install -D aap1img.bin $RPM_BUILD_ROOT/lib/firmware/pm8001/aap1img.bin
install -D iopimg.bin $RPM_BUILD_ROOT/lib/firmware/pm8001/iopimg.bin
install -D ilaimg.bin $RPM_BUILD_ROOT/lib/firmware/pm8001/ilaimg.bin
install -D istrimg.bin $RPM_BUILD_ROOT/lib/firmware/pm8001/istrimg.bin
install -D pm8001-wwn $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/pm8001-wwn

%clean
rm -rf $RPM_BUILD_ROOT

%post
# "weak modules" support
# Suse
if [ -x /usr/lib/module-init-tools/weak-modules ]; then
    rpm -ql %{name}-%{version} | grep '\.ko$' |
        /usr/lib/module-init-tools/weak-modules --add-modules
fi
# RedHat
if [ -x /sbin/weak-modules ]; then
    rpm -ql %{name}-%{version} | grep '\.ko$' |
        /sbin/weak-modules --add-modules
fi

# During a kickstart the running kernel is likely
# to be different than what we are installing so these
# will fail.
if [ -e /lib/modules/$(uname -r)/modules.dep ] ; then
   modprobe -r -q pm8001
   modprobe libsas
fi

depmod -a

if [ -e /lib/modules/$(uname -r)/modules.dep ] ; then
   modprobe pm8001
   modinfo pm8001
fi

/sbin/chkconfig --add pm8001-wwn

%preun
if [ "$1" = "0" ] ; then
	/sbin/chkconfig --del pm8001-wwn
fi
rpm -ql %{name}-%{version} | grep '\.ko$' > /var/run/%{name}-modules

%postun
if [ "$1" = "0" ] ; then
  rmmod pm8001
fi

# "weak modules" support
# Suse
if [ -x /usr/lib/module-init-tools/weak-modules ]; then
    cat /var/run/%{name}-modules | grep '\.ko$' |
        /usr/lib/module-init-tools/weak-modules --remove-modules
fi
# RedHat
if [ -x /sbin/weak-modules ]; then
    cat /var/run/%{name}-modules | grep '\.ko$' |
        /sbin/weak-modules --remove-modules
fi
depmod -a
rm /var/run/%{name}-modules

%files
%defattr(-,root,root,-)
/lib/modules/%{KVER}/updates/kernel/drivers/scsi/pm8001.ko
/lib/firmware/pm8001/aap1img.bin
/lib/firmware/pm8001/iopimg.bin
/lib/firmware/pm8001/istrimg.bin
/lib/firmware/pm8001/ilaimg.bin
%attr(0500,root,root) %{_sysconfdir}/init.d/pm8001-wwn

%doc %attr(0444,root,root) 
/usr/share/doc/pm8001/pm8001install
/usr/share/doc/pm8001/release.txt
