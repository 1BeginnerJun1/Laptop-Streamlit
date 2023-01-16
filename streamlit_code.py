import streamlit as st
import pandas as pd
import joblib
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from PIL import Image

#Load model and scaler
model = load_model('D:/Latihan Coding/Data Science Portfolio/Portfolio 1 - Gaming Laptop Price Estimation/laptopestimate.h5')
scaler = MinMaxScaler()
scaler = joblib.load('scaler.gz')

st.title('Estimate The Gaming Laptop Price You Want to Know!')
col1, col2, col3 = st.columns([1,4,1])
with col2:
        image = Image.open('D:/Latihan Coding/Data Science Portfolio/Portfolio 1 - Gaming Laptop Price Estimation/laptopimage.JPG')
        st.image(image, caption = 'Source : All-free-download.com')
st.subheader('Informations : ')
informations = (
"* Laptop Brand : It is laptop's brand.",
"* Device Type : Class of device.",
"* Operation System : System software that manages computer hardware, software resources, and provides common services for computer programs.",
"* Processor : CPU (Central Processing Unit)",
"* GPU Max Speed : Maximum speed of GPU to operate",
"* RAM Type : RAM capacity and its type",
"* Solid State Drive : Capacity of solid state drive (SSD)",
"* Size : Laptop's screen size",
"* Weight : Laptop's weight",
"* Resolution : Laptop's display resolutions",
"* Pixel Per Inch : Number of pixels within one inch of an image displayed on a monitor (common value: 141)",
"* Touch Screen : Is it touch screen or not? ",
)
for i in informations:
        st.markdown(i)

# Created empty dataset as template
dataset = pd.read_csv("D:/Latihan Coding/Data Science Portfolio/Portfolio 1 - Gaming Laptop Price Estimation/Trainerdata.csv")
empty_df = dataset[0:0]

col1, col2 = st.columns(2)
# Categorical list
devicetype_list = [x.split('_')[1] for x in dataset.columns if "Device Type" in x]
resolution_list = [x.split('_')[1] for x in dataset.columns if "Resolution" in x]
ssd_list = sorted(dataset['Solid State Drive'].unique())
laptopbrand_list = [x.split('_')[1] for x in dataset.columns if "Laptop Brand" in x]
os_list = [x.split('_')[1] for x in dataset.columns if "OS" in x]
processor_list = [x.split('_')[1] for x in dataset.columns if "Processor" in x]
ram_list = [x.split('_')[1] for x in dataset.columns if "RAM" in x]

# Function to convert Touch feature
def touchconvert(a):
        if a == 'Yes':
                return 1
        else:
                return 0

with st.sidebar:
        st.markdown("<p style='font-size: 24px'>Let's input your laptop's specifications here!</p>", 
                        unsafe_allow_html=True)
        # Input box
        laptopbrand = st.selectbox("Laptop Brand", laptopbrand_list)
        devicetype = st.selectbox ("Device Type", devicetype_list)
        os = st.selectbox("Operation System", os_list)
        processor = st.selectbox("Processor", processor_list)
        maxspeed = st.number_input("GPU Max Speed (GHz)", min_value=1.8, step=0.1)
        ram = st.selectbox("RAM Type", ram_list)
        solidstatedrive = st.selectbox ("Solid State Drive (GB)", ssd_list)
        size = st.number_input("Size (inch), Range : 13.3 inches - 18.4 inches", min_value=13.3, max_value=18.4, step=0.01)
        weight = st.number_input("Weight (kg), Range : 1 kg - 8 kg", min_value=1.0, max_value=8.0, step=0.01)
        resolution = st.selectbox("Resolution", resolution_list)
        ppi = st.number_input("Pixel Per Inch", min_value=100, step=1)
        touch = st.selectbox("Touch Screen", ('Yes','No'))
        # Prepare input data
        dict = {
                "Laptop Brand_"+laptopbrand : 1,
                "Device Type_"+devicetype : 1,
                "OS_"+os : 1,
                "Processor_"+processor : 1,
                "Max Speed" : maxspeed,
                "RAM_"+ram : 1,
                "Solid State Drive" : int(solidstatedrive),
                "Size" : size,
                "Weight" : weight,
                "Resolution_"+resolution : 1,
                "PPI" : ppi,
                "Touch" : touchconvert(touch)
                }
        # Convert input data into a understandable format by model
        value = pd.concat([empty_df,pd.DataFrame([dict])], axis=0, ignore_index=True).drop('Price', axis=1)
        data = value.fillna(0).values
        input_data = scaler.transform(data)
        predict = model.predict(input_data)
        st.subheader(" ")

#Show result
button = st.button("Calculate!")
if button:
        st.subheader("Estimated gaming laptop price :")
        st.subheader(f"Rp " + str("{:,}".format(int(predict[0][0]))))