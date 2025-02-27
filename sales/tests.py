import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

test_client = APIClient()

def test_upload_csv_success():
    url = reverse('upload_csv')
    csv_content = b"date,region,product,quantity,price\n2024-01-01,USA,ItemA,10,100.0"
    csv_file = SimpleUploadedFile("sales_data.csv", csv_content, content_type="text/csv")
    response = test_client.post(url, {'file': csv_file}, format='multipart')
    assert response.status_code == 200
    assert response.data["message"] == "File uploaded successfully"

def test_upload_csv_failure():
    url = reverse('upload_csv')
    response = test_client.post(url, {}, format='multipart')
    assert response.status_code == 400
    assert "error" in response.data
    
def test_get_sales():
    url = reverse('get_sales') + "?start_date=2024-01-01&end_date=2024-02-01&region=USA"
    response = test_client.get(url)
    assert response.status_code == 200