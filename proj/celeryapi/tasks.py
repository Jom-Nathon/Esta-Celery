
from celery import shared_task

from .tests import getPlotInfo
import itertools as itertools



def region_to_list():
    region = []
    with open('region_List.txt', encoding='utf8') as regionFile:
        for key,group in itertools.groupby(regionFile,lambda line: line.startswith('/\n')):
            if not key:
                region = list(group)
                region = list(map(lambda each:each.strip('/'), region))
                region = list(map(lambda each:each.strip('\n'), region))
                return region

@shared_task
def add(x, y):
    return x + y


@shared_task
def getArea(area):
    return getPlotInfo(area)

