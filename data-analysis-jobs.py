# from optparse import Option
# from turtle import color
import pandas
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output 


app = Dash(__name__)
server = app.server
data_set = pandas.read_csv("https://docs.google.com/spreadsheets/d/1Y7PCYJB89TWe-h-IylolkcrH2OU9fN1qViSPYXH6X7M/gviz/tq?tqx=out:csv&sheet=final_data".format('1Y7PCYJB89TWe-h-IylolkcrH2OU9fN1qViSPYXH6X7M','final_data'))
value_counts = data_set.groupby(['Company_Name' ]).size().reset_index(name='count')
#print(value_counts.Company_Name[0])

app.layout = html.Div([

    html.H1("Linkdn data analysis trending jobs skill requirements"),

    

    dcc.Dropdown(id="company_name",
                 options=value_counts.Company_Name,
                 multi=False,
                 value=value_counts.Company_Name[0],
                 style={'width': "50%", "display": "inline-block", "grid-gap": "10px"}),

    dcc.Dropdown(id='level',
                 options=[],
                 multi=False,
                 value=None,
                 style={'width': "50%", "display": "inline-block", "grid-gap": "10px"}),

    dcc.Graph(id="job_level",figure={},style={'width': "37%", "display": "inline-block", "grid-gap": "10px"}),
    dcc.Graph(id="job_type",figure={},style={'width': "63%", "display": "inline-block", "grid-gap": "10px"}),


    dcc.Dropdown(id='designation',
                 options=[],
                 multi=False,
                 value=None,
                 style={'width': "63%", "display": "inline-block", "grid-gap": "10px"}),

    dcc.Graph(id='skills',figure={},style={'width': "100%", "display": "inline-block", "grid-gap": "10px"}),

    dcc.Graph(id='average_applicant',figure={},style={'width': "100%", "display": "inline-block", "grid-gap": "10px"})

    

])

# hireing_companies = data_set['Company_Name'].value_counts()
# print(hireing_companies)

@app.callback(
    [Output(component_id="job_level",component_property='figure'),
     Output(component_id='level',component_property='options'),
     Output(component_id='level',component_property='value')],

    [Input(component_id="company_name",component_property='value')]
    
)

def detail_graph(name):
    data = data_set.copy()
    company_require = data[data['Company_Name'] == name].groupby([ 'Involvement']).size().reset_index(name='count')
    

    pie_chart = px.pie( names=company_require.Involvement, values=company_require['count'], title="Job levels percentage requirement")



    new_options = [{'label': f' {i}', 'value': f'{i}'} for i in company_require.Involvement]
    new_value = new_options[0]['value'] if new_options else None

    return [pie_chart,new_options,new_value]


@app.callback(
    [Output(component_id='job_type',component_property='figure'),
     Output(component_id='designation',component_property='options'),
     Output(component_id='designation',component_property='value')],

    [Input(component_id="level",component_property='value'),
     Input(component_id="company_name",component_property='value')]
)

def detail_graph(type,name):
    data = data_set.copy()
    company_industry_require = data[(data['Company_Name'] == name) & (data['Involvement'] == type)].groupby([ 'Designation']).size().reset_index(name='count')
  
    bar_chart =  px.bar( x=company_industry_require.Designation.str[:20], y=company_industry_require['count'], title="Job levels percentage requirement",color=company_industry_require['count'])

    return [bar_chart,company_industry_require.Designation,company_industry_require.Designation[0]]
    
@app.callback(
    [Output(component_id='skills',component_property='figure'),
     Output(component_id='average_applicant',component_property='figure')
     ],

    [Input(component_id="company_name",component_property='value'),
    Input(component_id="level",component_property='value'), 
    Input(component_id='designation',component_property='value')
    ]
)

def detail_graph(name,type,designation):
    data = data_set.copy()
    required_skill = []
    for skill in data.columns[10:]:
        required_skill.append(data[(data['Company_Name'] == name) & (data['Involvement'] == type) &(data['Designation']== designation)][skill].sum())
    bar_chart =  px.bar( x=data.columns[10:], y=required_skill, title=f"Type of skill required requirement for {designation}",color=required_skill)

    data = data[['Company_Name','Involvement','Designation','Total_applicants']]
    applicants = []
    for job in data[(data['Company_Name'] == name) & (data['Involvement'] == type)].Designation.drop_duplicates():
        print()
        applicants.append(data[data['Designation'] == job]['Total_applicants'].sum())
    bar_chart2 =  px.bar( x=data[(data['Company_Name'] == name) & (data['Involvement'] == type)].Designation.drop_duplicates().str[:20], y=applicants, title="Number of applicants",color=applicants)


    return [bar_chart,bar_chart2]



if __name__ == '__main__':
    app.run_server(debug=True)
