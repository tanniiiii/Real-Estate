def to_camel_case(name):
    parts = name.split('_')
    return '_'.join([parts[0].capitalize()] + [p.lower() for p in parts[1:]])

# Example usage
names = [", "ORDER_ID", "CUSTOMER_NAME"]
camel_case_names = [to_camel_case(name) for name in names]

print(camel_case_names)
