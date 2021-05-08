from django.shortcuts import render
from django.conf import settings
from django.contrib.gis.geos import Point

from data.models import (
    Sale,
    Customer,
    Excel,
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
    return render(request, template_name, context)


def theExcelDataFrame():
    excel_file = Excel.objects.order_by('created').last()
    if excel_file is not None:
        file_name = PurePath(settings.MEDIA_ROOT, str(excel_file.file))
        if Path(file_name).exists:
            return {
                'file_name': excel_file.file,
                'excel_df': pandas.read_excel(
                    file_name,
                    sheet_name='Nairobi',
                    index_col="CustomerName"
                    )
            }

    

def uploadExcel_view(request):
    template_name = 'pages/upload_file.html'
    excel_form = ExcellModelForm(request.POST or None, request.FILES or None)

    excel_DF = theExcelDataFrame()

    if excel_form.is_valid():
        excel_form.save()
        # uploaded_file = request.FILES['file']
        # excel_name = uploaded_file.name

        # Decode the excel
        # excel_data = uploaded_file.read().decode('UTF-8')

        # #Set up stream
        # io_string = io.StringIO(excel_data)

        # # Skip the header row
        # next(io_string)

        # for col in csv.reader(io_string, delimiter=','):

        #     new_sale, created = Sale.objects.update_or_create(
        #         customer_name = col[0],
        #         defaults = {
        #             'date': col[4],
        #             'product_a': col[1],
        #             'product_b': col[2],
        #             'product_c': col[3],
        #         }
        #     )

        #     new_customer, created = Customer.objects.update_or_create(
        #         customer_name = col[0],
        #         defaults = {
        #             'customer_name': col[0],
        #             'latitude': col[5],
        #             'longitude': col[6],
        #             'geom': Point(col[6], col[5], srid=4326)
        #         }
        #     )



    context = {
        'page_name': 'Upload File',
        'excel_form' : excel_form,
        'excel_name' : excel_DF['file_name'],
        # 'excel_df' : excel_DF['excel_df'].to_html(),
    }
    return render(request, template_name, context)