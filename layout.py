import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto


layout = html.Div([html.Div(className='eight columns', children=[
    html.Div(className='queries', children=[
        dcc.Input(id="input1", type="text", placeholder="기업명"),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
        dcc.Input(id="input2", type="text", placeholder="시작 일자", debounce=True),
        dcc.Input(id="input3", type="text", placeholder="종료 일자", debounce=True),
        dcc.Input(id="input4", type="text", placeholder="최신 이슈", debounce=True),
        dcc.Input(id="input5", type="text", placeholder="유사 키워드", debounce=True),
        dcc.Input(id="input6", type="number", min=1, max=10, placeholder="유사 키워드 갯수", debounce=True),
        dcc.Input(id="input7", type="number", placeholder="종목", min=1, max=10, debounce=True)
    ]),
    cyto.Cytoscape(
        id='cytoscape',
        elements=[
        ],
        layout={'name': 'concentric'},
        style={'width': '900px', 'height': '900px'}
        )
    ])])