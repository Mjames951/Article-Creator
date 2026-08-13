from PIL import Image, ImageOps
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile

def addImage(form, modelInstance=None):
    print("IMAGE HANDLER CALLED")
    Image = form.cleaned_data['image']
    imageName, newImage = CropPicture(Image)
    if not imageName or not newImage:
        form.add_error(None, 'The uploaded file is not a valid image')
        return False
    try: #to save the image
        if not modelInstance: modelInstance = form.save(commit=False)
        modelInstance.image.save(imageName, ContentFile(newImage.read()), save=False)
        return modelInstance
    except:
        form.add_error(None, "Unable to save the uploaded file.")
        modelInstance.delete()
        return None

def CropPicture(OGpicture):
    maxEdge = settings.IMG_MAX_WIDTH_HEIGHT

    try: 
        picture = Image.open(OGpicture)
        picture.verify()
        #reopen due to verify pointer at end of file
        picture = Image.open(OGpicture)

        #convert png to RGB
        if picture.mode in ("RGBA", "LA", "P"):
            picture = picture.convert("RGB")

            (width, height) = picture.size
            maxside = max(width, height)
            divisor = maxside / maxEdge
            picture = picture.resize((round(width/divisor), round(height/divisor)), Image.LANCZOS)

        picture = ImageOps.exif_transpose(picture) #fixes image rotation on iphone images

        #Create a new picture file to be saved as the image
        temp_picture = BytesIO()
        picture.save(temp_picture, format="JPEG", quality=70, optimize=True)
        temp_picture.seek(0)
        original_name, _ = OGpicture.name.lower().split(".")
        original_name=original_name.split("/")[-1]
        picture = f"{original_name}.jpg"
        return picture, temp_picture          
    except:
        return None, None