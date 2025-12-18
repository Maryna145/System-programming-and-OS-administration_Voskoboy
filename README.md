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
- DEB package was built and tested on Ubuntu
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

## 📁 Lab 4 — CI/CD Automation (GitHub Actions)

**Objective:** Automate the build process of RPM and DEB packages using GitHub Actions. The pipeline triggers on every push to the `main` branch.

### Workflow Configuration
- **File:** `.github/workflows/build.yml`
- **Triggers:** `push` to `main`, `pull_request` to `main`.

### Pipeline Architecture

The workflow consists of two parallel jobs:

#### 1. RPM Build (`build-rpm`)
- **Environment:** Runs inside a **Fedora 39 Docker container** (`container: fedora:39`) running on an Ubuntu host.
- **Steps:**
  - Installs `rpm-build`, `rpmdevtools`.
  - Sets up the build tree using `rpmdev-setuptree`.
  - Archives sources from `lab2/`.
  - Builds the package using `rpmbuild`.
  - Uploads the artifact directly from the `/root/rpmbuild/RPMS/`

#### 2. DEB Build (`build-deb`)
- **Environment:** Runs natively on **Ubuntu 24.04**.
- **Steps:**
  - Uses the pre-existing structure from `lab3/count-files-deb`.
  - Fixes execution permissions (`chmod +x`) to ensure the script runs correctly.
  - Builds the package using `dpkg-deb`.
  - Uploads the artifact directly from the working directory.

### Results (Artifacts)
#### The compiled packages are automatically uploaded as **GitHub Artifacts** and can be downloaded from the "Actions" tab after a successful build. 
---
## 📁 Lab 5 — Jenkins Infrastructure (Docker + SSH Agent)
**Objective:** Create a Dockerfile and docker-compose setup to run Jenkins Master and a custom Ubuntu-based Builder agent, connected securely via SSH keys.

**Files**
- `Dockerfile` — Configuration for the `jenkins-builder` image (Ubuntu 24.04 + SSH Server + Build tools).
- `docker-compose.yml` — Orchestrates both Master and Builder containers in a shared network.
- `.env` — Stores the `SSH_PUB_KEY` variable (git-ignored for security).

### 1. Security Setup (SSH Keys)
Jenkins requires the private key in the legacy PEM format (starting with `-----BEGIN RSA PRIVATE KEY-----`).

**Generate keys:**

```bash
ssh-keygen -t rsa -b 4096 -m PEM -f jenkins_key -N ""
```
> Generate RSA key in PEM format directly
### 2. Configure Environment
Create a `.env` file to inject the public key into the builder container.

```bash
nano .env
```
**Content:**
```bash
SSH_PUB_KEY=ssh-rsa AAAAB3NzaC... (copy content from jenkins_key.pub)
```

### 3. Execution
Start the infrastructure:
```bash
docker compose up -d --build
```
### 4. Jenkins Configuration
#### Add Credentials:
- Go to `Manage Jenkins` -> `Credentials`.
- Kind: SSH Username with private key.
- Paste the entire content of `jenkins_key`, including header `-----BEGIN RSA PRIVATE KEY-----` and footer `-----END RSA PRIVATE KEY-----`.
#### Add Node:
- Name: `builder`
- Remote root directory: `/home/jenkins`
- Host: `jenkins-builder`
- Launch method: Launch agents via SSH.
- Credentials: Select the key created above.
- Host Key Verification Strategy: Non verifying Verification Strategy.

### Verification
Check the node status in Jenkins UI or logs:
```bash
This is a Unix agent
Agent successfully connected and online.
```
---
## 📁 Lab 6 — Jenkins CI/CD Pipeline (Multi-OS Support)
**Objective:** Create a Jenkins Pipeline that utilizes a custom Docker Agent to build, install, and execute artifacts locally (DEB) and inside a dynamic container (RPM).

### Infrastructure Updates (Lab 5 Extension)
To support this pipeline, the infrastructure from Lab 5 was updated:

- **Dockerfile:** Added `docker.io`, `sudo`, `rpm`, and `dpkg-dev` to the agent image. Configured passwordless sudo for the `jenkins` user.

- **Docker Compose:** Mounted ё/var/run/docker.sockё to allow the agent to spawn sibling containers (Docker-in-Docker).

### Pipeline Architecture (Jenkinsfile)
The pipeline implements a hybrid build strategy:

### 1. DEB Stage (Native Ubuntu)
Executes directly on the `jenkins-builder` agent (which is Debian/Ubuntu based).

- **Steps:**
  - Prepares the script (`chmod +x`).
  - Builds the package using `dpkg-deb`.
  - Installs via `sudo dpkg -i`.
  - Executes the installed command to verify logic.

### 2. RPM Stage (Containerized Fedora)
Since the agent cannot natively install RPMs, it spawns a temporary Fedora container.

- **Method:** Uses the "Copy-Exec" pattern to handle file transfer in a Docker-in-Docker environment.
- **Steps:**
- Starts a background Fedora container (`docker run -d`).
- Copies source files (`.tar.gz`, `.spec`) into the container using `docker cp`.
- Builds the package inside via `docker exec` and `rpmbuild`.
- Installs and verifies the package inside the container.
- Cleans up (removes container).
### Execution Results
### 1. Before running, ensure the host's Docker socket is accessible:
```bash
sudo chmod 666 /var/run/docker.sock
```
### 2. The pipeline successfully verifies the script logic in two different environments simultaneously.
- **Ubuntu Agent Output:**
```bash
+ sudo count-files
The amount of files in /etc/ is: 452
```
- **Fedora Container Output:**
```bash
[Fedora] Executing Script...
The amount of files in /etc/ is: 352
```
The file count differs because the Agent is a heavier container with more tools installed, while the Fedora container is a minimal base image.

