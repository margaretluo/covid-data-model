import csv
import logging
import numpy as np
import pandas as pd
import pprint
import datetime

beds = pd.read_csv("data/beds.csv")
populations = pd.read_csv("data/populations.csv")


r0_initial = 2.8
hospitalization_rate = .05
case_fatality_rate = .015
hospital_capacity_change_daily_rate = 1.05
initial_hospital_bed_utilization = .5

model_interval = 4
previous_snapshots = 3

logging.basicConfig(level=logging.DEBUG)

def get_population(province_state, country_region):
    matching_pops = populations[(populations["Province/State"] == province_state) & (populations["Country/Region"] == country_region)]
    return int(matching_pops.iloc[0].at["Population"])

def get_beds(province_state, country_region):
    matching_beds = beds[(beds["Province/State"] == province_state) & (beds["Country/Region"] == country_region)]
    beds_per_mille = matching_beds.iloc[0].at["Beds Per 1000"]
    return int(beds_per_mille * get_population(province_state, country_region) / 1000)

def get_snapshot(date, province_state, country_region):
    snapshot_filename = 'data/{}.csv'.format(date.strftime('%m-%d-%Y'))
    logging.debug('Loading: {}'.format(snapshot_filename))
    full_snapshot = pd.read_csv(snapshot_filename)
    filtered_snapshot = full_snapshot[(full_snapshot["Province/State"] == province_state) & (full_snapshot["Country/Region"] == country_region)]
    pprint.pprint(filtered_snapshot)
    return filtered_snapshot

def forecast_region(province_state, country_region):
    logging.info('Building results for {} in {}'.format(province_state, country_region))
    pop = get_population(province_state, country_region)
    beds = get_beds(province_state, country_region)
    logging.debug('This location has {} beds for {} people'.format(beds, pop))

    logging.debug('Loading daily report from {} days ago'.format(model_interval))

    # @TODO: See if today's data is already available.

    snapshots = []

    snapshot_date = datetime.date.today() - datetime.timedelta(days=1)

    snapshots.append(get_snapshot(snapshot_date, province_state, country_region))

    for i in range(0, previous_snapshots):
        snapshot_date -= datetime.timedelta(days=model_interval)
        snapshots.insert(0, get_snapshot(snapshot_date, province_state, country_region))

    pprint.pprint(snapshots)


forecast_region('California', 'US')