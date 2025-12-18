pipeline {
    agent { 
        label 'builder' 
    }

    environment {
        LAB2_DIR = "lab2"
        LAB3_DIR = "lab3"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Maryna145/System-programming-and-OS-administration_Voskoboy.git'
            }
        }

        stage('DEB: Build & Install') {
            steps {
                script {
                    echo "--- 1. Preparing Script ---"
                    sh "chmod +x ${LAB3_DIR}/count-files-deb/usr/bin/count_files"
                    
                    echo "--- 2. Building DEB Package ---"
                    sh "dpkg-deb --build ${LAB3_DIR}/count-files-deb"
                    echo "--- 3. Installing DEB Package ---"
                    sh "sudo dpkg -i --force-all ${LAB3_DIR}/count-files-deb.deb"                   
                    echo "--- 4. Testing Execution ---"
                    sh "count_files"
                }
            }
        }
        stage('RPM: Build & Install') {
            steps {
                script {
                    echo "--- Launching Fedora Container ---"
                    def dockerCmd = """
                        docker run --rm -v ${WORKSPACE}:/mnt fedora:latest /bin/bash -c '
                            echo "[Fedora] Installing tools..."
                            dnf install -y rpm-build
                            echo "[Fedora] Creating build tree..."
                            mkdir -p /root/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
                            echo "[Fedora] Copying files..."
                            cp /mnt/${LAB2_DIR}/count_files.tar.gz /root/rpmbuild/SOURCES/
                            cp /mnt/${LAB2_DIR}/count_files.spec /root/rpmbuild/SPECS/
                            echo "[Fedora] Building RPM..."
                            rpmbuild -bb /root/rpmbuild/SPECS/count_files.spec
                            echo "[Fedora] Installing RPM..."
                            rpm -ivh /root/rpmbuild/RPMS/noarch/*.rpm
                            echo "[Fedora] Executing Script..."
                            count_files
                        '
                    """
                    sh dockerCmd
                }
            }
        }
    }
}
