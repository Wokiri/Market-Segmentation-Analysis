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
# import csv, io, json



# Create your views here.
def home_page_view(request):
    template_name = 'pages/home_page.html'

    sales_df = None
    customers_df = None
    wards_df = 4

    if Sale.objects.count() > 0 and Customer.objects.count() > 0 and Ward.objects.count() > 0:

        ward_customer_list = []

        for ward in Ward.objects.all():
            custs = Customer.objects.filter(customer_name__lte=500).filter(geom__intersects=ward.geom)#.values_list('customer_name')
            if custs:
                custs_list = []
                for i, obj in enumerate(list(custs)):
                    custs_list.append(obj.customer_name)
                ward_customer_data = {str(ward.ward):custs_list}
                ward_customer_list.append(ward_customer_data)


        print(ward_customer_list)
        # wards_df = pandas.DataFrame().to_html(
        #     justify='center', show_dimensions=True, classes=[
        #         'table table-dark table-striped table-sm table-bordered font-barlow-light align-middle'
        #     ]
        # )

        sales_df = pandas.DataFrame(Sale.objects.values())
        customers_df = pandas.DataFrame(Customer.objects.values('id', 'customer_name')).rename(
            columns={
                'id':'Customer Id',
                'customer_name':'Customer Name',
            }
        )

        sales_df_head = sales_df.rename(
            columns={
                'id':'Sale Id',
                'date':'Sale Date',
                'product_a': 'Product A',
                'product_b': 'Product B',
                'product_c': 'Product C',
                'customer_id': 'Customer Id',
                'total_sales': 'Total Sales',
            }
        ).merge(customers_df, left_on='Customer Id', right_on='Customer Id').set_index('Sale Id').head().to_html(
            justify='center', show_dimensions=True, classes=[
                'table table-dark table-striped table-sm table-bordered font-barlow-light align-middle'
            ]
        )

    context = {
        'page_name': 'Home Page',
        'sales_df': sales_df,
        'customers_df': customers_df,
        'sales_df_head': sales_df_head,
        'wards_df': wards_df,
    }

    return render(request, template_name, context)



def map_page_view(request):
    template_name = 'pages/map_page.html'

    context = {
        'page_name': 'Map',
    }

    if Sale.objects.count() > 0 and Customer.objects.count() > 0 and Ward.objects.count() > 0:

        customers_geojson = serialize(
            'geojson',
            Customer.objects.filter(customer_name__lte=15000),
            # Customer.objects.all(),
            # srid=3857,
            fields = ('customer_name', 'pk', 'geom')
        )

        market_wards_geojson = serialize(
            'geojson',
            Ward.objects.all(),
        )
        
        
        context = {
            'page_name': 'Map Page',
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