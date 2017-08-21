import timeline

example = timeline.Timeline()

example.add_task('1 May 2018', '15 April 2019', '21cmFAST runs', 'red')
example.add_task('1 Jan 2019', '1 April 2020', 'Mock 21cm Observations', 'red')
example.add_task('1 July 2019', '1 Dec 2020', 'zre PDFs', 'red')
example.add_task('1 April 2019', '1 Feb 2020', 'broad hydro sims', 'blue')
example.add_task('1 Oct 2020', '1 May 2021', 'final forecasts', 'yellow')
example.add_task('1 July 2018', '1 April 2019', 'fiducial hydro sims', 'blue')
example.add_task('1 Feb 2020', '1 Jan 2021', 'narrow hydro sims', 'blue')
example.add_task('15 Jun 2020', '1 May 2021', 'refined mapping function', 'blue')
example.add_task('1 Jan 2019', '15 Oct 2019', 'initial mapping function', 'blue')
example.add_task('1 April 2019', '15 March 2021', 'joint 21 cm field galaxy catalogs', 'yellow')
example.add_task('1 Oct 2019', '1 July 2020', 'preliminary forecasts', 'yellow')

example.add_event('1 Oct 2018', 'Conf 1', 'Conf')
example.add_event('1 June 2019', 'Conf 2', 'Conf')
example.add_event('1 March 2020', 'Conf 3', 'Conf')
example.add_event('29 Sep 2019', 'Paper 1', 'Paper')
example.add_event('20 May 2020', 'Paper 2', 'Paper')
example.add_event('1 Jan 2021', 'Paper 3', 'Paper')

example.plot()
