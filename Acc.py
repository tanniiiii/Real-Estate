import streamlit as st
import streamlit_antd_components as sac
from itertools import chain

# Sample trade view columns
trade_view_columns = ["Trade_Count_sum", "BUSINESS_DATE", "Trade_Price_avg", "Trade_Volume"]

# Default selection
default_selection = ["Trade_Count_sum"]

# Initialize session state
if "selected_columns" not in st.session_state:
    st.session_state.selected_columns = list(default_selection)

# Sidebar: Tree selection
category_tree = [{"label": col, "value": col} for col in trade_view_columns if col != "BUSINESS_DATE"]
tree_selection = sac.tree(
    items=category_tree,
    label="Features",
    open_all=False,
    checkbox=True,
    key='feature_selector'
)

# Combine tree selections
new_selection = list(chain(default_selection, tree_selection))

# Search and select columns using multiselect
search_selection = st.multiselect(
    "Search and select columns",
    options=[col for col in trade_view_columns if col != "BUSINESS_DATE"]
)

# Add selected columns if not already in the list
for col in search_selection:
    if col in new_selection:
        st.warning(f"Column '{col}' is already selected.")
    else:
        st.session_state.selected_columns.append(col)
        st.success(f"Added '{col}' to selection.")

# Show selected columns
st.write("Selected Columns:", st.session_state.selected_columns)
