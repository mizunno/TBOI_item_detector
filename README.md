# TBOI item detector (under development)

Are you a The Binding of Isaac player? Do you think there are a lot of items and trinkets to know about? In this project, a Deep Learning based item detector is proposed. The idea is to detect an item given an image of it take it from your phone, or whatever.

This is just a fun project to do in my free time and does not pretend to be a serious project. But all contributions are welcome :wink:.

## Download items images

The Deep Learning model need images to learn how to detect new ones. So first we need to download all items images. Due to the large number of items (Repentance expansion), a script to automate the process is given in `code/scripts/items_scraper.py`. The script scraps the webpage `https://bindingofisaacrebirth.fandom.com/` (thanks :smile:) in order to find and download the images and some useful information about them. The script only needs the output path for the images and the output path for the CSV file containing some metadata (item name, image path, etc) about the items.

```python

python code/items_scrapper.py <IMAGES_OUTPUT_PATH> <METADATA_OUTPUT_PATH>
```

## Training dataset generation

In order to train the DL model to detect items from photos, we need thousands (or even more) of images. But that kind of dataset does not exists (yet) so we are going to generate it transforming the items images.