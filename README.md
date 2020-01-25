<p align="center">
  <img src="https://i.imgur.com/CyxC7a4.jpg" alt="Logo"></img>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/QTechOfficial/OpenPeripherals" alt="License">
  <img src="https://img.shields.io/travis/QTechOfficial/OpenPeripherals" alt="Build Status">
  <img src="https://img.shields.io/github/release-date/QTechOfficial/OpenPeripherals" alt="Release">
  <br>
  <img src="https://img.shields.io/github/contributors/QTechOfficial/OpenPeripherals" alt="Contributors">
  <img src="https://img.shields.io/github/commit-activity/m/QTechOfficial/OpenPeripherals" alt="Commits per month">
  <img src="https://img.shields.io/github/last-commit/QTechOfficial/OpenPeripherals" alt="Last commit">
</p>

<h3 align="center">An open source program to control your peripherals written in Python.</h3>

<!-- 
Screenshots will go here!
--!>

OpenPeripherals is an open source driver and frontend for controlling peripherals with special features such as RGB that aims to replace and unify 3rd party software into a crossplatform, easy to use interface.

Currently OpenPeripherals only supports Linux, but Windows support is currently being worked on.

## Getting Started
### Linux:

**Dependencies:**

You will need the following packages from your distro's package manager:
- python (v3.6+)
- pip for python3

| **Distro**    | **Command**                            |
|---------------|----------------------------------------|
| Ubuntu/Debian | `sudo apt install python3 python3-pip` |
| Arch/Manjaro  | `sudo pacman -S python python-pip`     |

In addition, you will need the following packages from pip:
- hidapi
- pyqt5
- pydbus

**Installation:**
To install, simply clone the repository using git.

`git clone https://github.com/QTechOfficial/OpenPeripherals.git`

## Hardware Support
If your device is not on here, please submit a pull request!

**Supported devices:**
- Redragon
  * K556
  * K552

**WIP devices:**
- ASUS Aura (SMBus only)

**Currently unsupported devices:**
- ASUS Aura (USB)
