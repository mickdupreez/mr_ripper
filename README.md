
  

# ![](https://i.imgur.com/kle7CYE.jpeg)![](https://img.shields.io/github/last-commit/mickdupreez/mr_ripper?style=for-the-badge)

  

  

## Mr Ripper is a DVD ripping and transcoding program that allows you to easily add your DVD movies to your media collection. It also retrieves movie info and posters from IMDB. The program has a user-friendly GUI and is a useful tool for movie enthusiasts. Give it a try!

  

  

  

# ![](https://i.imgur.com/4npssPG.jpeg)
# Description
### What the script can do and why you need it. 
This scrip was written for the purpous of simplifying and streamlineing the whole process of digitizeing a DVD collection, with all the steps involved it can be time consumeing and repetative

instead of opening 2 - 3 diffrent programs all with diffrent settings and configuration each time you insert a new dvd, run this script it will simplify the process by implementing the following automations.
- Automatically RIP your DVDs to a directory on your PC with 0 input buttons or settings.
- Automatically Transcode the file if it is over a certain size "20GB" default.
- Automatically gets the correct Movie title and Poster art work.
- Automatically places the movie in a folder with the correct movie name with the poster art.
### The whole idea is
- Run the script.
- Insert a DVD into the drive.
- Insert a new DVD when that one gets ejected
- Done
Everything else is done for you.
# Getting started.
## Steps that need to be completed before the script will run on your PC

 1. Install the latest version of Python,  you can verify that Python is installed by opening a command prompt and typing "python --version".
 2. Install the required Python libraries to make the script work.
 3. Install the latest version of MakeMKV on your PC.
 4. Install the latest version of Google Chrome on your PC
 5. Make Sure you have a compatible DVD drive attached to your PC
 6. Download and Run The Mr Ripper Script


## Step 1
  ### To install the latest version of Python on a Windows PC, follow these steps:
-   Go to the official Python website (https://www.python.org/)
-   Click on the `Downloads` tab.
-   Click on the link for the `latest version of Python`.
-   Click on the `Windows` icon to download the Python installer for Windows.
-   Once the download is complete, `double-click` on the downloaded file to start the installation.
-   Follow the prompts to install Python on your PC. `Make sure to check the box to add Python to your PATH environment variable`.
-   Once the installation is complete, you can verify that Python is installed by opening a command prompt and typing "python --version". This should display the version of Python that you just installed.

## Step 2
### Required libraries :

-   `BeautifulSoup` (`bs4`)
-   `Pillow`
-   `makemkv`
-   `googlesearch`
-   `selenium`

#### Copy and paste this command into a terminal, this will install the above required libraries.
```bash

pip install bs4 Pillow makemkv googlesearch selenium

```

## Step 3
### To install MakeMKV on your PC, follow these steps:

- Go to the official MakeMKV website ([https://www.makemkv.com/](https://www.makemkv.com/))
- Click on the "Download" tab.
- Scroll down to the "MakeMKV for Windows" section.
- Click on the link to download the latest version of MakeMKV for Windows.
- Once the download is complete, double-click on the downloaded file to start the installation.
- Follow the prompts to install MakeMKV on your PC.
- Once the installation is complete, you can launch MakeMKV from the Start menu or by double-clicking on the MakeMKV shortcut on your desktop.
#### Please note! MakeMKV is free to you but you need to update your `key` when it expires.

> `These steps only need to be completed if your key has expired`

-  Get your new key from `https://forum.makemkv.com/forum/viewtopic.php?t=1053`
- Open MakeMKV from the start menu, then click on `help` "top left".
- Click on `Register`, paste the new key in here and click `OK`

## Step 4
### To install Google Chrome, the latest version on your PC, follow these steps:

-  Go to the Google Chrome download page ([https://www.google.com/chrome/](https://www.google.com/chrome/)) and click the "Download Chrome" button.
-  Once the download is complete, open the downloaded file and click "Run" to begin the installation process.
-  Follow the prompts to install Google Chrome on your PC. This may include agreeing to the terms of service and selecting the installation location.
-  Once the installation is complete, you can launch Google Chrome from the Start menu or from the shortcut on your desktop.
-  If you encounter any issues during the installation process, you can consult the Google Chrome documentation or contact the Google Chrome support team for assistance.

## Step 5
### It is hard to say if your drive is compatible. Here is a list of drives that have been tested:
-  Please read https://forum.makemkv.com/forum/viewtopic.php?f=16&t=19634 for a better guide
-  BP60NB10, UHD Official External Slim 9.5mm USB 2.0 | Rip speed 6x BD 66 ~45 mins BD 100 ~1 hour 5mins  
-  BP50NB40, UHD Officialish External Slim 9.5mm USB 2.0 | Rip speed 6x BD 66 ~45 mins BD 100 ~1 hour 5mins  
-  LG WH16NS60, UHD Official Internal 5.25 sata | Rip speed 8x BD 66 ~45 mins BD 100 ~1 hour  
-  LG BU40N, UHD Official Internal Slim Sata 9.5mm | Rip speed 6x BD 66 ~45 mins BD 100 ~1 hour 5mins  
-  LG WH14NS40, UHD Friendly Internal 5.25 sata | Rip speed 8x BD 66 ~45 mins BD 100 ~1 hour if flashed properly other wise 6x rips speed and slower then BU40N  
-  LG WH16NS40, UHD Friendly Internal 5.25 sata | Rip speed 8x BD 66 ~45 mins BD 100 ~1 hour if flashed properly other wise 6x rips speed and slower then BU40N  
-  ASUS BW-16D1HT, UHD Friendly Internal 5.25 sata | Rip speed 8x BD 66 ~45 mins BD 100 ~1 hour  
-  ASUS BW-16D1HT Pro, UHD Friendly Internal 5.25 sata | Rip speed 8x BD 66 ~45 mins BD 100 ~1 hour  
-  LG BH16NS55, UHD Friendly Internal 5.25 sata | Rip speed 8x BD 66 ~45 mins BD 100 ~1 hour if flashed properly other wise 6x rip speed and slower then BU40N  
-  Buffalo BRUHD-PU3-BK, UHD Official, External Slim 9.5mm USB 3.0 LG BU40N inside| Rip speed 6x BD 66 ~45 mins BD 100 ~1 hour 5mins  
-  Archgon MD-8107S-U3-UHD, UHD Official, External Slim 9.5mm LG BU40N inside USB 3.0-Marty| Rip speed 6x BD 66 ~45 mins BD 100 ~1 hour 5mins

## Step 6

### To download the zip file for the Mr Ripper program from GitHub, follow these steps:

1.  Go to the following link: [https://github.com/mickdupreez/mr_ripper](https://github.com/mickdupreez/mr_ripper)
2.  Click on the green "Code" button, then click on the "Download ZIP" button.
3.  Save the zip file to a location on your PC, such as your desktop or a folder in your documents.

To extract the zip file and place the program in a directory where you want to store your movie collection, follow these steps:

1.  Locate the zip file on your PC and right-click on it.
2.  Select "Extract All" from the menu.
3.  In the "Extract Compressed (Zipped) Folders" window, click on the "Browse" button and select the directory where you want to store your movie collection.
4.  Click on the "Extract" button to extract the zip file to the selected directory.

To open and run the Mr Ripper program, follow these steps:

1.  Open the directory where you extracted the Mr Ripper program. 
2.  Open a terminal here by right clicking in the directory then selecting open in terminal, alternatively you can open a terminal and type `cd "the location of the directory where you extracted the Mr Ripper program" this will take you to the directory.
3. Then finally type the following command to run the script

```bash
python Mr_Ripper_v2.0.py
```

