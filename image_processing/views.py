from django.shortcuts import render

# Create your views here.

import cv2
import numpy as np
import os
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ImageUploadForm
from .models import ProcessedImage

def process_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_obj = form.save()
            
            # Get the image path
            image_path = img_obj.original_image.path
            
            # Read the image with OpenCV
            image = cv2.imread(image_path)
            
            # Apply OpenCV operations (example: convert to grayscale)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Save the processed image
            processed_path = os.path.join(settings.MEDIA_ROOT, 'processed', 
                                       os.path.basename(image_path))
            cv2.imwrite(processed_path, gray_image)
            
            # Update the model with processed image path
            relative_path = os.path.join('processed', os.path.basename(image_path))
            img_obj.processed_image = relative_path
            img_obj.save()
            
            return render(request, 'result.html', {'img_obj': img_obj})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})