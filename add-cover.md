Here's a modified version of the code I use. You will want to change the `example.mp3` and `cover.jpg` (and perhaps the mime type too):
  
 import eyed3

    audiofile = eyed3.load('example.mp3')
    if (audiofile.tag == None):
        audiofile.initTag()

    audiofile.tag.images.set(3, open('cover.jpg','rb').read(), 'image/jpeg')

    audiofile.tag.save()

`tag.images.set()` takes three arguments:

- **Picture Type**: This is the type of image it is. `3` is the code for the front cover art. You can [find them all here][1].
- **Image Data**: This is the binary data of your image. In the example, I load this in using `open().read()`.
- **Mime Type**: This is the type of file the binary data is. If it's a `jpg` file, you'll want `image/jpeg`, and if it's a `png` file, you'll want `image/png`.

[1]: http://id3.org/id3v2.3.0#Attached_picture
