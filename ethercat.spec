#----------------------------------------------------------------------------
#
#  $Id$
#
#  Copyright (C) 2006-2010  Florian Pose, Ingenieurgemeinschaft IgH
#
#  This file is part of the IgH EtherCAT Master.
#
#  The IgH EtherCAT Master is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License version 2, as
#  published by the Free Software Foundation.
#
#  The IgH EtherCAT Master is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with the IgH EtherCAT Master; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#  ---
#
#  The license mentioned above concerns the source code only. Using the
#  EtherCAT technology and brand is only permitted in compliance with the
#  industrial property and similar rights of Beckhoff Automation GmbH.
#
#  vim: tw=78
#
#----------------------------------------------------------------------------

Name: ethercat
Version: 1.5.2
Release: 1

License: GPL
URL: http://etherlab.org/en/ethercat

Provides: ethercat
Source: %{name}-%{version}.tar.bz2
BuildRoot: /tmp/%{name}-%{version}

BuildRequires: %kernel_module_package_buildreqs

#----------------------------------------------------------------------------
# Main Package
#----------------------------------------------------------------------------

Summary: IgH EtherCAT Master
Group: EtherLab

%description
This is an open-source EtherCAT master implementation for Linux 2.6. See the
FEATURES file for a list of features. For more information, see
http://etherlab.org/en/ethercat.

%kernel_module_package

#----------------------------------------------------------------------------
# Development package
#----------------------------------------------------------------------------

%package devel

Summary: Development files for applications that use the EtherCAT master.
Group: EtherLab

%description devel
This is an open-source EtherCAT master implementation for Linux 2.6. See the
FEATURES file for a list of features. For more information, see
http://etherlab.org/en/ethercat.

#----------------------------------------------------------------------------

%prep
%setup

%build
%configure --enable-tty --enable-generic --enable-e100 \
    --with-linux-dir=/usr/src/linux-obj/%_target_cpu/default
make
mkdir obj
for flavor in %flavors_to_build; do
    target=obj/$flavor
    rm -rf $target
    mkdir $target
    cp -r config.h globals.h Kbuild master/ devices/ \
        examples/ tty/ include/ $target
    make -C /usr/src/linux-obj/%_target_cpu/$flavor modules M=$PWD/$target
done

%install
for flavor in %flavors_to_build; do
	md5sum obj/$flavor/Module.symvers
done
make DESTDIR=${RPM_BUILD_ROOT} install
for flavor in %flavors_to_build; do
    target=obj/$flavor
    make -C /usr/src/linux-obj/%_target_cpu/$flavor modules_install \
        M=$PWD/$target INSTALL_MOD_PATH=${RPM_BUILD_ROOT} \
        INSTALL_MOD_DIR=ethercat
done

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc AUTHORS
%doc COPYING
%doc COPYING.LESSER
%doc ChangeLog
%doc FEATURES
%doc INSTALL
%doc NEWS
%doc README
%doc README.EoE
/etc/init.d/ethercat
/etc/sysconfig/ethercat
/usr/bin/ethercat
/usr/lib/libethercat.so*

%files devel
%defattr(-,root,root)
/usr/include/*.h
/usr/lib/libethercat.a
/usr/lib/libethercat.la

#----------------------------------------------------------------------------
