# TkEnneagram

**TkEnneagram** is a Python program that calculates the Enneagram scores of the astrological results that are calculated from the values that are entered by users and from the records that are stored in [Astro-Databank](https://www.astro.com/astro-databank/Main_Page). Because of the license conditions, [Astro-Databank](https://www.astro.com/astro-databank/Main_Page) can not be shared with third party users. Therefore those who are interested in using this program with [Astro-Databank](https://www.astro.com/astro-databank/Main_Page), should contact with the webmaster of [Astrodienst](http://www.astro.com) to get a license. The program uses a json file that includes the enneagram scores that is prepared by [Sjoerd Visser](https://vissesh.home.xs4all.nl/). 

After downloading the program, users should see the below files and folders in the main directory of the program.

![img1](https://user-images.githubusercontent.com/29302909/96911963-4506c700-14aa-11eb-87e4-33aeba62c3a5.png)

## Availability

Windows, Linux and macOS

## Dependencies

In order to run **TkEnneagram**, at least [Python](https://www.python.org/)'s 3.6 version must be installed on your computer. Note that in order to use [Python](https://www.python.org/) on the command prompt, [Python](https://www.python.org/) should be added to the PATH. There is no need to install manually the libraries that are used by the program. When the program first runs, the necessary libraries will be downloaded and installed automatically.

## Usage

**1.** Run the program by writing the below to **cmd** for Windows or to **bash** for Unix.

**For Unix**

    python3 run.py

**For Windows**

    python run.py
    
**Note:** In order to run the program, Windows users could double click the `run.bat` file.

**Note:** When the program first run in Windows, users might get a [PermissionError](https://docs.python.org/3/library/exceptions.html#PermissionError)  during the installation of [Pyswisseph](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyswisseph) library unless they run **cmd** as Administrator.

**2.** Short time later users should see a window which is similar to below.

![img2](https://user-images.githubusercontent.com/29302909/96912540-3076fe80-14ab-11eb-87f6-913aef1b6562.png)

**3.** By default there's no folder called **Database**. If users come to the **Database** menu cascade then click the **Open** menu button, an empty folder called **Database** would be created in the main directory of the program. Users should move the **XML** file that they obtained to this folder. And if the users click the **Open** menu button for the second time, a window as below would occur.

![img3](https://user-images.githubusercontent.com/29302909/96887895-b2f0c580-148d-11eb-91ae-d730a4735fe1.png)

Users can move many databases to the **Database** folder and select the database you want to work with. The above window is only destroyed when the users press the **Apply** button.

After pressed the **Apply** button, the Enneagram types of the records would be calculated and these types would be added as the new items of the records. 

![img4](https://user-images.githubusercontent.com/29302909/96914184-56050780-14ad-11eb-8c5a-09b8e13d66a2.png)

After the calculation is completed, a JSON file would be created in the **Database** folder. The filename would include the name of the XML file + the algorithm that is used. For example, if the name of the XML file is **adb_export_200814_1910.xml** and the name of the used algorithm is **2010_Algorithm_Placidus.json**, the name of the derived database would be **adb_export_200814_1910_2010_Algorithm_Placidus.json**. And users could select this file. Also users could use this file with [TkAstroDb](https://github.com/dildeolupbiten/TkAstroDb). If users select this JSON file instead the XML file, the calculation would no longer be done again. That's why it's recommended that users would load this derived database to the program after it's created.

**4.** A new frame should cover the main window as below in a few seconds after the calculation is completed.

![img5](https://user-images.githubusercontent.com/29302909/96915097-8600da80-14ae-11eb-9888-520e66c8d08e.png)

**5.** If users want to add records manually to the displayed records, they should type the name of the record in the combobox. For example suppose a user wants to add **Albert Einstein** to the displayed records, the user could write **einstein** or a keyword that the program could find to the **Search A Record By Name** section, then if users press **Enter** key, a list of records that contains **einstein** characters would be inserted to the combobox and a drop-down menu would be popped. Users can select the found records from this drop-down menu via clicking to the arrow of the combobox. After selecting the record, a new button called **Add** is created as below.

![img6](https://user-images.githubusercontent.com/29302909/96916028-a8dfbe80-14af-11eb-80f5-3f2a1da8052e.png)

If users click the **Add** button, the record would be added to the treeview and the **Add** button would be destroyed. However, users can continue selecting the records from the drop-down menu. The **Add** button would be created for the next record unless the record is already in the treeview.

![img7](https://user-images.githubusercontent.com/29302909/96916033-aa10eb80-14af-11eb-9b79-69934bb74b22.png)

**6.** If a record that is inserted to the treeview is selected and users use the right-click of their mause, a right click menu would open and if they want, users could open the ADB page of the record, remove the record from the treeview and open the Enneagram scores of the record. The Enneagram scores would be displayed in a new window like below:

![img8](https://user-images.githubusercontent.com/29302909/96916444-3de2b780-14b0-11eb-9ac5-e7dff22dbc9b.png)

By scrolling the horizontal scrollbar, users could see the total scores.

![img9](https://user-images.githubusercontent.com/29302909/96916721-9e71f480-14b0-11eb-913e-8fb02fa33878.png)

The blue colored line describes the total scores. And the highest value is considered as the Enneagram Type of the person. Also the the highest neighbour of the Enneagram Type is considered as the Wing type of the person. So the ennagram and wing type of Albert Einstein is calculated as **4w5** according to 2010 Algorithm. (See [4w5](https://www.google.com/search?q=4w5) for further reading.)

Also, users could export the result into a spreadsheet file via using the **Export** button.

**7.** Users could select the categories of ADB via clicking the **Select** button near the **Categories** label. There are two ways of selecting the categories: One is the **Basic** category selection method which is coming by default and a window as below would open if the selection method is **Basic**.

![img10](https://user-images.githubusercontent.com/29302909/96892541-68257c80-1492-11eb-904e-f79b9cc9bf21.png)

Users could search a category by writing somethings to the search entry. If the characters that users typed match with the characters of the categories in the category list, the horizontal scrollbar would move to the category that contains the characters. And if users press the **Enter** key, the program would move to the positions of other categories that contain the characters.

In order to select a category, users should use the right-click of the mause and select the **Add** option. The color of the added category would turn to red. Users could select all the categories by using `CTRL-A`, then the selected categories should be added.

In order to apply the selections, users should click the **Apply** button.

The other category selection method is called as **Advanced**. Users could change the category selection method via coming to the **Options** menu cascade and clicking the **Category Selection** menu. If the **Category Selection** menu button is clicked, a window as below would open.

![img11](https://user-images.githubusercontent.com/29302909/96896860-b0df3480-1496-11eb-86eb-f9ce3c3df6f5.png)

As mentioned before, by default, the **Basic** option is selected. The selected option would be valid for the next time.

If users click the **Select** button near the **Categories** after selected the **Advanced** category selection, a window as below would open.

![img12](https://user-images.githubusercontent.com/29302909/96897416-3cf15c00-1497-11eb-96f9-7189e6ba6f09.png)

The left frame is for including the categories whereas the right frame for ignoring the categories.

**8.** Users could select the [Rodden Ratings](https://www.google.com/search?&q=rodden+rating), thus only the records that have the selected Rodden Ratings would be inserted to the treeview. If users click the **Select** button near the **Rodden Rating**, a window as below would open.

![img13](https://user-images.githubusercontent.com/29302909/96898559-88583a00-1498-11eb-948e-6327ea3905f9.png)

**9.** After selected the **Categories** and the **Rodden Ratings**, users should click the **Display** button to insert the filtered records to the treeview. The inserting process may take time depending on the amount of selected categories and selected rodden ratings. After the inserting process is completed, users should receive an information message as below.

![img14](https://user-images.githubusercontent.com/29302909/96917717-e7767880-14b1-11eb-9bf8-758b505a812e.png)

Users could also filter the records using the checkbuttons which could be seen on the main window.

**10.** Before passing to the calculation process, users could select the **House System** to be used by coming to the **Options** menu cascade then clicking the **House System** menu button. 

![img15](https://user-images.githubusercontent.com/29302909/96900253-91e2a180-149a-11eb-94cb-ca6d7d7f57c2.png)

By default, the **Placidus** house system is selected. However the selected house system would be used as default for next calculations.

**11.** When users completed selecting the options they want, they can start the process of finding the observed values. In order to do that, users should come to the **Calculations** menu cascade then click the **Find Observed Values** menu button. The program would ask users to specify the year ranges to elect the records that are out of the specified range. The default numbers are the minimum and maximum year numbers of of records in the selected category.

![img17](https://user-images.githubusercontent.com/29302909/96918198-9e72f400-14b2-11eb-97fb-6db0140e2e84.png)

By pressing the **Apply** button, a new window like below would open.

![img18](https://user-images.githubusercontent.com/29302909/96918197-9d41c700-14b2-11eb-8571-795363911e4f.png)

Users could look how the distribution changes according to the time range. Also by clicking to the **Export** button, the results could be exported into a spreadsheet file. The spreadsheet file would be created in the nested directories which would be located in the main directory of the program. The name of the directories depend on the selected category, house system, checkbuttons and the values of the year range.

**12.** There's a menu button called **Add Category** under the **Database** menu cascade that is used to add the **Sun**, the **Moon**, the **Ascendant** and the **Midheaven** sign degrees as the new categories of the records. If users click this menu button, a window to select the JSON files would be opened and after selecting the file (for example the **adb_export_200814_1910_2010_Algorithm_Placidus.json** file) a calculation would be started and after the calculation is completed, the users would receive an information message and the content of the JSON file would be changed. Then the newly added categories would be available when users want to select the categories. But in order to do that, the JSON file should be loaded to the program. Below you are seeing some parts of the newly added categories after clicked the **Select** button near the **Categories**.

![img19](https://user-images.githubusercontent.com/29302909/96922565-b0579580-14b8-11eb-9bf3-8f0d8c825768.png)

**13.** Users could select the planets that would be used in the calculation process of the Enneagram Types via coming to the **Options** menu cascade and clicking the **Planets** menu button. By default, as can be seen below, all planets are selected.

![img20](https://user-images.githubusercontent.com/29302909/96923347-d467a680-14b9-11eb-93ed-1e3bbefaf3c8.png)

**14.** Users could select the algorithms that would be used in the calculation process of the Enneagram Types via coming to the **Options** menu cascade and clicking the **Algorithm** menu button. By default, as can be seen below, the default algorithm is selected as **2010_Algorithm_Placidus.json**.

![img21](https://user-images.githubusercontent.com/29302909/96923566-26103100-14ba-11eb-9a86-3aebdf703c79.png)

In order to use different algorithms, users should contact with [Sjoerd Visser](https://vissesh.home.xs4all.nl/) as he is the creator of the algorithms. He would send to users a json file which content is hashed and a key to decrypt the hashed json file. Users could use the program for the key to be written into the **defaults.ini** file. Users could change the key manually by changing the related part of the **defaults.ini** file. But also they can activate the key by opening the Enneagram Scores of a single record (not the Enneagram distribution) after the hashed algorithm is selected.

So, before using the new algorithm, users should activate the key. The steps to activate the key are as below:

- Move the JSON file that is shared by Mr. Visser to the **Database** folder.

- Click to the **Algorithm** menu button which is under the **Options** menu cascade.

- Select the new JSON file. (In my case The name of the new algorithm is written as **2012_Algorithm_Placidus.json**.)

![img22](https://user-images.githubusercontent.com/29302909/96924827-e21e2b80-14bb-11eb-98d5-90f831f7732d.png)

- Type some characters in the **Search a name** field, for example type **einstein** characters. Add one of the found records to the treeview.

- Select the record on the treeview then right click the mause and click the **Open Enneagram Scores** option. After clicked the **Open Enneagram Scores** menu button, a window like below would open.

![img23](https://user-images.githubusercontent.com/29302909/96925237-84d6aa00-14bc-11eb-87f5-38e8e92dbdea.png)

Users could write the key that is shared with them to this entry field. Then users should press to **OK** button to activate the key. If the entered key is correct, a window like below would open which means that the key is activated successfully.

![img24](https://user-images.githubusercontent.com/29302909/96925576-0b8b8700-14bd-11eb-8114-a9c63ce1d3c8.png)

Users can use the new algorithm anymore. They can create a new derived database by using the XML file and the new algorithm.

**15.** If users click the **User Entry** menu button, a window as below opens.

![img25](https://user-images.githubusercontent.com/29302909/96925940-9a989f00-14bd-11eb-97bf-735fa9112fe5.png)

Users should fill all the entries as shown in the image below.

![img26](https://user-images.githubusercontent.com/29302909/96926187-eba89300-14bd-11eb-96d3-6cf7700a95f1.png)

**16.** The geocoding service needs an internet connection. To get the coordinates of a place, users should press **Enter** and/or **Return** key. Sometimes the Geocoding Service may not respond and the program raises a warning message like below.

![img27](https://user-images.githubusercontent.com/29302909/92814219-84ca9100-f3cb-11ea-9290-7af50b571c8b.png)

In this case, it's recommended to close this messagebox and try again.

**17.** After pressed to **Enter**, if the entered value is a valid place, a drop-down menu pops under the place entry. Users could select the country from this list.

![img28](https://user-images.githubusercontent.com/29302909/96926398-2e6a6b00-14be-11eb-9d25-9782f3c00bf9.png)

After the selection, the latitude and longitude values of this place are inserted to the related entries. Users also could add the latitude and longitude values manually.

**18.** If all the entries are filled as described above, users could the **Calculate** button. And short after a window like below is created.

**Note:** Users could activate the key for 2012 algorithm via using this **User Entry Form** too.

![img29](https://user-images.githubusercontent.com/29302909/96926916-edbf2180-14be-11eb-94fc-94d7dd18a537.png)

**19.** By clicking to the **Export** button, users could export the results into a spreadsheet file.

**20.** If an update is released, users could update their program by coming to the **Help** menu cascade and clicking the **Check for updates** menu button.

**21.** If users click the **About** section which is under the **Help** menu cascade, a window like below opens and users could contact the developer using the email link written on the frame.

![img30](https://user-images.githubusercontent.com/29302909/96930339-35947780-14c4-11eb-9138-5ae0b923fe5a.png)

## Licenses

**TkEnneagram** is released under the terms of the **GNU GENERAL PUBLIC LICENSE**. Please refer to the **LICENSE** file.
