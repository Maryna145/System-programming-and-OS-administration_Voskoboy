Name: count_files
Version: 1
Release: 1
Summary: Script that counts files in /etc
License: GPL
Source0: count_files.tar.gz
BuildArch: noarch

%description
This package installs script that counts files in /etc.

%prep

%setup -q -c -T
tar -xzf %{SOURCE0} -C .


%build

%install
install -Dm0755 count_files.sh %{buildroot}/usr/local/bin/count_files

%files
/usr/local/bin/count_files

%clean
rm -rf %{buildroot}
