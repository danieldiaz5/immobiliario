from config.conexionDb import conn
import streamlit as st
import pandas as pd
from pathlib import Path
# import base64
from PIL import Image
import os
import json
import pickle
# from streamlit_extras.mention import mention
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import (CredentialsError,
                                                ForgotError,
                                                Hasher,
                                                LoginError,
                                                RegisterError,
                                                ResetError,
                                                UpdateError)


# Inicializa la sesión 
# st.session_state.logged_in = False

## FUNCIONES
# Cargar el modelo desde el archivo .bin
def load_model(file_path):
    with open(file_path, 'rb') as file:
        dv, model = pickle.load(file)
    return dv, model

# Procesar el arreglo JSON y predecir usando el modelo
def predict(json_data, dv, model):
    
    X = dv.transform([json_data])
    
    # prediction = model.predict(transformed_data)
    
    y_predict = model.predict_proba(X)[0,1]
    
    churn = y_predict >= 0.5
    
    return y_predict , churn


def page1():
    
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://img.freepik.com/free-photo/gradient-blue-abstract-background-smooth-dark-blue-with-black-vignette-studio_1258-68059.jpg?t=st=1732944985~exp=1732948585~hmac=d45bf004e7e071ec13bf89121ed0349eb52665fdb1cf1a81fa2af6905e2d7046&w=1380");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    
    # Ruta a tu imagen de fondo
    img_path = Path("data/data.jpg")

    st.markdown("<h1 style='text-align: center;'>INMOBILIARIA</h1>", unsafe_allow_html=True)
    # st.markdown(
    #     """ <div style="display: flex; 
    #     align-items: center;"> 
    #     <img src="ruta_de_tu_imagen.jpg" 
    #     width="50" style="margin-right: 10px;"> <h1>Título de tu aplicación</h1> </div> """,
    #     unsafe_allow_html=True)

    # Define la ruta de la imagen
    image_path = Path(img_path)

    col1, col2, col3 = st.columns(3)
    with col2:
        if image_path.is_file():
            st.image(image_path.as_posix(), caption='Casa', use_container_width=True)
        else:
            st.write("El archivo de imagen no se encontró.")
            


    st.write("Introduce los valores de tus variables:")


    # Entrada de texto para el arreglo JSON 
    # json_input = st.text_area('Ingresa el arreglo JSON aquí')

    col1, col2 = st.columns(2)


    with col1:
        TotalCharges = st.number_input('TotalCharges',min_value=0)
        MonthlyCharges = st.number_input("MonthlyCharges",min_value=0)

    with col2:
        tenure = st.number_input('tenure',min_value=0)
        options = ["Male", "Female"]
        gender = st.selectbox("Selecciona una opción", options)
        # gender = st.text_input('Género:')


    json_input = {
        "customerID": "1992-zkjort",
        "gender":gender,
        "SeniorCitizen": 1,
        "Partner": "si",
        "Dependents": "yes",
        "tenure": tenure,
        "PhoneService": "yes",
        "MultipleLines": "no",
        "InternetService": "fiber optic",
        "OnlineSecurity": "yes",
        "OnlineBackup": "yes",
        "DeviceProtection": "no",
        "TechSupport": "no",
        "StreamingTV": "no",
        "StreamingMovies": "yes",
        "Contract": "1 year",
        "PaperlessBilling": "yes",
        "PaymentMethod": "bank_transfer_(automatic)",
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges
    }

    json_input =  json.dumps(json_input)
    # Cargar el modelo
    dv, model = load_model('src/models/model_C=1.0.bin') 

    if st.button('Procesar'):
        try:
            data = json.loads(json_input)
            df = pd.DataFrame([data])
            st.write(df)
            
            y_predict, churn = predict(data, dv, model)
            
            result = {
                    'probabilidad de abandono': float(y_predict),
                    'abandono': bool(churn)
                }
            # st.success(f'Resultado: {result}')
            st.write(result)
        except json.JSONDecodeError:
            st.error('Error al procesar el JSON. Asegúrate de que el formato es correcto.')
        except Exception as e:
            st.error(f'Error al predecir: {e}')

        




    # Directorio donde se almacenarán las imágenes
    upload_dir = "data/"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)


    # Cargar una imagen desde el disco local 
    uploaded_file = st.file_uploader("Elige una imagen", type=["png", "jpg", "jpeg"]) 


    # Almacenar la imagen si se ha cargado un archivo válido
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_path = os.path.join(upload_dir, uploaded_file.name)
        image.save(image_path)
        st.success(f"Imagen almacenada en: {image_path}")

def page2(): 
    st.title("Recomendación") 
    st.write("Página en Construcción") 
    
def page3(): 
    st.title("Inversión") 
    st.write("Página en Construcción") 


# Function to change the sidebar color
def change_sidebar_color(color):
    st.markdown(
        f"""
        <style>
        .sidebar .sidebar-content {{
            background-color: {color} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def authenticate_user(usuario, password): 
    try: 
        query = f"""SELECT u.password 
                    FROM "USUARIOS" u 
                    WHERE username = '{usuario}'
                    """
        result = pd.read_sql(query,conn)
        
        if result['password'].values[0] == password: 
            return True 
        return False 
    except Exception as e: 
        print(f"Database error: {e}") 
        return False
    
def insert_usuario(name: str,lastname: str,username: str,password: str,email: str):
    # conn = sqlite3.connect('inmodbcore')
    # c = conn.cursor()
    INSERT_Q = """
                INSERT INTO USUARIOS 
                (username,password,nombre,email)
                VALUES (?,?,?,?) """
    nombre = name + ' ' + lastname
    parameters = (username,password,nombre,email)
    try:
        with conn.cursor as cursor:
            conn.   execute(INSERT_Q,parameters)
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        conn.close()
        return False
        



        
st.set_page_config(
    page_title = 'INMILIARIA',
    layout = 'wide',
    page_icon = ':derelict_house_building:'
)




# Verificar si hay un estado de sesión para el inicio de sesión
if 'login' not in st.session_state:
    st.session_state['login'] = False
    
if 'register' not in st.session_state:
    st.session_state['register'] = False

if st.session_state['login']:
    # Aquí va tu aplicación principal
    # authenticator.logout()
    # st.write(f'Welcome *{st.session_state["name"]}*')

    with st.sidebar:
        # CSS para cambiar el color de fondo de la barra lateral 
        # sidebar_css = """ 
        #     <style> 
        #         .css-1d391kg { /* Clase CSS específica de la barra lateral */ 
        #         background-color: #0E78FB !important; /* 
        #         Cambia #0E78FB al color que desees */ } 
        #     </style> """ 
        # # Aplica el CSS 
        # st.markdown(sidebar_css, unsafe_allow_html=True)

        # sidebar_color = st.sidebar.color_picker('Choose sidebar color', '#FFFFFF')
        # change_sidebar_color('#FFFFFF')

        # URL de la imagen de fondo
        background_image_url = "https://img.freepik.com/free-photo/gradient-blue-abstract-background-smooth-dark-blue-with-black-vignette-studio_1258-68059.jpg?t=st=1732944985~exp=1732948585~hmac=d45bf004e7e071ec13bf89121ed0349eb52665fdb1cf1a81fa2af6905e2d7046&w=1380"

        # CSS para aplicar la imagen de fondo a la barra lateral
        sidebar_css = f"""
        <style>
            .css-1d391kg {{
                background-image: url({background_image_url});
                background-size: cover;
            }}
        </style>
        """

        # Aplica el CSS
        st.markdown(sidebar_css, unsafe_allow_html=True)




        image_url = "data/icono.png"
        title = "Epsilon Data"

        html_code = f"""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <h1>{title}</h1>
        </div>
        """
        
        st.sidebar.image(image_url, use_container_width=False, width=50) 
        st.sidebar.markdown(html_code, unsafe_allow_html=True)



            
    pages = { 
            "Predicción": page1, 
            "Recomendación": page2, 
            "Inversión": page3 
            }

    selection = st.sidebar.radio("Ir a", list(pages.keys()))


    # Mostrar la página seleccionada 
    pages[selection]()


    # Agregar el nombre del usuario y un icono en la parte inferior del sidebar 
    st.sidebar.markdown("---") 
    st.sidebar.markdown("### Usuario") 
    # Datos del usuario 
    user_name = st.session_state["username"]
    # user_icon = "" 
    # user_url = "" 
    if user_name == 'jsmith':
        user_image_url = "data/profile.png" 
    elif user_name == 'rbriggs':
        user_image_url = "data/woman.png" 
    else:
        user_image_url = "data/user.png" 
    


    # Mostrar la imagen en la barra lateral 
    st.sidebar.image(user_image_url, caption=f"{user_name}", use_container_width=False,width=80)


    # HTML y CSS para la marca "Powered by" 
    powered_by = """ <div style="position: fixed; 
                    bottom: 0; 
                    right: 0; 
                    width: 100%; 
                    background-color: #f8f9fa; 
                    text-align: right; 
                    padding: 10px 20px; 
                    font-size: 12px; 
                    color: #6c757d;"> 
                    Powered by <a href="https://sites.google.com/view/epsilon-data/" 
                    target="_blank">[Epsilon Data]</a> 
                    </div> """ 

    # Agregar el HTML a la aplicación 
    st.markdown(powered_by, unsafe_allow_html=True)
    if st.button("Cerrar sesión"): 
        st.session_state['login'] = False 

else:
    # Pantalla de inicio de sesión
    st.title("Epsilon Data")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if authenticate_user(username, password):
            st.session_state['login'] = True
            st.session_state['username'] = username
        else:
            st.error("Usuario o contraseña incorrectos")

    if st.button("Registrase"):
        st.session_state['register'] = True
    
    if st.session_state['register']:
        st.subheader('Registro de nuevo usuario')
        name = st.text_input('Nombre')
        lastname = st.text_input('Apellido')
        username_new = st.text_input('Nuevo Usuario')
        password_new = st.text_input('Nueva Contraseña ',type='password')
        email = st.text_input('Correo electróncio')
        
        if st.button('Registrar'):
            if insert_usuario(name,lastname,username,password,email):
                st.success('!Registro exitoso!')
                st.session_state['register'] = False
            else:
                st.error("El nombre ya exite")


    

