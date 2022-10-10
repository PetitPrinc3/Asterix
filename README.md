# Asterix : Automated Sanitizing Terminal with Embedded Relevant Information eXtraction

![Asterix](Images/banner.png)

## What is this repo ?

This project will be in active development from the 22nd of August 2022 until at least the 10th of November 2022.  
The ultimate goal is to propose an Open-Source USB malware cleaner kiosk that is portable and offers good functionalities.

This is my graduation project from the French Naval Academy, in collaboration with the Informatic Institute of the University of Amsterdam.

You will find here the pieces of software that make Asterix as well as the report concerning the project one redacted.  
You will also find functionnalities that have not been implemented but were part of the thinking/designing process.

## The project



#### System Components

- ✅ [Frontend](Frontend) :
    - [USB Handler](Frontend/USBHandler)
    - [Pyrate](https://github.com/G4vr0ch3/PyRATE)
    - [Pyrate Automation](Frontend/PyrateAutomation/)
- ✅ [Backend](Backend)
    - [USB Handler / Identification](Backend/USBHandler)
    - [USB to USB transfer](#)
- ✅ [Analysis Center](AC-Center)
    - [Virtual Machine](#)
    - [USB to VM transfer](#)
    - [Anti-Virus Analysis Wrapper PyWAVA](https://github.com/G4vr0ch3/PyWAVA)
    - [Pywava Automation](AC-Center/PywavaAutomation/)
- ❌ [Brain](Brain)
    - [Reset handler](#)
    - [MAIN](#)
- ❌ [Host](Host)
    - [Start launcher](#)
    - [UDEV Rules](#)

| ![](Images/arch_and_op.png) |
| :-: |
| System's architecture |


#### Project Status

| Item | Status | Completion | Comment |
| :-: | :-: | :-: | :-: |
| Frontend | :green_circle: | 100% | Done. |
| Backend | :green_circle: | 100% | Gave up on drive formatting. |
| AC-Center (ARM) | :yellow_circle: | 99% | SSH Identity. |
| AC-Center (x64) | :hourglass: | 0% |  |
| Brain | :green_circle: | 100% | Implementing ssh interraction with other containers ? |
| Host | :orange_circle: | 50% | Main soft/Hardening/GUI. |
| Installer | :orange_circle: | 70% |  |
| Hardware | :orange_circle: | 75% | Case. |
| [Website](https://g4vr0ch3.github.io/Asterix) | :orange_circle: | 15% | Under construction |

| ![](Images/status.png) |
| :-: |
| Detailed status |

## Contributing to the project

We will gladly accept any valuable input !  
Should you have any remarks, advice or whatever you deem useful to us, please contact me either via:

> [e-mail](mailto:gavrochebackups@gmail.com)  
> [Discord](https://discordapp.com/users/Gavroche#2871)  
> [Twitter](https://twitter.com/Gvrch3)

Many thanks !

##

[Gavroche](https://github.com/G4vr0ch3)
