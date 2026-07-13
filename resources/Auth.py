import streamlit as st

import constants as c
import resources.Environment as Env


def _password_entered() -> None:
    """
    Callback for the password input. Validates the entered value against the
    DASHBOARD_PASSWORD environment variable and updates the session auth flag
    :return:
    """

    if st.session_state.get("password_input") == Env.DASHBOARD_PASSWORD.get():
        st.session_state["dashboard_authenticated"] = True
        del st.session_state["password_input"]
    else:
        st.session_state["dashboard_authenticated"] = False


def require_password() -> None:
    """
    Gate the current page behind the password configured in the DASHBOARD_PASSWORD
    environment variable. Must be called before any other page content is rendered.
    Stops execution of the rest of the page until the correct password is entered.
    A successful login is remembered for the rest of the browser session via
    st.session_state, which is shared across pages, so this only prompts once per
    session no matter which page is opened first
    :return:
    """

    if st.session_state.get("dashboard_authenticated", False):
        return

    st.markdown(c.HIDE_ST_STYLE, unsafe_allow_html=True)
    st.title("🔒 Login required")
    st.text_input("Password", type="password", on_change=_password_entered, key="password_input")

    if st.session_state.get("dashboard_authenticated") is False:
        st.error("Incorrect password")

    st.stop()
