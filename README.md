# SFWpy
categorizes and gives images a NSFW evaluation

input: url or image directory<br />
output: categorized images and a NSFW evaluation and exports info to an SQLite database


SFWpy is very machine and environment-specific at the moment;
it relies on paths for one particular machine and it's terribly dependent on environmental packages 
(i.e. it won't work on your machine without massive configuration)

For directories: the script reads in the images<br />
For URLs: the script scrapes the site using ImageScraper and reads in the images.

Images are first processed by Inception in Tensorflow, a neural network for categorizing images with good accuracy.
Then the images are processed through a Docker container supporting Caffe, the engine required for using Yahoo's open_nsfw evaluation.

Lastly, imagename/location as well as the categorization and NSFW evaluation are sent to an SQLite database

--To do:--<br />
Flag images in db that score .7 or higher as NSFW for review<br />
Add ability to change name of project<br />
Work on interoperability -- may have to start over :/<br />
