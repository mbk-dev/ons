import ons


val = ons.infl.get_cpih()
print(val)

val = ons.infl.get_inflation_cpih()
print(val)


gdp = ons.get_gdp()
print(gdp)