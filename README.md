# System Programming and OS Administration

This repository contains the laboratory works for the course "System Programming and OS Administration".
---

## 📁 Lab 1 — Bash script to count files in /etc 

**Objective:** Create a bash script that counts the number of files in /etc. 

### File
- `count_files.sh` — The script, including root privilege check.  

```bash
#!/bin/bash
if [ "$(id -u)" -ne 0 ]; then 
    echo "root permissions required"
    exit 1
fi

count=$(find /etc -type f | wc -l)

echo "The amount of files in /etc/ is: $count"
```

### Execution

```bash
sudo ./count_files.sh
# The amount of files in /etc/ is: 1679
```

---

## 📁 Lab 2 — RPM Package

**Objective:** Package the script from Lab 1 (`count_files.sh`) into an RPM package using Fedora Docker container.
- RPM package was built and tested inside a Docker container

### Prepare files on host

- `count_files.sh` — bash script to count files in `/etc`
- `count_files.tar.gz` — tarball with the script (sources for the package)
- `count_files.spec` — RPM spec file containing package metadata, build instructions, and installation paths

### Start Fedora Docker container

```bash
docker run -it -v $(pwd):/mnt fedora:latest bash
```

> Mounts the current host folder to /mnt inside the container.

## Inside the container

### Install RPM build tools

```bash
dnf install -y rpm-build
```

### Create RPM build directories

```
mkdir -p /root/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
```
### Copy files to the build environment
```bash
cp /mnt/count_files.tar.gz /root/rpmbuild/SOURCES/
cp /mnt/count_files.spec /root/rpmbuild/SPECS/
```
### Build the RPM package
```bash
rpmbuild -bb /root/rpmbuild/SPECS/count_files.spec
```
> The resulting RPM is located in:
``` 
/root/rpmbuild/RPMS/noarch/
```

### Copy the RPM back to host
```bash
cp /root/rpmbuild/RPMS/noarch/*.rpm /mnt/
```
> On the host, `count_files-1-1.noarch.rpm` is ready for installation and testing.

---
### Verify the package
Inside the container or after installing on the host:
```bash
rpm -ql count_files-1-1
count_files
```
- Expected output 
```bash
/usr/local/bin/count_files
```
> Installed path may vary depending on spec configuration.
### Execute the script 
```bash
count_files
```
- Expected output
```bash
The amount of files in /etc/ is: <number>
```
> The number may differ depending on the environment (container vs full host OS).

---


## 📁 Lab 3 — DEB Package

**Objective:** Package the Lab 1 script  (`count_files.sh`)  into a DEB package.

### Package structure

```
count-files-deb/
    DEBIAN/
        control
    usr/
        bin/
            count_files
```

### Commands for package creation and installation

1) **Creating package directories**

```bash
mkdir -p count-files-deb/DEBIAN
mkdir -p count-files-deb/usr/bin
```

2) **Creating the script and making it executable**

```bash
nano count-files-deb/usr/bin/count_files
chmod +x count-files-deb/usr/bin/count_files
```

- Content of `count_files` (Lab 1):

```bash
#!/bin/bash
if [ "$(id -u)" -ne 0 ]; then 
    echo "root permissions required"
    exit 1
fi

count=$(find /etc -type f | wc -l)

echo "The amount of files in /etc/ is: $count"
```

3) **Creating the control file**

```bash
nano count-files-deb/DEBIAN/control
```

Content of `control`:

```
Package: count-files
Version: 1.0
Section: utils
Priority: optional
Architecture: all
Installed-Size: 4
Maintainer: Maryna <maryna@example.com>
Description: Bash script that counts files in /etc
Depends: bash
```

4) **Building the package**

```bash
dpkg-deb --build count-files-deb
```

- After execution. the`count-files-deb.deb` file will appear.

5) **Installation and verification**

```bash
sudo dpkg -i count-files-deb.deb
sudo count_files
```

**Expected output:**

```
The amount of files in /etc/ is: 1679
```

> The script was successfully executed with root privileges and counted the number of files in `/etc`.

---
