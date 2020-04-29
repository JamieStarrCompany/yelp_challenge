def get_scenario(n):
    s = (("Phoenix", "Mexican", "Wednesday", [14,0]),\
    ("Gilbert", "Delis", "Saturday", [13,0]),\
    ("Scottsdale", "Breakfast & Brunch", "Sunday" , [9,0] ),\
    ("Glendale", "Barbeque", "Sunday", [18,0]),\
    ("Chandler", "Asian Fusion", "Thursday", [18,0]),\
    ("Cave Creek", "American (New)", "Tuesday", [17,0]),\
    ("Fountain Hills", "Pizza", "Friday", [13,3]),\
    ("Avondale", "African", "Monday", [12,0]))
    if n > 0:
        if n <= len(s):
            return s[n-1]
