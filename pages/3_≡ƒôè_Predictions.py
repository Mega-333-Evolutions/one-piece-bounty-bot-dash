import streamlit as st
from streamlit_option_menu import option_menu

import constants as c
from pages.predictions.add import main as add_main
from pages.predictions.list import main as list_main
from resources.Auth import require_password


require_password()


def main():
    """
    Main function
    :return:
    """

    st.title("Predictions")
    st.markdown(c.HIDE_ST_STYLE, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Add", "List"],
        icons=["plus-square", "list-ul"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    if selected == "Add":
        add_main()
    elif selected == "List":
        list_main()


main()
