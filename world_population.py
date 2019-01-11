import json
from country_codes import get_country_code
from pygal.maps.world import World
from pygal.style import RotateStyle, LightColorizedStyle


filename = 'population_data.json'
with open(filename) as f:
    pop_data = json.load(f)

    # Build a dictionary of population data
    # Extract the population of every country in 2010
    # The else part caters for countries that do not have codes, as they are regions/groupings other than specified countries
    # Apply pygal.style() attribute to use one color base for each shade
    cc_populations = {}
    for pop_dict in pop_data:
        if pop_dict['Year'] == '2010':
            country_name = pop_dict['Country Name']
            population = int(float(pop_dict['Value']))
            code = get_country_code(country_name)
            if code:
                cc_populations[code] = population

# Group the countries into three different population levels
cc_pops_1, cc_pops_2, cc_pops_3 = {}, {}, {}
for cc, pop in cc_populations.items():
    if pop < 10000000:
        cc_pops_1[cc] = pop
    elif pop < 1000000000:
        cc_pops_2[cc] = pop
    else:
        cc_pops_3[cc] = pop

# See how many countries are in each level
print(len(cc_pops_1), len(cc_pops_2), len(cc_pops_3))

# Style the world map, apply single base color, but varying shade.
wm_style = RotateStyle('#0000FF', base_style=LightColorizedStyle)
wm = World(style=wm_style)

wm.title = 'World Population in 2010, by country'
wm.add('0-10m', cc_pops_1)
wm.add('10m-1bn', cc_pops_2)
wm.add('>1bn', cc_pops_3)

wm.render_to_file('world_population.svg')



