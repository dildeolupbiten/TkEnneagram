# TkEnneagram

**TkEnneagram** is a Python program that calculates the Enneagram scores of the astrological results that are calculated from the values that are entered by users. The program uses a json file that includes the enneagram scores that is prepared by [Sjoerd Visser](https://vissesh.home.xs4all.nl/).

## Availability

Windows, Linux and MacOSX

## Dependencies

In order to run **TkEnneagram**, at least [Python](https://www.python.org/)'s 3.6 version must be installed on your computer. Note that in order to use [Python](https://www.python.org/) on the command prompt, [Python](https://www.python.org/) should be added to the PATH.

The program has several requirements. But users don't need to install them manually. The requirements will be installed automatically when the program first runs.

## Usage

**1.** Run the program by writing the below to **cmd** for Windows or to **bash** for Unix.

**For Unix**

    python3 run.py

**For Windows**

    python run.py
    
**Note:** For Windows, users also can run the program by double-clicking to the batch file.

**2.** The users should fill all the entries as shown in the image below.

![img1](https://user-images.githubusercontent.com/29302909/92821314-9b74e600-f3d3-11ea-9d10-4e90b0fbb1a4.png)

**3.** The geocoding service needs an internet connection. To get the coordinates of a place, users should press **Enter** and/or **Return** key. Sometimes the Geocoding Service may not respond and the program raises a messagebox like below. In this case, it's recommended to close this messagebox and try again.

![img2](https://user-images.githubusercontent.com/29302909/92814219-84ca9100-f3cb-11ea-9290-7af50b571c8b.png)

**4.** After pressed to **Enter**, if the entered value is a valid place, a drop-down menu is opened under the place entry. Users can select the country from this list.

![img3](https://user-images.githubusercontent.com/29302909/92821307-99ab2280-f3d3-11ea-8d41-4b4c5ec73208.png)

**5.** After the selection, the latitude and longitude values of this place are inserted to the related entries. The state of the latitude and longitude entries are readonly.

![img4](https://user-images.githubusercontent.com/29302909/92821311-9adc4f80-f3d3-11ea-8c67-735bb42abc34.png)

**6.** If all the entries are filled as described above, users could the **Calculate** button. And short after a window like below is created.

![img5](https://user-images.githubusercontent.com/29302909/92814222-85fbbe00-f3cb-11ea-84cf-f2f50fd220ea.png)

**7.** By clicking to the **Export** button, users can export the results into a spreadsheet file like below.

![img6](https://user-images.githubusercontent.com/29302909/92814215-83996400-f3cb-11ea-99a5-c154f7012f07.png)

## Licenses

**TkEnneagram** is released under the terms of the **GNU GENERAL PUBLIC LICENSE**. Please refer to the **LICENSE** file.
