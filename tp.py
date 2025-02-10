import pandas as pd  

# Load the Excel file  
df = pd.read_excel("your_file.xlsx")  

# Remove text inside parentheses including the parentheses  
df["Employee Name"] = df["Employee Name"].str.replace(r"\s*\(.*?\)", "", regex=True)  

# Save the cleaned data back to Excel  
df.to_excel("cleaned_file.xlsx", index=False)  

print("User IDs removed successfully!")
