import streamlit as st
from streamlit_antd_components import sac
from itertools import chain

# Sample trade view columns
trade_view_columns = ["Trade_Count_sum", "BUSINESS_DATE", "Trade_Price_avg", "Trade_Volume"]

# Default selection
default_selection = ["Trade_Count_sum"]

# Initialize session state if not already present
if "selected_columns" not in st.session_state:
    st.session_state.selected_columns = list(default_selection)

# Sidebar: Tree selection
category_tree = [{"label": col, "value": col} for col in trade_view_columns if col != "BUSINESS_DATE"]
new_selection = sac.tree(
    items=category_tree,
    label="Features",
    open_all=False,
    checkbox=True,
    key='feature_selector'
)

# Combine new selections
new_selection = list(chain(default_selection, new_selection))

# Search box for column selection
search_col = st.text_input("Search for a column")

if st.button("Add Column"):
    if search_col in new_selection:
        st.warning(f"Column '{search_col}' is already selected.")
    elif search_col in trade_view_columns and search_col != "BUSINESS_DATE":
        st.session_state.selected_columns.append(search_col)
        st.success(f"Added '{search_col}' to selection.")
    else:
        st.error("Invalid column name.")
    
    # Clear search box
    st.experimental_rerun()

# Show selected columns
st.write("Selected Columns:", st.session_state.selected_columns)
