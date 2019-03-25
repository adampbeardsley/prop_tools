import matplotlib.pyplot as plt
import cPickle as pkl
from pandas import to_datetime
import matplotlib.patches as patches
from matplotlib import gridspec
from collections import OrderedDict
from itertools import cycle
import numpy as np
from matplotlib.ticker import AutoMinorLocator


def overlap(t1, t2):
    return (t2.begin < t1.begin < t2.end) or (t2.begin < t1.end < t2.end)


class Event():
    """ Class to hold information about events (instantaneous) """
    def __init__(self, time, desc, category=None):
        self.time = to_datetime(time)
        self.desc = desc
        self.category = category


class Task():
    """ Class to hold information about tasks (extend over time) """
    def __init__(self, begin, end, desc, category=None):
        self.begin = to_datetime(begin)
        self.end = to_datetime(end)
        self.desc = desc
        self.category = category
        self.row = None


class Category():
    """ Category to group tasks """
    def __init__(self, name, color=None):
        self.name = name
        self.color = color


class Timeline():

    def __init__(self, begin=None, end=None):
        self.begin = to_datetime(begin)
        self.end = to_datetime(end)
        self.tasks = []
        self.events = []
        self.categories = OrderedDict()
        self.add_category(None)

    def add_event(self, time, desc, category=None):
        self.events.append(Event(time, desc, category=category))
        if category not in self.categories.keys():
            self.add_category(category)

    def add_task(self, begin, end, desc, category=None):
        self.tasks.append(Task(begin, end, desc, category=category))
        if category not in self.categories.keys():
            self.add_category(category)

    def add_category(self, name, order=-1):
        self.categories[name] = Category(name)

    def count_categories(self, tcount=True, ecount=True):
        """ Count categories which actually have tasks or events
        Arguments:
            tcount: (bool) Whether to include tasks in the count (Default=True).
            ecount: (bool) Whether to include events in the count (Default=True).
        Returns:
            ncat: (int) Number of categories counted in tasks and/or events
        """
        ncat = 0
        for category in self.categories:
            ctasks = [t for t in self.tasks if t.category is category]
            cevents = [e for e in self.events if e.category is category]
            if tcount * len(ctasks) or ecount * len(cevents):
                ncat += 1
        return ncat

    def sort_tasks(self):
        """ Try to compress the tasks by sharing rows """
        rows = []
        for category in self.categories:
            row_i = len(rows)
            row_f = len(rows)
            ctasks = [t for t in self.tasks if t.category is category]
            if len(ctasks) == 0:
                continue
            for t1 in ctasks:
                fits = False
                for row in rows[row_i: row_f + 1]:
                    fits = True
                    for t2 in row:
                        if overlap(t1, t2):
                            fits = False
                            break
                    if fits:
                        row.append(t1)
                        break
                if not fits:
                    rows.append([t1])
                    row_f += 1
        for i, row in enumerate(rows):
            for t in row:
                t.row = i
        return len(rows)

    def plot(self, figsize=(8, 5), linewidth=1, buffsize=0.02, rounding_size=0.03):
        """ Plot the timeline """
        self.fig = plt.figure(figsize=figsize)
        plot_tasks = len(self.tasks) > 0
        plot_events = len(self.events) > 0
        if plot_tasks:
            if plot_events:
                # Plot both
                gs = gridspec.GridSpec(2, 1, height_ratios=[8, 1])
                self.tax = plt.subplot(gs[0])
                self.eax = plt.subplot(gs[1])
            else:
                # Just tasks
                self.tax = plt.subplot(111)
        else:
            # Just events
            self.eax = plt.subplot(111)
        # Color cycles here instead of init to ensure we start at the start.
        cat_colors = cycle(['#f4ccccff', '#c9daf8ff', '#fff2ccff', '#d9ead3ff', '#d9d2e9ff'])
        year_colors = cycle(['#d9d9d9ff', '#f3f3f3ff'])
        quarter_colors = cycle(['#d9d9d9ff', '#f3f3f3ff'])
        if self.begin is None:
            # Get earliest task or event
            dates = [e.time.value for e in self.events] + [t.begin.value for t in self.tasks]
            xi = np.min(dates)
        else:
            xi = self.begin.value
        if self.end is None:
            # Get latest task or event
            dates = [e.time.value for e in self.events] + [t.end.value for t in self.tasks]
            xf = np.max(dates)
        else:
            xf = self.end.value
        if plot_tasks:
            self.tax.set_xlim(xi, xf)
            self.tax.get_xaxis().set_ticks([])
            self.tax.get_yaxis().set_ticks([])
            [i.set_linewidth(linewidth) for i in self.tax.spines.itervalues()]
            # set up header
            y_header = 0.9  # TODO: determine location programatically
            self.tax.axhline(y=y_header, color='k', linewidth=linewidth)
            qs = ['1 Jan ', '1 April ', '1 July ', '1 Oct ']
            for year in range(to_datetime(xi).year, to_datetime(xf).year + 1):
                # Shades and text for years
                left = np.max([xi, to_datetime(str(year)).value])
                right = np.min([xf, to_datetime(str(year + 1)).value])
                p = patches.Rectangle((left, y_header), right - left, 1 - y_header,
                                      fc=year_colors.next(), ec='none')
                self.tax.add_patch(p)
                self.tax.axvline(x=left, ymin=y_header, ymax=1, color='k', linewidth=linewidth)
                self.tax.text((left + right) / 2., (y_header + 1) / 2., str(year),
                              verticalalignment='center', horizontalalignment='center')
                # Shaded quarters
                for q in qs:
                    left = np.max([xi, to_datetime(q + str(year)).value])
                    right = np.min([xf, to_datetime(q + str(year + 1)).value])
                    p = patches.Rectangle((left, 0), right - left, y_header,
                                          fc=quarter_colors.next(), ec='none')
                    self.tax.add_patch(p)
        if plot_events:
            self.eax.get_yaxis().set_ticks([])
            self.fig.autofmt_xdate()
            self.eax.yaxis.set_visible(False)
            self.eax.spines['right'].set_visible(False)
            self.eax.spines['left'].set_visible(False)
            self.eax.spines['top'].set_visible(False)
            self.eax.xaxis.set_ticks_position('bottom')
            years = [to_datetime(str(y)) for y in range(to_datetime(xi).year,
                                                        to_datetime(xf).year + 1)]
            self.eax.set_xticks(years)
            self.eax.xaxis.set_minor_locator(AutoMinorLocator())
            self.eax.set_xlim(to_datetime(xi), to_datetime(xf))
            self.eax.set_ylim(0, 2)
            self.eax.tick_params('x', length=15, width=linewidth, which='major',
                                 direction='inout')
            self.eax.tick_params('x', length=7, width=linewidth, which='minor',
                                 direction='inout')
            self.eax.set_xticklabels([])

        # Loop through categories, plot tasks and events
        nrows = self.sort_tasks()
        ncats = self.count_categories()
        ntcats = self.count_categories(ecount=False)
        necats = self.count_categories(tcount=False)
        if plot_tasks:
            dy = (y_header - buffsize * (1 + ntcats)) / nrows
        for ci, category in enumerate(self.categories):
            ctasks = [t for t in self.tasks if t.category is category]
            cevents = [e for e in self.events if e.category is category]
            if len(ctasks) or len(cevents):
                fc = self.categories[category].color
                if fc is None:
                    fc = cat_colors.next()
            if len(ctasks) > 0:
                for task in ctasks:
                    xmin = float(task.begin.value - xi) / (xf - xi)
                    ymin = float(y_header - dy * (task.row + 1) - buffsize * ci)
                    dx = float(task.end.value - task.begin.value) / (xf - xi)
                    fp = patches.FancyBboxPatch((xmin, ymin), dx, dy,
                                                boxstyle='round,pad=0,rounding_size=' + str(rounding_size),
                                                fc=fc, ec='k', transform=self.tax.transAxes)
                    self.tax.add_patch(fp)
                    self.tax.text(xmin + dx / 2., ymin + dy / 2., task.desc,
                                  verticalalignment='center', horizontalalignment='center',
                                  transform=self.tax.transAxes)
            if len(cevents) > 0:
                for event in cevents:
                    self.eax.scatter(event.time, 1.3, c=fc, marker='d', s=150,
                                     edgecolors='k')
                    self.eax.text(event.time, -0.5, event.desc, verticalalignment='top',
                                  horizontalalignment='right', rotation=30)
        plt.show()

    def save(self, filename='timeline.pkl'):
        if filename.split('.')[-1] != 'pkl':
            filename += '.pkl'
        with open(filename, 'wb') as f:
            outp = pkl.Pickler(f)
            outp.dump(self)
