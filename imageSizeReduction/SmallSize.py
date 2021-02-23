import PIL

from PIL import Image, ImageFilter
import os
#Read image
path = "/Users/rpkDocuments/before/"
new_path="/Users/rpkDocuments/after/"
#resize_ratio = 0.5  # where 0.5 is half size, 2 is double size
basewidth = 1000

def resize_im():
    dirs = os.listdir(path)
    for item in dirs:
        print (item) 
        if (item.endswith('.jpg'))==0:
            continue
        if os.path.isfile(path+item):
            img = Image.open(path+item)
            file_path, extension = os.path.splitext(path+item)
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
            print(file_path)
            file_name=file_path[len(path):len(file_path)]
            print(file_name)
            print(extension)
            img.save(new_path + file_name + "_sml" + extension , 'JPEG', quality=90)
            
resize_im()            