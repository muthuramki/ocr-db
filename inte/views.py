
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from django.http import HttpResponseNotAllowed
import os
import requests
import base64
import json
from rest_framework import generics
from .models import OCRResponse
from .serializers import OCRResponseSerializer
 
# Define your Azure Form Recognizer configuration
endpoint = "https://savic-ocr-integration-document-intelligence.cognitiveservices.azure.com/"
key = "7be7b9df5d014fbd94c2d5ce7961925a"
model_id = "Almaya_Choithram_Shankar_Trading_Custom_Model"
desired_fields = ['Invoice Number', 'Invoice Date', 'Purchase Order Number', 'VendorName', 'VendorAddress', 'Vendor Tax Id', 'Customer Name', 'Customer Tax Id', 'SubTotal', 'Total Tax', 'Invoice Total', 'Amount', 'Description', 'ProductCode', 'Barcode', 'Quantity', 'Tax', 'TaxRate', 'Unit', 'UnitPrice','MaterialNumber','LineText','LineItemNo']
 
# Function to extract fields from Form Recognizer result
def extract_fields(result):
    data = []
    for idx, document in enumerate(result.documents):
        doc_data = flatten_document_fields(document.fields)
        data.append(doc_data)
    return data
 
# Function to flatten document fields
def flatten_document_fields(fields):
    flattened_fields = {}
    for name, field in fields.items():
        field_value = field.value if field.value else field.content
        if name == 'Items' and field.value_type == "list":
            items_data = []
            for item in field.value:
                item_fields = flatten_document_fields(item.value)
                items_data.append(item_fields)
            flattened_fields[name] = items_data
        elif field.value_type == "dictionary":
            nested_flattened_fields = flatten_document_fields(field.value)
            flattened_fields.update(nested_flattened_fields)
        elif name in desired_fields:
            flattened_fields[name] = field_value
    return flattened_fields
 
# Function to analyze layout and extract fields
def analyze_layout(file_path):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    with open(file_path, "rb") as file:
        content = file.read()
    poller = document_analysis_client.begin_analyze_document(
        model_id=model_id, document=content
    )
    result = poller.result()
    structured_output = extract_fields(result)
    return structured_output
 
# View for uploading invoice
def upload_invoice(request):
    if request.method == 'POST' and request.FILES.get('invoice'):
        invoice_file = request.FILES['invoice']
        temp_file_path = 'temp_invoice.pdf'
        with open(temp_file_path, 'wb') as f:
            for chunk in invoice_file.chunks():
                f.write(chunk)
        try:
            extracted_data = analyze_layout(temp_file_path)
            return render(request, 'invoice_data.html', {'extracted_data': extracted_data})
        except Exception as e:
            print(f"Error occurred during document analysis: {e}")
            return HttpResponse("Error occurred during document analysis.", status=500)
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
    return render(request, 'upload.html')
 
# View for pushing data to SAP
import json
import base64
import requests
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render
from .models import OCRResponse
 
def push_to_sap(request):
    if request.method == 'POST':
        # Extract JSON data from the request body
        data = json.loads(request.body)
 
        # Convert the JSON data to a string with indentation
        json_data = json.dumps(data, indent=4)
 
        # Print the JSON data in the terminal
        print("Received JSON data:", json_data)
 
        # Define your username and password
        username = "SAIP"
        password = "Praneeth@10"
 
        # Encode the credentials
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
 
        # Construct the URL with the JSON data
        sap_url = f"http://savic1909.savictech.com:8000/sap/bc/abap/zmigo_vk/rest/?sap-client=220&req={json.dumps(data)}"
 
        response = requests.get(sap_url, headers={'Authorization': 'Basic ' + credentials})    
        if response.status_code == 200:
            print("JSON data retrieved successfully from SAP portal!")
            sap_response_json = response.json()
            print("Response:", json.dumps(sap_response_json, indent=4))
           
            # Format the message to be saved
            message = f'code: "Success", msgtxt: "Records :0008 got updated"'
           
            # Create and save OCRResponse instance
            ocr_response = OCRResponse(code="Success", msgtxt="Records :0008 got updated")
            ocr_response.save()
 
            # Print the message
            print(message)
           
            # Render response.html with SAP response
            return render(request, 'response.html', {'sap_response': sap_response_json})
        else:
            print("Failed to push JSON data to SAP portal. Status code:", response.status_code)
            print("Error message:", response.text)
           
            # Format the error message to be saved
            message = f'code: "Error", msgtxt: "Failed with status code: {response.status_code}"'
           
            # Create and save OCRResponse instance with error details
            ocr_response = OCRResponse(code="Error", msgtxt=f"Failed with status code: {response.status_code}")
            ocr_response.save()
 
            # Print the error message
            print(message)
           
            # Return JSON response with error message and appropriate status code
            return JsonResponse({'error_message': 'Failed to push JSON data to SAP portal'}, status=response.status_code)
 
    return HttpResponseNotAllowed(['POST'])
 
 
   
   
def home_page_view(request):
    return render(request, 'Home-page.html')
 
def login_view(request):
    return render(request, 'login.html')

def forgot_password_view(request):
    return render(request, 'forgot-password.html')
 
def reset_password_view(request):
    return render(request, 'reset-password.html')
 
def drop_menu_view(request):
    return render(request, 'drop-menu.html')
 
def register_page_view(request):
    return render(request, 'register.html')
 
def upload_page_view(request):
    return render(request, 'upload.html')
 
# views.py
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import status
from django.http import JsonResponse
 
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
 
@ensure_csrf_cookie
def login_view(request):
    error_message = {'username': None, 'password': None}  # Initialize error messages
   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to drop-menu.html upon successful login
            return redirect('drop-menu.html')
        else:
            error_message['username'] = 'Invalid username or password'
            error_message['password'] = 'Invalid username or password'
 
    csrf_token = get_token(request)
    return render(request, 'login.html', {'error_message': error_message, 'csrf_token': csrf_token})
 
from rest_framework import generics
from .models import OCRResponse
from .serializers import OCRResponseSerializer
 
class OCRResponseCreateView(generics.CreateAPIView):
    queryset = OCRResponse.objects.all()
    serializer_class = OCRResponseSerializer
   
   
 
from django.shortcuts import render
from .models import OCRResponse
from django.db.models import Count
 
def drop_menu_view(request):
    last_ocr_response = OCRResponse.objects.last()
    success_count = OCRResponse.objects.filter(code='Success').count()
    failed_count = OCRResponse.objects.filter(code='Error').count()
   
    context = {
        'last_ocr_response': last_ocr_response,
        'success_count': success_count,
        'faild_count' : failed_count,
    }
    return render(request, 'drop-menu.html', context)
 