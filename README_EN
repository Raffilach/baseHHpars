Hello everyone!

_____________________________________________________________

The main purpose of this script is to extract the necessary data about job vacancies from the hh.ru website for further analysis.

Since we couldn't get the hh API due to bureaucratic issues (so to speak), we had to come up with ways to circumvent this obstacle.

You can familiarize yourself with the method itself, the code is here.

_____________________________________________________________

Now, let me tell you a bit about the files available here.

Well, the most important file in this project is EXvacOFF.txt, in which you can see an example of a job vacancy from the page we use to get the data (needed to understand how the page from which we generally get information is structured).

Next, in second place, we have cityCode.txt, which contains the codes of all available 9,652 cities listed on hh.ru (happy searching for your city).

In third place of honor, we have the CSV file that we get after the program runs (if you run it through PyCharm, don't be alarmed if the file doesn't appear immediately after the message that it has been saved, the project just hasn't refreshed yet).

The fourth place goes to the timeCreate file. Its purpose is to check each job vacancy at specified intervals to see if it is still open or if there is no information about its relevance, and update its status accordingly: if it's still open, it gets the status "Open," otherwise, it gets the status "Closed."

And finally, the script itself (headPars), about which I don't know what to say, it exists, and that's good enough :)

_____________________________________________________________

Regarding the line with the salary in rubles in the CSV, there are many vacancies with currencies other than rubles, as well as different salary formats, but for proper analysis, we need to structure this information into a single value.

Therefore, we take a single number, remember it, if it says “10000000 - 40000000 UZS,” we calculate the average value and remember it, and then convert the resulting amount to rubles. (We can also create several other columns in the CSV to convert to different currencies, but for our project, this is probably too much).

_____________________________________________________________

After the new update (07/06/2024), you might notice that file names in the code have been replaced with <Your_file_name.csv>.
This is for better orientation in the code during review and analysis.
The file name itself should look like this "<Your_file_name>_<Script_start_date in format(2024-06-15)>.csv".
You will also notice a new file, timeCreate, which is needed to update the relevance of the job vacancies.

_____________________________________________________________

!!!The project is still in development!!!
