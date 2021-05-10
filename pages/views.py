from django.shortcuts import render, get_object_or_404
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
# import numpy
# import csv, io, json



# Create your views here.
def home_page_view(request):
    template_name = 'pages/home_page.html'

    sales_df = None
    customers_df = None
    ward_customer_list = None
    sales_df_head = None


    if Sale.objects.count() > 0 and Customer.objects.count() > 0 and Ward.objects.count() > 0:

        ward_customer_list = []

        for ward in Ward.objects.all():
            customers = Customer.objects.filter(geom__intersects=ward.geom)#.values_list('customer_name')
            if customers:
                custs_list = []
                for i, obj in enumerate(list(customers)):
                    custs_list.append(obj.customer_name)
                ward_customer_data = {
                    'Ward':str(ward.ward),
                    'SubCounty':str(ward.sub_county),
                    'County':str(ward.county),
                    'Number_Clients':len(custs_list),
                }
                ward_customer_list.append(ward_customer_data)
                

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
        'ward_customer_list': ward_customer_list,
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
            # Customer.objects.filter(customer_name__lte=10000),
            Customer.objects.all(),
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


def theExcelDataFrame(nrows):
    excel_file = Excel.objects.order_by('created').last()
    if excel_file is not None:
        file_name = PurePath(settings.MEDIA_ROOT, str(excel_file.file))
        if Path(file_name).exists:
            return {
                'file_name': excel_file.file,
                'excel_df': pandas.read_excel(
                    file_name,
                    nrows=nrows
                )
            }
    

def uploadExcel_view(request):
    template_name = 'pages/upload_file.html'
    excel_form = ExcellModelForm(request.POST or None, request.FILES or None)

    context = {
        'page_name': 'Upload File',
        'excel_form' : excel_form,
    }

    dropped_excel_DF = None
    excel_results = None

    if request.method == 'POST' and excel_form.is_valid():
        excel_form.save()

        excel_results = theExcelDataFrame(100)

        excel_DF = excel_results['excel_df']

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

    if excel_results is not None:
        context = {
            'page_name': 'Upload File',
            'excel_form' : excel_form,
            'excel_name' : excel_results['file_name'],
            'dropped_excel_DF': dropped_excel_DF,
        }
        
    return render(request, template_name, context)



def ward_detail_view(request, ward_url):
    template_name = 'pages/ward_detail.html'
    
    ward = get_object_or_404(Ward, ward_url=ward_url)
    customers = Customer.objects.filter(geom__intersects=ward.geom)
    total_prod_a_sales = 0
    total_prod_b_sales = 0
    total_prod_c_sales = 0
    total_sales = 0

    for customer in customers:
        sale = Sale.objects.get(customer=customer)
        total_prod_a_sales += sale.product_a
        total_prod_b_sales += sale.product_b
        total_prod_c_sales += sale.product_c
        total_sales += sale.total_sales
    num_customers = customers.count()

    context = {
        'page_name': 'Ward Detail',
        'ward' : ward,
        'num_customers' : num_customers,
        'total_prod_a_sales' : total_prod_a_sales,
        'total_prod_b_sales' : total_prod_b_sales,
        'total_prod_c_sales' : total_prod_c_sales,
        'total_sales' : total_sales,
    }
        
    return render(request, template_name, context)