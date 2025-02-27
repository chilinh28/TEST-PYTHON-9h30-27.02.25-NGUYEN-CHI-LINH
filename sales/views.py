from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
from datetime import datetime
from .models import SalesRecord
from django.db.models import Sum, Count

@api_view(['POST'])
def upload_csv(request):
    if 'file' not in request.FILES:
        return Response({"error": "File not found"}, status=400)
    file = request.FILES['file']

    if not file.name.endswith('.csv'):
        return Response({"error": "File must be CSV"}, status=400)
    try:
        df = pd.read_csv(file)

        required_columns = {'date', 'region', 'product', 'quantity', 'price'}
        if not required_columns.issubset(df.columns):
            return Response({"error": "Format file missing attribute"}, status=400)

        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        records = [
            SalesRecord(
                date=row['date'],
                region=row['region'],
                product=row['product'],
                quantity=row['quantity'],
                price=row['price']
            )
            for _, row in df.iterrows()
        ]
        SalesRecord.objects.bulk_create(records)

        return Response({"message": "Uploaded successfully"})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def get_sales(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    region = request.GET.get('region')

    if not start_date or not end_date or not region:
        return Response({"error": "Required parameters (start_date, end_date, region)"}, status=400)
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_records = SalesRecord.objects.filter(date__range=[start_date, end_date], region=region)

        total_quantity = filtered_records.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_sales = filtered_records.aggregate(total_sales=Sum('quantity') * Sum('price'))['total_sales'] or 0
        transaction_count = filtered_records.count()

        return Response({
            "total_quantity": total_quantity,
            "total_sales": total_sales,
            "transaction_count": transaction_count
        })

    except ValueError:
        return Response({"error": "Invalid date format"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
