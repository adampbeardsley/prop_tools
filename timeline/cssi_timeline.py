import timeline

cssi = timeline.Timeline(begin='15 Sep 2019', end='15 Oct 2022')

# Create tasks with start date, end date, description, and category.
cssi.add_task('1 Oct 2019', '31 Dec 2020', 'Infrastructure Design', 'Inf')
cssi.add_task('1 July 2020', '31 Dec 2021', 'SimpleDS Test Case', 'Inf')
cssi.add_task('1 Jan 2021', '30 Sept 2021', 'Gather Costing Data', 'Inf')
cssi.add_task('1 Oct 2021', '30 Sep 2022', 'Create Estimator Tool', 'Inf')
cssi.add_task('1 Oct 2019', '1 April 2021', 'Community engagement,\n code sprints', 'Comm')
cssi.add_task('1 April 2021', '30 Sept 2022', 'Community Development,\n Outreach', 'Comm')


cssi.add_event('1 Feb 2021', 'Open Design Review', 'Comm')
cssi.add_event('1 April 2021', 'Release V1.0', 'Inf')
cssi.add_event('1 June 2021', 'Publish JOSS Paper', 'Comm')
cssi.add_event('5 Jan 2022', 'AAS Workshop', 'Comm')
cssi.add_event('1 June 2020', 'User Meeting', 'Comm')
cssi.add_event('1 April 2022', 'SimpleDS Results', 'Inf')

# Make the plot.
cssi.plot()
