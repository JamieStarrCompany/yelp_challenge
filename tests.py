def get_scenario(n):
    s = (("Phoenix", "Mexican", "Wednesday", [14,0]),\
    ("Gilbert", "Deli", "Saturday", [13,0]))
    if n < len(s):
        return s[n]
