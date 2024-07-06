Всем привет! 

_____________________________________________________________ 

Главная суть этого скрипта - добывать нужные нам данные о вакансиях с сайта hh.ru для дальнейшего анализа полученных данных. 

 
Так как нам не получилось получить api самого hh из-за бюрократических проблем (скажем так), пришлось придумывать способы обхода данной неурядицы. 

С собственно способом вы можете сами познакомиться, код тут есть. 

_____________________________________________________________ 

 
Сейчас расскажу немного про файлы, которые тут есть. 

Ну, самый основной файл в этом проекте - EXvacOFF.txt, в нем вы можете увидеть пример одной вакансии со страницы, которую мы используем для получения данных (Нужно для представления о том, как устроена страница откуда мы берем в целом информацию) 

Далее, на втором месте у нас стоит - cityCode.txt, в нем коды всех доступных 9652 городов, которые есть на hh.ru (приятного поиска своего города). 

Почетное, третье место, у нас занимает csv файл, который мы получаем после работы программы (если будете запускать через PyCharm, не пугайтесь, что файл не появляется сразу после выведения надписи, о том, что он сохранен, не обновился проект просто) 

Четвертое место занимает файл - timeCreate. Суть его работы  в том, что-бы каждый заданный промежуток времени он проходился по всем вакансиям и если вакансия до сих пор открыта или не имеет данных о актуальности, он проверяет ее статус, в случает если на закрылась, она получает статус "Открыта", в отрицательном случает она получает статус "Закрыта".

Ну и наконец, сам скрипт (headPars), о нем не знаю чо сказать, он есть и уже хорошо :) 

_____________________________________________________________ 

Про строку с рублевой зарплатой в csv, там есть много вакансий с отличными от рубля валютами, а также разным оформлением зарплаты, но для хорошего анализа, нам нужно структурировать эту информацию к одному значению. 

Поэтому мы берем, там, где одна циферка, запоминаем ее, если там, где “10000000 - 40000000 UZS” мы вычисляем среднее значение и запоминаем его, ну и получившийся результат приводим к рубликам. (можно так же создать несколько других колонок в csv, для приведения в различные валюты, но для нашего проекта это, наверное, слишком 

_____________________________________________________________ 


 
_____________________________________________________________ 

После нового обновления (06.07.2024), мы можете заметить, что названия файлов в коде заменены на <Your_file_name.csv>.
Это нужно для лучшей ориентации в коде при просмотре и его анализе.
Само название файла по моей задумке должно выглядеть следующем образом "<Ваше_название_файла>_<Дата_начала_работы_скрипта в формате(2024-06-15)>.csv". 
А так-же заметить новый файл timeCreate - который нужен для актуализации данных о актуальности вакансий.

_____________________________________________________________ 

!!!Проект пока в заработке!!!
  
