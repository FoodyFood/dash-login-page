import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import warnings
import os
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
import configparser

port=8050
username: str
url_prefix: str
if 'JUPYTERHUB_USER' in os.environ:
    username = os.environ['JUPYTERHUB_USER']
    url_prefix= f"/user/{username}/proxy/{port}/"
else:
    url_prefix = "/"


warnings.filterwarnings("ignore")
conn = sqlite3.connect('users.sqlite')
engine = create_engine('sqlite:///users.sqlite')
db = SQLAlchemy()
config = configparser.ConfigParser()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable = False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(80))


Users_tbl = Table('users', Users.metadata)


app = dash.Dash(__name__, requests_pathname_prefix=url_prefix)
server = app.server


app.config.suppress_callback_exceptions = True


# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///users.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db.init_app(server)


# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = f'{url_prefix}/login'


#User as base

# Create User class with UserMixin
class Users(UserMixin, Users):
    pass


create = html.Div([ html.H1('Create User Account')
        , dcc.Location(id='create_user', refresh=True)
        , dcc.Input(id="username"
            , type="text"
            , placeholder="user name"
            , maxLength =140)
        , dcc.Input(id="email"
            , type="email"
            , placeholder="email"
            , maxLength = 140)
        , dcc.Input(id="password"
            , type="password"
            , placeholder="password")
        , dcc.Input(id="role"
            , type="text"
            , placeholder="role"
            , maxLength = 50)
        , html.Button('Create User', id='submit-val', n_clicks=0)
        , html.Div(id='container-button-basic')
    ])#end div


login =  html.Div([dcc.Location(id='url_login', refresh=True)
            , html.H2('''Please log in to continue:''', id='h1')
            , dcc.Input(placeholder='Enter your username',
                    type='text',
                    id='uname-box')
            , dcc.Input(placeholder='Enter your password',
                    type='password',
                    id='pwd-box')
            , html.Button(children='Login',
                    n_clicks=0,
                    type='submit',
                    id='login-button')
            , html.Div(children='', id='output-state')
        ]) #end div


success = html.Div([dcc.Location(id='url_login_success', refresh=True)
            , html.Div([html.H2('Login successful.')
                    , html.Br()
                    , html.P('Select An App')
                    , dcc.Link('App 1', href = f'{url_prefix[:-1]}/app1')
                ]) #end div
            , html.Div([html.Br()
                    , html.Button(id='back-button', children='Go back', n_clicks=0)
                ]) #end div
        ]) #end div


data = html.Div([dcc.Dropdown(
                    id='dropdown',
                    options=[{'label': i, 'value': i} for i in ['Day 1', 'Day 2']],
                    value='Day 1')
                , html.Br()
                , html.Div([dcc.Graph(id='graph')])
            ]) #end div


failed = html.Div([ dcc.Location(id='url_login_df', refresh=True)
            , html.Div([html.H2('Log in Failed. Please try again.')
                    , html.Br()
                    , html.Div([login])
                    , html.Br()
                    , html.Button(id='back-button', children='Go back', n_clicks=0)
                ]) #end div
        ]) #end div

logout = html.Div([dcc.Location(id='logout', refresh=True)
        , html.Br()
        , html.Div(html.H2('You have been logged out - Please login'))
        , html.Br()
        , html.Div([login])
        , html.Button(id='back-button', children='Go back', n_clicks=0)
    ])#end div


app.layout= html.Div([
            html.Div(id='page-content', className='content')
            ,  dcc.Location(id='url', refresh=False)
        ])


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.callback(
    Output('page-content', 'children')
    , [Input('url', 'pathname')])
def display_page(pathname):
    print(f"User {current_user} navigated to: {pathname}")
    if pathname == f'{url_prefix[:-1]}/':
        return login
    elif pathname == f'{url_prefix[:-1]}/login':
        return login
    if pathname == f'{url_prefix[:-1]}/create':
        if current_user.is_authenticated:
            user = Users.query.filter_by(id=current_user.id).first()
            if user.role == "admin":
                return create
            else:
                return 'User does not have admin permissions'
        else:
            return login
    elif pathname == f'{url_prefix[:-1]}/success':
        if current_user.is_authenticated:
            return success
        else:
            return failed
    elif pathname == f'{url_prefix[:-1]}/app1':
        if current_user.is_authenticated:
            return data
    elif pathname == f'{url_prefix[:-1]}/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout
        else:
            return logout
    else:
        return '404 - Page Not Found'


#set the callback for the dropdown interactivity
@app.callback(
    [Output('graph', 'figure')]
    , [Input('dropdown', 'value')])
def update_graph(dropdown_value):
    if dropdown_value == 'Day 1':
        return [{'layout': {'title': 'Graph of Day 1'}
                , 'data': [{'x': [1, 2, 3, 4]
                    , 'y': [4, 1, 2, 1]}]}]
    else:
        return [{'layout': {'title': 'Graph of Day 2'}
                ,'data': [{'x': [1, 2, 3, 4]
                    , 'y': [2, 3, 2, 4]}]}]


@app.callback(
   [Output('container-button-basic', "children")]
    , [Input('submit-val', 'n_clicks')]
    , [State('username', 'value'), State('email', 'value'), State('password', 'value'), State('role', 'value')])
def insert_users(n_clicks, username, email, password, role):
    if username == None or password == None: # This is run on page load, so we catch that there is no User/Pass yet and return empty
        return [html.Div()]
    hashed_password = generate_password_hash(password, method='sha256')
    if username is not None and email is not None and password is not None:
        ins = Users_tbl.insert().values(username=username, email=email, password=hashed_password, role=role)
        conn = engine.connect()
        conn.execute(ins)
        conn.close()
        return [login]
    else:
        return [html.Div([html.H2('Already have a user account?'), dcc.Link('Click here to Log In', href=f'{url_prefix[:-1]}/login')])]


@app.callback(
    Output('url_login', 'pathname')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def successful(n_clicks, username, password):
    user = Users.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return f'{url_prefix[:-1]}/success'
        else:
            pass
    else:
        pass


@app.callback(
    Output('output-state', 'children')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def update_output(n_clicks, username, password):
    if n_clicks > 0:
        user = Users.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        return ''


@app.callback(
    Output('url_login_success', 'pathname')
    , [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return f'{url_prefix[:-1]}/'


@app.callback(
    Output('url_login_df', 'pathname')
    , [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return f'{url_prefix[:-1]}/'


# Create callbacks
@app.callback(
    Output('url_logout', 'pathname')
    , [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return f'{url_prefix[:-1]}/'


if __name__ == '__main__':
    app.run_server(debug=True)