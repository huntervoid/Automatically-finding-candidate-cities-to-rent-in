from craigslist import CraigslistHousing
cl_h = CraigslistHousing(site='sfbay', area='sfc', category='roo',
                         filters={'max_price': 1200, 'private_room': True})

# You can get an approximate amount of results with the following call:
print(cl_h.get_results_approx_count())


for result in cl_h.get_results(sort_by='newest', geotagged=True):
    print(result)