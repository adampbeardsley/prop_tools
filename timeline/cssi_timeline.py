import timeline

cssi = timeline.Timeline(begin='15 Sep 2019', end='15 Oct 2022')

# Create tasks with start date, end date, description, and category.
cssi.add_task('1 Oct 2019', '31 Dec 2020', 'Prototype Pipeline Tracker', 'Inf')
cssi.add_task('1 July 2020', '1 June 2022', 'SimpleDS on HERA and MWA data', 'Sci')
cssi.add_task('1 Jan 2021', '30 Sept 2021', 'Gather Costing Data', 'Inf')
cssi.add_task('1 Oct 2021', '30 Sep 2022', 'Create Estimator Tool', 'Inf')

cssi.add_task('1 Oct 2019', '1 April 2021', 'Community Input:\nTelecons,'
              + ' Code Sprints, Reviews', 'Comm')
cssi.add_task('1 April 2021', '30 Sept 2022', 'Community Outreach:\n'
              + 'Advertise, Recruit, Support Users', 'Comm')


cssi.add_event('1 Oct 2020', 'Open Design Review', 'Comm')
cssi.add_event('1 Jan 2021', 'Release V1.0', 'Inf')
cssi.add_event('1 March 2021', 'Publish JOSS Paper', 'Comm')
cssi.add_event('5 Jan 2022', 'AAS Workshop', 'Comm')
# cssi.add_event('1 June 2020', 'User Meeting', 'Comm')
cssi.add_event('1 Sep 2021', 'MWA results', 'Sci')
cssi.add_event('1 June 2022', 'HERA results', 'Sci')
# cssi.add_event('1 July 2022', 'Two External Adopters', 'Comm')
cssi.add_event('1 Sept 2022', 'Publish Cost Estimator', 'Inf')

# Jigger the colors
cssi.categories['Inf'].color = '#d9ead3ff'  # green
cssi.categories['Comm'].color = '#c9daf8ff'  # blue
cssi.categories['Sci'].color = '#f4ccccff'  # red

# Make the plot.
cssi.plot()
