---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Before opening a new issue**
Install the latest `bearhub-git` package from AUR and check if the unexpected behavior is happening there as well.
Otherwise, install from source:
```
git clone https://github.com/spalencsar/bearhub.git --depth=1
cd bearhub
python3 -m venv venv
venv/bin/pip install pip --upgrade
venv/bin/pip install setuptools --upgrade
venv/bin/pip install -r requirements.txt
venv/bin/pip install .
venv/bin/bearhub  # or venv/bin/bearhub-tray
```
 
**Describe the bug**
A clear and concise description of what the bug is.

**Software Environment**
Bearhub version: 
O.S: name and version 
Python version:
Installation method: pip | distro package manager (e.g: pacman)


P.S: these instructions and the template must be respected, otherwise your issue will be closed.