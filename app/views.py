# from django.shortcuts import render
# from django.http import HttpResponse
# from django.core.exceptions import ValidationError
# from .models import scrapeData
# import os
# import requests
# from bs4 import BeautifulSoup
# from django.conf import settings

# # Create your views here.

# def index(request):
#     return render(request,"index.html")

# def scripe_image(request):
#     url = request.POST.get('url')
#     number_of_images  = request.POST.get('number')
#     if number_of_images is None:
#         return HttpResponse("Number of images is required")
    
#     try:
#         number_of_images = int(number_of_images)
#         if number_of_images < 0:
#             raise ValidationError("Number of images must be a positive number")
#     except ValidationError:
#         return HttpResponse("Invalid number of images please enter positive integer")
    
#     image_urls = []
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content,"html.parser")
#     for img in soup.find_all('img'):
#         image_urls.append(img['src'])

#     # save the images to the database and media folder
#     for image_url in image_urls[:number_of_images]:
#         image_data = requests.get(image_url).content
#         filename = os.path.basename(image_url)

#         # # save the image to the media folder
#         # media_folder = settings.MEDIA_ROOT
#         # with open(os.path.join(media_folder,filename),'wb') as f:
#         #     f.write(image_data)

#         # scrape_data = scrapeData(URL = url, Name_Of_Img = filename)
#         # scrape_data.save()
#     context = {
#         "Imags_urls":image_urls,
#     }
#     return render(request,"index.html",context)


import os
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.conf import settings
from django.shortcuts import render
from .models import scrapeData


def scripe_image(request):
    # Get the URL and number of images from the request
    url = request.POST.get("url")
    number_of_images = request.POST.get("number")

    # Check if the number of images is None
    if number_of_images is None:
        return HttpResponse("Number of images is required.")

    # Validate the number of images
    try:
        number_of_images = int(number_of_images)
        if number_of_images <= 0:
            raise ValidationError("Number of images must be a positive integer.")
    except ValueError:
        return HttpResponse(
            "Invalid number of images. Please enter a positive integer."
        )

    # Scrape the images from the website
    image_urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for img in soup.find_all("img"):
        image_urls.append(img["src"])

    # Save the images to the database and media folder
    for image_url in image_urls[:number_of_images]:
        image_data = requests.get(image_url).content
        filename = os.path.basename(image_url)

        # Save the image to the media folder
        media_folder = settings.MEDIA_ROOT
        with open(os.path.join(media_folder, filename), "wb") as f:
            f.write(image_data)

        # Create a scrapeData object and save it to the database
        scrape_data = scrapeData(URL=url, Name_Of_Img=filename)
        scrape_data.save()

    return render(request, "index.html", {"image_urls": image_urls})


def index(request):
    return render(request, "index.html")
