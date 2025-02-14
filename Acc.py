import streamlit as st
from itertools import chain
import streamlit_antd_components as sac

# Initialize session state
if 'selected_columns' not in st.session_state:
    st.session_state.selected_columns = ["Trade_Count_sum"]  # Default selection
if 'search_columns' not in st.session_state:
    st.session_state.search_columns = []

# Sidebar tree component
with st.sidebar:
    tree_selection = sac.tree(
        items=category_tree,
        label="Features",
        open_all=False,
        checkbox=True,
        key='feature_selector'
    )

# Main interface
st.header("Column Selection")

# Search and add functionality
search_term = st.text_input("Search and add features", key='search_box')
if st.button("Add") and search_term:
    valid_columns = [col for col in trade_view_columns 
                    if col != 'BUSINESS_DATE' and col not in st.session_state.selected_columns]
    
    if search_term in valid_columns:
        st.session_state.search_columns.append(search_term)
        st.session_state.search_box = ""  # Clear search box
    else:
        st.warning(f"Column '{search_term}' is invalid or already selected")

# Combine all selections
all_selected = list(chain(
    ["Trade_Count_sum"],  # Default
    st.session_state.search_columns,
    tree_selection
))

# Check for duplicates
unique_selected = list(set(all_selected))
duplicates = [item for item in set(all_selected) if all_selected.count(item) > 1]

if len(duplicates) > 0:
    st.warning(f"Duplicate columns detected: {', '.join(duplicates)}")

# Update session state
if sorted(all_selected) != sorted(st.session_state.selected_columns):
    st.session_state.selected_columns = unique_selected

# Display final selection
st.write("Selected Columns:", st.session_state.selected_columns)