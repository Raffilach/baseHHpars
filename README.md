<p align="center"> <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Ga+Maamli&duration=2000&pause=1000&color=CB17C4&background=FFFFFF00&center=true&vCenter=true&random=false&width=435&lines=README+%D0%BA+%D0%9F%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D1%83+%D0%BF%D0%BE+%D0%BF%D0%B0%D1%80%D1%81%D0%B8%D0%BD%D0%B3%D1%83+HH.ru;README+for+the+HH.ru+Parsing+Project;Zabrodivshiy+Kivi" alt="Typing SVG" /></a> </p>

<p><H3> <a href = "#RU">RU</a> / <a href = "#EN">EN</a> </H3></p>

<p><a id="RU">ЭТО СТАРАЯ ВЕРСИЯ ПРОЕКТА В СКОРОМ ВРЕМЕНИ БУДЕТ ДОБАВЛЕНО ОБНОВЛЕНИЕ </p>

<p><a id="RU">Всем привет! </p>

<p>Содержание:</p>
<a href = "#esse">1 - Суть проекта</a>
<a href = "#files">2 - Рассказ про файлы</a>
<a href = "#csv">3 - Пояснение к CSV</a>
<a href = "#new1">4 - Обновление 06.07.2024</a>
<a href = "#stat">5 - Статус проекта</a>


<p>_____________________________________________________________ </p>

<p id = "esse" >Главная суть этого скрипта - добывать нужные нам данные о вакансиях с сайта hh.ru для дальнейшего анализа полученных данных. </p>

<p>Так как нам не получилось получить api самого hh из-за бюрократических проблем (скажем так), пришлось придумывать способы обхода данной неурядицы. </p>

<p>С собственно способом вы можете сами познакомиться, код тут есть. </p>

<p>_____________________________________________________________ </p>
 
<p id = "files">Сейчас расскажу немного про файлы, которые тут есть. </p>

<p>Ну, самый основной файл в этом проекте - EXvacOFF.txt, в нем вы можете увидеть пример одной вакансии со страницы, которую мы используем для получения данных (Нужно для представления о том, как устроена страница откуда мы берем в целом информацию) </p>

<p>Далее, на втором месте у нас стоит - cityCode.txt, в нем коды всех доступных 9652 городов, которые есть на hh.ru (приятного поиска своего города). </p>

<p>Почетное, третье место, у нас занимает csv файл, который мы получаем после работы программы (если будете запускать через PyCharm, не пугайтесь, что файл не появляется сразу после выведения надписи, о том, что он сохранен, не обновился проект просто) </p>

<p>Четвертое место занимает файл - timeCreate. Суть его работы в том, что-бы каждый заданный промежуток времени он проходился по всем вакансиям и если вакансия до сих пор открыта или не имеет данных о актуальности, он проверяет ее статус, в случает если на закрылась, она получает статус "Открыта", в отрицательном случает она получает статус "Закрыта".</p>

<p>Ну и наконец, сам скрипт (headPars), о нем не знаю чо сказать, он есть и уже хорошо :) </p>

<p>_____________________________________________________________ </p>

<p id = "csv">Про строку с рублевой зарплатой в csv, там есть много вакансий с отличными от рубля валютами, а также разным оформлением зарплаты, но для хорошего анализа, нам нужно структурировать эту информацию к одному значению. </p>

<p>Поэтому мы берем, там, где одна циферка, запоминаем ее, если там, где “10000000 - 40000000 UZS” мы вычисляем среднее значение и запоминаем его, ну и получившийся результат приводим к рубликам. (можно так же создать несколько других колонок в csv, для приведения в различные валюты, но для нашего проекта это, наверное, слишком </p>

<p>_____________________________________________________________ </p>

<p id = "new1">После нового обновления (06.07.2024), мы можете заметить, что названия файлов в коде заменены на <Your_file_name.csv>.
Это нужно для лучшей ориентации в коде при просмотре и его анализе.
Само название файла по моей задумке должно выглядеть следующем образом "<Ваше_название_файла>_<Дата_начала_работы_скрипта в формате(2024-06-15)>.csv". 
А так-же заметить новый файл timeCreate - который нужен для актуализации данных о актуальности вакансий.</p>

<p>_____________________________________________________________ </p>

<p id = "stat">!!!Проект пока в заработке!!!</p>

<p>_____________________________________________________________ </p>
<p>_____________________________________________________________ </p>
<p>_____________________________________________________________ </p>

<p><h3 id="EN">Hello everyone!</h3></p>

<p>Contents:</p>
<a href = "#esse.2">1 - The essence of the project</a>
<a href = "#files.2">2 - A story about files</a>
<a href = "#csv.2">3 - Explanation of CSV</a>
<a href = "#new1.2">4 - Update 07/06/2024</a>
<a href = "#stat.2">5 - Project status</a>

<p>_____________________________________________________________</p>

<p id = "esse.2">The main purpose of this script is to extract the necessary data about job vacancies from the hh.ru website for further analysis.</p>

<p>Since we couldn't get the hh API due to bureaucratic issues (so to speak), we had to come up with ways to circumvent this obstacle.</p>

<p>You can familiarize yourself with the method itself, the code is here.</p>

<p>_____________________________________________________________</p>

<p id = "files.2">Now, let me tell you a bit about the files available here.</p>

<p>Well, the most important file in this project is EXvacOFF.txt, in which you can see an example of a job vacancy from the page we use to get the data (needed to understand how the page from which we generally get information is structured).</p>

<p>Next, in second place, we have cityCode.txt, which contains the codes of all available 9,652 cities listed on hh.ru (happy searching for your city).</p>

<p>In third place of honor, we have the CSV file that we get after the program runs (if you run it through PyCharm, don't be alarmed if the file doesn't appear immediately after the message that it has been saved, the project just hasn't refreshed yet).</p>

<p>The fourth place goes to the timeCreate file. Its purpose is to check each job vacancy at specified intervals to see if it is still open or if there is no information about its relevance, and update its status accordingly: if it's still open, it gets the status "Open," otherwise, it gets the status "Closed."</p>

<p>And finally, the script itself (headPars), about which I don't know what to say, it exists, and that's good enough :)</p>

<p>_____________________________________________________________</p>

<p id = "csv.2">Regarding the line with the salary in rubles in the CSV, there are many vacancies with currencies other than rubles, as well as different salary formats, but for proper analysis, we need to structure this information into a single value.</p>

<p>Therefore, we take a single number, remember it, if it says “10000000 - 40000000 UZS,” we calculate the average value and remember it, and then convert the resulting amount to rubles. (We can also create several other columns in the CSV to convert to different currencies, but for our project, this is probably too much).</p>

<p>_____________________________________________________________</p>

<p id = "new1.2">After the new update (07/06/2024), you might notice that file names in the code have been replaced with <Your_file_name.csv>.
This is for better orientation in the code during review and analysis.
The file name itself should look like this "<Your_file_name>_<Script_start_date in format(2024-06-15)>.csv".
You will also notice a new file, timeCreate, which is needed to update the relevance of the job vacancies.</p>

<p>_____________________________________________________________</p>

<p id = "stat.2">!!!The project is still in development!!!
</p>
