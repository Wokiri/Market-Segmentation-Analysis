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


from .forms import (
    NumberOfRecordForm,
    SearchWardForm,
)


from pathlib import Path, PurePath
from math import pi
import pandas

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.transform import cumsum
from bokeh.palettes import Category20_20, Spectral4

def pie_chart(source=None,
    title='Pie Chart',
    tool_tips=None,
    radius=0.8,
    line_color='#000000',
    legend_field='',
    legend_orient='horizontal',
    legend_loc='top_center'
    ):
    plot = figure(
        title=title,
        tooltips=tool_tips,
    )
    plot.wedge(
        x=0,
        y=1,
        radius=radius,
        start_angle=cumsum('value', include_zero=True),
        end_angle=cumsum('value'),
        line_color=line_color,
        fill_color='color',
        source=source,
        legend_field=legend_field,
    )

    plot.axis.visible=False
    plot.axis.axis_line_color=None
    plot.toolbar.active_drag = None
    plot.title.align = "center"
    plot.title.text_color = "DarkSlateBlue"
    plot.title.text_font_size = "18px"
    plot.legend.orientation = legend_orient
    plot.legend.location = legend_loc

    script, div = components(plot)

    return {
        'script':script,
        'div':div,
    }


def draw_bar_charts(
    x_name,
    x_label,
    y_name,
    y_label,
    source=None,
    title='Bar Graph',
    tool_tips=None,
    legend_field='',
    x_range=[],
    fill_color='color',
    legend_orientation="horizontal",
    legend_location = "top_left"
):
    
    b_graph=figure(
        title=title,
        x_axis_label=x_label,
        y_axis_label=y_label,
        tooltips = tool_tips,
        x_range=x_range,
        # y_range=(0,9),
        plot_width=1120,
        )
        
    
    b_graph.vbar(
        x=x_name,
        top=y_name,
        source=source,
        width=0.8,
        legend_field=legend_field,
        fill_color=fill_color,
        line_color ='#331100',
        )

    b_graph.toolbar.active_drag = None
    b_graph.title.align = "center"
    b_graph.title.text_color = "darkgreen"
    b_graph.title.text_font_size = "18px"
    b_graph.xaxis.major_label_text_color = 'darkgreen'
    b_graph.yaxis.major_label_text_color = 'darkgreen'
    b_graph.xgrid.grid_line_color = None
    b_graph.y_range.start=0
    b_graph.legend.orientation=legend_orientation
    b_graph.legend.location = legend_location


    b_graph_script, b_graph_div = components(b_graph)

    return {
        'b_graph_script': b_graph_script,
        'b_graph_div': b_graph_div,
    }






# Create your views here.
def home_page_view(request):
    template_name = 'pages/home_page.html'


    context = {
        'page_name': 'Home Page',
    }


    if Sale.objects.count() > 0 and Customer.objects.count() > 0 and Ward.objects.count() > 0:

        ward_customer_list = []
        wards = []

        for ward in Ward.objects.all():
            customers = Customer.objects.filter(geom__intersects=ward.geom)#.values_list('customer_name')
            if customers:
                custs_list = []
                for i, obj in enumerate(list(customers)):
                    custs_list.append(obj.customer_name)
                wards.append(ward)
                ward_customer_data = {
                    'Ward':str(ward.ward),
                    'SubCounty':str(ward.sub_county),
                    'County':str(ward.county),
                    'Number_Clients':len(custs_list),
                    'WardUrl':ward.ward_url,
                }
                ward_customer_list.append(ward_customer_data)
            

        sales_df = pandas.DataFrame(Sale.objects.values())
        customers_df = pandas.DataFrame(Customer.objects.values('id', 'customer_name')).rename(
            columns={
                'id':'Customer Id',
                'customer_name':'Customer Name',
            }
        )

        county_df = pandas.DataFrame(data=ward_customer_list, columns=['County', 'Number_Clients']).groupby(['County']).sum()
        county_df.loc[:,'color'] = Category20_20[:len(county_df)]
        county_df.loc[:,'value'] = county_df['Number_Clients']/county_df['Number_Clients'].sum() * 2*pi

        county_geog = pie_chart(
            source=ColumnDataSource(county_df),
            legend_field='County',
            title='Market Composition by County',
            tool_tips=[
                ('County', '@County'),
                ('No. Customers', '@Number_Clients'),
            ]
        )

        sub_county_df = pandas.DataFrame(data=ward_customer_list, columns=['SubCounty', 'Number_Clients']).groupby(['SubCounty']).sum()
        sub_county_df.loc[:,'color'] = Category20_20[:len(sub_county_df)]
        sub_county_df.loc[:,'value'] = sub_county_df['Number_Clients']/sub_county_df['Number_Clients'].sum() * 2*pi

        sub_county_geog = pie_chart(
            source=ColumnDataSource(sub_county_df),
            legend_field='SubCounty',
            title='Market Composition by SubCounty',
            tool_tips=[
                ('SubCounty', '@SubCounty'),
                ('No. Customers', '@Number_Clients'),
            ],
            legend_orient='vertical',
            legend_loc='right',
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
            'county_script': county_geog['script'],
            'county_div': county_geog['div'],
            'sub_county_script': sub_county_geog['script'],
            'sub_county_div': sub_county_geog['div'],
            'num_wards': len(wards),
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
            return pandas.read_excel(
                    file_name,
                    nrows=nrows
                )
    

def uploadExcel_view(request):
    template_name = 'pages/upload_file.html'
    excel_form = ExcellModelForm(request.POST or None, request.FILES or None)
    num_records_form = NumberOfRecordForm(request.POST or None)

    context = {
        'page_name': 'Upload File',
        'excel_form' : excel_form,
        'num_records_form' : num_records_form,
    }

    dropped_excel_DF = None

    if 'n_rows' in request.POST and excel_form.is_valid() and num_records_form.is_valid():
        excel_form.save()

        n_rows = num_records_form.cleaned_data['n_rows']
        excel_DF = theExcelDataFrame(n_rows)
        

        dropped_excel_DF = excel_DF.loc[excel_DF['Product A'] < 0].loc[excel_DF['Longitude'] == 0].to_html(
            justify='center', show_dimensions=True, classes=[
                'table table-warning table-striped table-sm table-bordered font-barlow-light align-middle'
            ]
        )
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

    if Excel.objects.all():
        context = {
            'page_name': 'Upload File',
            'excel_form' : excel_form,
            'num_records_form' : num_records_form,
            'excel_name' : Excel.objects.order_by('created').last().file,
            'dropped_excel_DF': dropped_excel_DF,
        }
        
    return render(request, template_name, context)



def ward_detail_view(request, ward_url):
    template_name = 'pages/ward_detail.html'
    search_ward_form = SearchWardForm(request.POST or None)

    ward = get_object_or_404(Ward, ward_url=ward_url)

    if search_ward_form.is_valid() and 'ward_name' in request.POST:
        ward = get_object_or_404(Ward, ward__icontains=search_ward_form.cleaned_data['ward_name'])
    
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

    ward_geojson = serialize(
        'geojson',
        Ward.objects.filter(ward_url=ward.ward_url),
        fields = ('ward', 'geom')
    )

    ward_customers_geojson = serialize(
        'geojson',
        customers,
        fields = ('customer_name', 'geom')
    )

    data = {
        'total_prod_a_sales':[total_prod_a_sales],
        'total_prod_b_sales':[total_prod_b_sales],
        'total_prod_c_sales':[total_prod_c_sales],
        'total_sales':[total_sales],
    }

    columns=['Total Product A Sales', 'Total Product B Sales', 'Total Product C Sales', 'Cumulative Sales',]
    values=[total_prod_a_sales, total_prod_b_sales, total_prod_c_sales, total_sales]

    source = ColumnDataSource(data=dict(columns=columns, values=values, color=Spectral4))

    ward_bar_graph = draw_bar_charts(
        'columns',
        'Products',
        'values',
        'Sales Quantity',
        source=source,
        legend_field='columns',
        title=f'Sales Bar Chart for {ward.ward} Ward',
        x_range=columns,
        tool_tips=[
                ('Sales', '@values'),
            ]
        )


    context = {
        'page_name': 'Ward Detail',
        'ward' : ward,
        'search_ward_form':search_ward_form,
        'num_customers' : num_customers,
        'total_prod_a_sales' : total_prod_a_sales,
        'total_prod_b_sales' : total_prod_b_sales,
        'total_prod_c_sales' : total_prod_c_sales,
        'total_sales' : total_sales,
        'ward_geojson' : ward_geojson,
        'ward_customers_geojson' : ward_customers_geojson,
        'bar_graph_script' : ward_bar_graph['b_graph_script'],
        'bar_graph_div' : ward_bar_graph['b_graph_div'],
    }
        
    return render(request, template_name, context)