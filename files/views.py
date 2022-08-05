# Import mimetypes module
import mimetypes
# Import HttpResponse module
from django.http.response import HttpResponse

from hashlib import new
from pathlib import Path
from django.utils import timezone
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, HttpResponse

from .azure_file_controller import ALLOWED_EXTENTIONS, download_blob, upload_file_to_blob

from . import models
from azure.storage.blob import ContainerClient
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from .models import File
from django.core.files.storage import FileSystemStorage

azure_connection_string = "DefaultEndpointsProtocol=https;AccountName=bojan01;AccountKey=43yMGDN6D2JG+DOxHCdll2HOrGgzacYWmDAYQgRhFwUBGgoA9T3FJF1qbRImUVsz7rdghbKGcDJj+AStJH2RjQ==;EndpointSuffix=core.windows.net"
container_name = "myfiles"


def upload_to_azure(myfile, azure_connection_string, container_name):
    container = ContainerClient.from_connection_string(azure_connection_string, container_name)
    if not container.exists():
        container.create_container()

    try:
        with open("./myfiles/" + myfile, "rb") as f:
            container.get_blob_client(myfile).upload_blob(f)
            print(myfile, "uploaded to container", container_name)
    except:
        print(myfile, "is already uploaded to container", container_name)


def index(request):
    return render(request, "files/index.html", {})


date_string = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        new_file = File(file_name=file.name, file=file)
        new_file.date_created = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
        new_file.save()
        
        # find all files
        files = os.listdir("./myfiles")
        for myfile in files:
            if myfile == file.name:
                print("yes, I found the file", myfile)
                upload_to_azure(myfile, azure_connection_string, container_name)
                messages.success(
                    request, f"{file.name} was successfully uploaded")
                return render(request, "files/upload_file.html", {})
    return render(request, "files/upload_file.html", {})


def list_files(request):
    files = File.objects.all()
    context = {"files": files}
    return render(request, "files/list_files.html", context=context)


# def download(request, id):
#     obj = File.objects.get(file_id=id)
#     filename = obj.model_attribute_name.path
#     response = FileResponse(open(filename, 'rb'))
#     return response


import os
from django.conf import settings
from django.http import HttpResponse, Http404

def delete_file(request,file_id):
    file = models.File.objects.get(pk=file_id)
    file.deleted = 1
    file.save()
    return redirect("list_files")

from django.http import FileResponse

def download(request, file_id):
    obj = File.objects.get(id=file_id)
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    return response


def download(request, file_id):
    obj = File.objects.get(id=file_id)
    filename = obj.file_name

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = BASE_DIR + '/myfiles/' + filename
    
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
