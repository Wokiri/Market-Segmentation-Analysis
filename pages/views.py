from django.shortcuts import render
from django.conf import settings
from django.contrib.gis.geos import MultiPoint, Point
from django.contrib  import messages
from django.core.serializers import serialize

from data.models import (
    Sale,
    Customer,
    Excel,
    Ward,
)

from data.forms import (
    ExcellModelForm,
)


from pathlib import Path, PurePath
import pandas
import csv, io, json



# Create your views here.
def home_page_view(request):
    template_name = 'pages/homepage.html'

    context = {
        'page_name': 'Home',
    }

    if Sale.objects.count() > 0 and Customer.objects.count() > 0 and Ward.objects.count() > 0:

        customers_geojson = serialize(
            'geojson',
            Customer.objects.filter(customer_name__lte=2000),
            # Customer.objects.all(),
            # srid=3857,
            fields = ('customer_name', 'pk', 'geom')
        )

        market_wards_geojson = serialize(
            'geojson',
            Ward.objects.all(),
        )
        
        
        context = {
            'page_name': 'Home Page',
            'customers_geojson': customers_geojson,
            'market_wards_geojson': market_wards_geojson,
        }
        
    return render(request, template_name, context)


def theExcelDataFrame():
    excel_file = Excel.objects.order_by('created').last()
    if excel_file is not None:
        file_name = PurePath(settings.MEDIA_ROOT, str(excel_file.file))
        if Path(file_name).exists:
            return {
                'file_name': excel_file.file,
                'excel_df': pandas.read_excel(file_name)
            }

    

def uploadExcel_view(request):
    template_name = 'pages/upload_file.html'
    excel_form = ExcellModelForm(request.POST or None, request.FILES or None)

    context = {
        'page_name': 'Upload File',
        'excel_form' : excel_form,
    }

    dropped_excel_DF = None

    if request.method == 'POST' and excel_form.is_valid():
        excel_form.save()

        excel_DF = theExcelDataFrame()['excel_df']

        dropped_excel_DF = excel_DF.loc[excel_DF['Product A'] < 0].loc[excel_DF['Longitude'] == 0].to_html()
        excel_DF = excel_DF.loc[excel_DF['Product A'] >= 0].loc[excel_DF['Longitude'] != 0]

        def df_row_values(num:int):
            return list(excel_DF.iloc[num].values)

        for i in range(len(excel_DF)):
            row_vals = df_row_values(i)

            new_customer, created = Customer.objects.update_or_create(
                customer_name = row_vals[0],
                defaults = {
                    'customer_name': row_vals[0],
                    'longitude': row_vals[6],
                    'latitude': row_vals[5],
                    'geom': MultiPoint(Point(row_vals[6], row_vals[5], srid=4326))
                }
            )

            
            new_sale, created = Sale.objects.update_or_create(
                customer = new_customer,
                defaults = {
                    'date': row_vals[4],
                    'product_a': row_vals[1],
                    'product_b': row_vals[2],
                    'product_c': row_vals[3],
                }
            )

        messages.success(request, f'Created/Updated {Customer.objects.count()} Customer Records!')
        messages.success(request, f'Created/Updated {Sale.objects.count()} Sale Records!')

    if theExcelDataFrame() is not None:
        context = {
            'page_name': 'Upload File',
            'excel_form' : excel_form,
            'excel_name' : theExcelDataFrame()['file_name'],
            'dropped_excel_DF': dropped_excel_DF,
        }
        
    return render(request, template_name, context)