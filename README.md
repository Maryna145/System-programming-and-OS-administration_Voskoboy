# System Programming and OS Administration

Репозиторій містить лабораторні роботи з курсу **"Системне програмування та адміністрування ОС"**.

---

## 📁 Lab 1 — Bash скрипт для підрахунку файлів у /etc

**Мета:** створити bash скрипт, який підраховує кількість файлів у `/etc`.  

### Файл
- `count_files.sh` — скрипт з перевіркою прав root.  

```bash
#!/bin/bash
if [ "$(id -u)" -ne 0 ]; then 
    echo "root permissions required"
    exit 1
fi

count=$(find /etc -type f | wc -l)

echo "The amount of files in /etc/ is: $count"
```

### Приклад виконання

```bash
sudo ./count_files.sh
# The amount of files in /etc/ is: 1679
```

---

## 📁 Lab 2 — RPM пакет

**Мета:** упакувати скрипт Lab 1 (`count_files.sh`) у RPM пакет на Ubuntu.

### Файли для пакету

- `count_files.sh` — bash скрипт для підрахунку файлів у `/etc`
- `count_files.tar.gz` — tarball зі скриптом (джерела для пакету)

### Створення структури та tarball

```bash
mkdir -p ~/rpmbuild/SOURCES ~/rpmbuild/SPECS
tar czf ~/rpmbuild/SOURCES/count_files.tar.gz count_files.sh
```

> Створюємо структуру для RPM (`SOURCES` і `SPECS`) і архівуємо скрипт.

### Збірка RPM

```bash
rpmbuild -ba ~/rpmbuild/SPECS/count-files.spec
ls ~/rpmbuild/RPMS/noarch
```

**Результат:**

```
count_files-1-1.noarch.rpm
```

> Команда `rpmbuild -ba` зібрала пакет у директорії `~/rpmbuild/RPMS/noarch`.

### Встановлення пакету

```bash
sudo rpm -i ~/rpmbuild/RPMS/noarch/count_files-1-1.noarch.rpm
```

### Перевірка скрипта

```bash
sudo count_files
```

**Вивід:**

```
The amount of files in /etc/ is: 1679
```

---

## 📁 Lab 3 — DEB пакет

**Мета:** упакувати скрипт Lab 1 (`count_files.sh`) у DEB пакет на Ubuntu.

### Структура пакету

```
count-files-deb/
    DEBIAN/
        control
    usr/
        bin/
            count_files
```

### Команди для створення і встановлення пакету

1) **Створюємо каталоги пакету**

```bash
mkdir -p count-files-deb/DEBIAN
mkdir -p count-files-deb/usr/bin
```

2) **Створюємо скрипт і робимо його виконуваним**

```bash
nano count-files-deb/usr/bin/count_files
chmod +x count-files-deb/usr/bin/count_files
```

- Вміст `count_files` (Lab 1):

```bash
#!/bin/bash
if [ "$(id -u)" -ne 0 ]; then 
    echo "root permissions required"
    exit 1
fi

count=$(find /etc -type f | wc -l)

echo "The amount of files in /etc/ is: $count"
```

3) **Створюємо control-файл**

```bash
nano count-files-deb/DEBIAN/control
```

Вміст `control`:

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

4) **Побудова пакету**

```bash
dpkg-deb --build count-files-deb
```

- Після виконання з’явиться файл `count-files-deb.deb`.

5) **Встановлення і перевірка**

```bash
sudo dpkg -i count-files-deb.deb
sudo count_files
```

**Очікуваний вивід:**

```
The amount of files in /etc/ is: 1679
```

> Скрипт успішно запущено з правами root і підраховує кількість файлів у `/etc`.

---
