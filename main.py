import streamlit as st
from streamlit_option_menu import option_menu
#import os
import about,lttimes,top12 

st.set_page_config(
        page_title="Swim Times ",
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
  
        with st.sidebar:    
    
            app = option_menu(
                #menu_title='Swim Times ',
                menu_title='',
                options=['About','LTtimes','Top12'],
               # icons=['house-fill','person-circle','trophy-fill','chat-fill','info-circle-fill'],
#                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"margin": "1px !important","padding": "1!important","background-color":"#74b6f9"},
        #"icon": {"color": "white", "font-size": "18x"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#74b6f9"},
        }
                )
        st.sidebar.write(":blue[Designed and Developed by Rohan Kodibagkar]")
        st.sidebar.image("./LTswimteam.jpg", use_column_width=True)  
        
        if app == "About":
            about.app()
        if app == "LTtimes":
            lttimes.app()    
        if app == "Top12":
            top12.app()        
             
    run()            
         