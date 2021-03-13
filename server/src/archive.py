  # spatial records

    def build_stat_geojson(self, neighborhoods_geojson_content, df, info_col, all_null=False):

        def get_stat(feat, stat):
            if all_null:
                return None
            return None if feat.get('properties').get(
                'nhood') not in df.index.tolist() else round(df[feat.get('properties').get('nhood')], 2)

            # return None if feat.get('properties').get(
            #     'nhood') not in df.index.tolist() else df.loc[feat.get('properties').get('nhood'), stat]

        neighborhoods_stats = {
            "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {
                                "id": uuid.uuid4().hex,
                                "nhood": feature.get('properties').get('nhood'),
                                info_col: get_stat(feature, info_col)
                            },
                            "geometry": {
                                "type": "MultiPolygon",
                                "coordinates": feature.get('geometry').get('coordinates')

                            }
                        }
                        for feature in neighborhoods_geojson_content.get('features')
                    ]
        }
        return neighborhoods_stats

    def type_records(self, table, start, end):
        # timestamp, location, longitude, class, description (optional)

        def is_null(val):

            return (val is None) or (val == 'None')

        def all_null(dic):

            res = False
            if any([is_null(dic.get(e)) for e in (self.spatialcols + ['classification'])]):
                res = True

            return res

        def get_disposiiton(name):

            if self.get_present(['clearance_description'], name):
                return 'clearance_description AS description'
            if self.get_present(['disposition'], name):
                return 'disposition AS description'
            return None

        req_col = self.spatialcols + ['classification', 'type', 'description']
        curr_col = self.get_present(table, req_col)
        if not all(e in curr_col for e in self.spatialcols) or len(curr_col) <= 3:
            return []

        type_cols = {
            ('classification'): ['classification', get_disposiiton(table)],
            ('type'): ['type AS classification', get_disposiiton(table)],
            ('description'): ['description AS classification', get_disposiiton(table)],
            ('classification', 'type'): ['classification', 'type AS description'],
            ('classification', 'description'): ['classification', 'description'],
            ('description', 'type'): ['type AS classification', 'description'],
            ('classification', 'description', 'type'): ['classification', 'description']

        }

        temp = list(set(curr_col) - set(self.spatialcols))
        temp.sort()
        temp = tuple(temp)

        col = type_cols.get(temp, None) + self.spatialcols
        col = [e for e in col if not is_null(e)]
        ts_bounds = self.timestamp_bounds(start, end)

        qry = f"SELECT {', '.join(col)} FROM {table} \
                WHERE timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]} \
                ORDER BY date DESC"

        # Filter none values
        lst = self.sql.get(qry)
        lst = [e for e in lst if not all_null(e)]

        return lst

    def priorityassignment_records(self, table, start, end):
        # timestamp, priority, class

        def contains_null(dic):

            res = False
            for e in self.spatialcols + ['classification']:
                if (dic.get(e) is None) or (dic.get(e) == 'None'):
                    res = True
                    break

            return res

        req_col = self.spatialcols + ['priority', 'classification', 'type']
        curr_col = self.get_present(table, req_col)
        if (not all(e in curr_col for e in self.spatialcols+['priority'])) or ('classification' not in curr_col and 'type' not in curr_col):
            return []
        if 'classification' not in curr_col:
            curr_col.remove('type')
            curr_col.append('type AS classification')
        ts_bounds = self.timestamp_bounds(start, end)

        qry = f"SELECT {', '.join(curr_col)} FROM {table} \
                WHERE timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]} \
                ORDER BY date DESC"

        # Filter none values
        lst = self.sql.get(qry)
        lst = [e for e in lst if not contains_null(e)]

        return lst

    def duration_records(self, table, start, end, col, calc_col):
        # timestamp, location, longitude, col

        def contains_null(dic):

            res = False
            for e in req_col:
                if (dic.get(e) is None) or (dic.get(e) == 'None'):
                    res = True
                    break

            return res

        def config(dic):

            duration = self.convert_timestamp_to_seconds(
                dic.get(col[0])) - self.convert_timestamp_to_seconds(dic.get('timestamp'))

            dic[calc_col] = normalize(duration)
            dic.pop(col[0])
            return dic

        def normalize(value):

            norm_value = (value - min)/(max-min)
            return norm_value

        extremas = self.extrema_response(table, start, end, calc_col)
        min = extremas.get("min")
        max = extremas.get("max")
        if min is None or max is None:
            return []

        req_col = self.spatialcols + col
        if req_col != self.get_present(table, req_col):
            return []
        ts_bounds = self.timestamp_bounds(start, end)
        qry = f"SELECT {', '.join(req_col)} FROM {table} \
                WHERE timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]} \
                ORDER BY date DESC"

        # Filter none values
        lst = self.sql.get(qry)

        lst = [e for e in lst if not contains_null(e)]
        # configure each record: convert to seconds and normalize
        lst = [y for y in (config(e) for e in lst) if y]

        return self.build_geojson(lst, calc_col)

    def arrival_records(self, table, start, end):
        return self.duration_records(table, start, end, ['timestamp_arrival'], 'arrival_time')

    def dispatch_records(self, table, start, end):
        return self.duration_records(table, start, end, ['timestamp_dispatch'], 'dispatch_time')

    def closed_records(self, table, start, end):
        return self.duration_records(table, start, end, ['timestamp_closed'], 'closed_time')

    def source_records(self, table, start, end):
        # timestamp, location, longitude, source

        def contains_null(dic):

            for e in req_col:
                if (dic.get(e) is None) or (dic.get(e) == 'None'):
                    return True

            return False

        req_col = ['source'] + self.spatialcols
        if req_col != self.get_present(table, req_col):
            return []
        ts_bounds = self.timestamp_bounds(start, end)
        qry = f"SELECT {', '.join(req_col)} FROM {table} \
                WHERE timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]} \
                ORDER BY date DESC"

        # Filter none values
        lst = self.sql.get(qry)
        lst = [e for e in lst if not contains_null(e)]

        return lst

    # old statistics

    def get_present(self, table, col):

        qry = f"PRAGMA table_info({table})"
        lst = self.sql.get(qry)
        names = [e.get('name') for e in lst]
        present = [e for e in col if e in names]
        return present

    def mean_time_between(self, table, start, end):

        ts_bounds = self.timestamp_bounds(start, end)
        req_col = ['timestamp']
        if not (req_col == self.get_present(table, req_col)):
            return None
        where = ['timestamp IS NOT NULL', "timestamp <> 'None'", 'timestamp > 0', 'timestamp <> 0']
        qry = f"CREATE TABLE OrderedDates AS SELECT TOSECONDS(timestamp) AS ts FROM {table} \
        WHERE {' AND '.join(where)} AND(timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]}) \
           ORDER BY timestamp ASC"
        self.sql.run(qry)

        qry = "SELECT AVG (t1.ts - t2.ts) \
              AS Avg FROM OrderedDates t1 INNER JOIN OrderedDates t2 on t1.oid = t2.oid + 1"
        res = self.sql.get(qry)[0].get("Avg")

        self.sql.run("DROP TABLE OrderedDates")
        if res == None:
            return None

        # merge the changes - this doesn't have the geojson
        # handles cities that don't have timestamp for now
        try:
            return round(res, 3)
        #    not using time.strftime("%H:%M:%S", time.gmtime(res)) since some > 24 hrs
        except:
            return None

    def top_five_classes(self, table, start, end):
        def contains_null(dic):

            res = False
            for e in cols:
                if (dic.get(e) is None) or (dic.get(e) == 'None'):
                    res = True
                    break
            return res

        def configure(dic):
            new_dic = {'classification': dic.get('classification'),
                       'percentage': round(dic.get('count')*100/total_calls, 3)}
            return new_dic

        ts_bounds = self.timestamp_bounds(start, end)
        if not (self.get_present(['classification'], table) == ['classification']):
            return None
        cols = ['classification', 'count']
        qry = f"SELECT COUNT(*) AS num FROM {table} WHERE (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]})"
        total_calls = self.sql.get(qry)[0].get('num')
        if not total_calls:
            return None
        where = ['classification IS NOT NULL', 'classification <> "None"']
        qry = f"SELECT classification, COUNT(*) as count \
               FROM {table} WHERE {' AND '.join(where)} AND (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]}) \
               GROUP BY classification \
               ORDER BY COUNT(*) DESC LIMIT 5"
        lst = self.sql.get(qry)
        lst = [e for e in lst if not contains_null(e)]
        lst = [configure(e) for e in lst]
        return lst

    def mean_response_by_priority(self, table, start, end):

        # still need to map non-integer priorities to integer!
        def clean_dict(dict):
            if dict.get('response_time') == None or dict.get('response_time') == 'None':
                return None
            response_seconds = time.gmtime(dict.get('response_time'))
            dict['response_time'] = time.strftime("%H:%M:%S", response_seconds)
            return dict
        req_col = ['priority', 'time_arrival']
        if req_col != self.get_present(table, req_col):
            return None

        ts_bounds = self.timestamp_bounds(start, end)
        where = ['timestamp<>0', 'timestamp IS NOT NULL', "timestamp<>'None'",
                 'timestamp_arrival<>0', 'timestamp_arrival IS NOT NULL', "timestamp_arrival<>'None'",
                 'timestamp_arrival - timestamp > 0', "priority<>'None'", "priority<>-1", 'priority IS NOT NULL'
                 ]

        qry = f"SELECT priority, AVG (TOSECONDS(timestamp_arrival) - TOSECONDS(timestamp)) AS response_time \
        FROM {table} WHERE {' AND '.join(where)} AND (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]}) \
        GROUP BY priority ORDER BY priority ASC"
        lst = self.sql.get(qry)

        # convert seconds to time format (hh:mm:ss)
        lst = [clean_dict(dict) for dict in lst]
        lst = [e for e in lst if e]

        return lst

    def count_incident(self, table, start, end, incident):

        def get_filters():

            table_config = configs.specific_incident_config.get(table)
            if table_config == None:
                return None
            incident_config = table_config.get(incident)
            if incident_config == None:
                return None
            where = [
                f"{incident_config.get('source')} LIKE '%{e}%'" for e in incident_config.get('contains')]
            return where

        ts_bounds = self.timestamp_bounds(start, end)
        col = ['COUNT(*) AS count']
        where = get_filters()
        if where == None:
            return -1

        qry = f"SELECT {', '.join(col)} FROM {table} \
                WHERE ({' OR '.join(where)}) AND (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]})"

        lst = self.sql.get(qry)

        res = lst[0].get('count')
        return res

    def change_incident(self, table, start, end, incident):

        prev_start_date = (parser.parse(start).date() -
                           datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        prev_end_date = (parser.parse(end).date() -
                         datetime.timedelta(days=365)).strftime('%Y-%m-%d')

        curr_count = self.count_incident(table, start, end, incident)
        prev_count = self.count_incident(table, prev_start_date, prev_end_date, incident)
        if curr_count == -1 or prev_count == -1 or prev_count == 0:
            return -1
        percent_change = (curr_count - prev_count)/prev_count * 100
        return percent_change

    def priority_incident(self, table, start, end, incident):

        def get_filters():

            table_config = configs.specific_incident_config.get(table)
            if table_config == None:
                return None
            incident_config = table_config.get(incident)
            if incident_config == None:
                return None
            where = [
                f"{incident_config.get('source')} LIKE '%{e}%'" for e in incident_config.get('contains')]
            return where
        present_priority = self.get_present(['priority'], table)

        if not present_priority:
            return -1
        ts_bounds = self.timestamp_bounds(start, end)
        col = ['AVG(priority) AS avg']
        where = get_filters()
        if where == None:
            return -1
        null_checks = ["priority<>'None'", 'priority IS NOT NULL', 'priority<>-1']

        qry = f"SELECT {', '.join(col)} FROM {table} \
                WHERE ({' OR '.join(where)}) AND ({' AND '.join(null_checks)}) AND (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]})"

        lst = self.sql.get(qry)

        res = lst[0].get('avg')
        if res == None:
            return -1
        return res

    def mean_duration(self, table, start, end, req_col):

        if req_col != self.get_present(table, req_col):
            return None
        ts_bounds = self.timestamp_bounds(start, end)
        null_checks = [f'{req_col[0]}<>0', f'{req_col[0]} IS NOT NULL', f"{req_col[0]}<>'None'",
                       f'{req_col[1]}<>0', f'{req_col[1]} IS NOT NULL', f"{req_col[1]}<>'None'",
                       f'{req_col[1]} - {req_col[0]} > 0'
                       ]

        qry = f"SELECT AVG (TOSECONDS({req_col[1]}) - TOSECONDS({req_col[0]})) AS duration \
        FROM {table} WHERE {' AND '.join(null_checks)} AND (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]})"
        lst = self.sql.get(qry)

        res = lst[0].get('duration')
        if res == None:
            return None
        # convert from seconds to '%H:%M:%S'
        seconds = time.gmtime(res)
        res = time.strftime("%H:%M:%S", seconds)
        return res

    def mean_response(self, table, start, end):

        return self.mean_duration(table, start, end, ['timestamp', 'timestamp_arrival'])

    def mean_completion(self, table, start, end):

        return self.mean_duration(table, start, end, ['timestamp', 'timestamp_closed'])

    def mean_dispatch(self, table, start, end):

        return self.mean_duration(table, start, end, ['timestamp', 'timestamp_dispatch'])

    def mean_response_dispatch(self, table, start, end):

        return self.mean_duration(table, start, end, ['timestamp_dispatch', 'timestamp_arrival'])

    def source_proportion(self, table, start, end):

        def contains_null(dic):

            res = False
            for e in cols:
                if (dic.get(e) is None) or (dic.get(e) == 'None'):
                    res = True
                    break
            return res

        def configure(dic):
            new_dic = {'source': dic.get('source'),
                       'percentage': round(dic.get('count')*100/total_calls, 3)}
            return new_dic

        req_col = ['source']
        cols = ['source', 'count']
        if req_col != self.get_present(table, req_col):
            return None
        ts_bounds = self.timestamp_bounds(start, end)
        qry = f"SELECT COUNT(*) AS num FROM {table} WHERE (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]})"
        total_calls = self.sql.get(qry)[0].get('num')
        if not total_calls:
            return None
        null_checks = ['source IS NOT NULL', 'source <> "None"']
        qry = f"SELECT source, COUNT(*) as count \
               FROM {table} WHERE (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]}) \
               GROUP BY source HAVING {' AND '.join(null_checks)}\
               ORDER BY COUNT(*) DESC"
        lst = self.sql.get(qry)
        lst = [e for e in lst if not contains_null(e)]
        lst = [configure(e) for e in lst]
        return lst

    def priority_proportion(self, table, start, end):

        def contains_null(dic):

            res = False
            for e in cols:
                if (dic.get(e) is None) or (dic.get(e) == 'None'):
                    res = True
                    break
            return res

        def configure(dic):
            new_dic = {'priority': dic.get('priority'),
                       'percentage': round(dic.get('count')*100/total_calls, 3)}
            return new_dic

        req_col = ['priority']
        cols = ['priority', 'count']
        if req_col != self.get_present(table, req_col):
            return None
        ts_bounds = self.timestamp_bounds(start, end)
        qry = f"SELECT COUNT(*) AS num FROM {table} WHERE (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]})"
        total_calls = self.sql.get(qry)[0].get('num')
        if not total_calls:
            return None
        null_checks = ['priority IS NOT NULL', 'priority <> "None"', 'priority<>-1']
        qry = f"SELECT priority, COUNT(*) AS count \
               FROM {table} WHERE (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]}) \
               GROUP BY priority HAVING {' AND '.join(null_checks)}\
               ORDER BY COUNT(*) DESC"
        lst = self.sql.get(qry)

        lst = [e for e in lst if not contains_null(e)]
        lst = [configure(e) for e in lst]
        return lst

    # data normalizations

    def extrema_response(self, table, start, end, duration_value):

        if duration_value == 'arrival_time':
            req_col = ['timestamp', 'timestamp_arrival']
        if duration_value == 'dispatch_time':
            req_col = ['timestamp', 'timestamp_dispatch']
        if duration_value == 'closed_time':
            req_col = ['timestamp', 'timestamp_closed']
        if req_col != self.get_present(table, req_col):
            return None
        ts_bounds = self.timestamp_bounds(start, end)

        null_checks = [f'{req_col[0]} IS NOT NULL', f"{req_col[0]}<>'None'",
                       f'{req_col[1]} IS NOT NULL', f"{req_col[1]}<>'None'"
                       ]

        qry = f"SELECT MIN (TOSECONDS({req_col[1]}) - TOSECONDS({req_col[0]})) AS min, MAX (TOSECONDS({req_col[1]}) - TOSECONDS({req_col[0]})) AS max \
        FROM {table} WHERE {' AND '.join(null_checks)} AND (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]})"
        # qry = f"SELECT AVG (TOSECONDS({req_col[1]}) - TOSECONDS({req_col[0]})) AS duration \
        # FROM {table} WHERE {' AND '.join(null_checks)} AND (timestamp >= {ts_bounds[0]} AND timestamp <= {ts_bounds[1]})"
        lst = self.sql.get(qry)

        min = lst[0].get('min')
        max = lst[0].get('max')
        if min == None or max == None:
            return None
        return {'min': min, 'max': max}

    # methods to handle statistics as single endpoint

    def all_stats(self, table, start, end):

        dts = self.dates_list(start, end)
        qry = f"SELECT * FROM {table} \
                WHERE date IN {dts} \
                ORDER BY timestamp DESC"
        lst = self.sql.get(qry)

        if not len(lst): return None
        return {
            "avg_between_calls": self.avg_time_between(table, lst),
            "avg_daily_calls": self.avg_daily_calls(table, lst),
            "avg_overlapping_calls": self.avg_overlap_count(table, lst),
            "avg_hourly_calls": self.avg_dispatch_per_hour(table, lst),
            "num_call_top_priority": self.highest_priority_count(table, lst, len(lst)),
            "priority_proportions": self.single_priority_proportion(table, len(lst), lst),
            "source_proportions": self.single_source_proportion(table, len(lst), lst),
            "type_top_frequency": self.single_top_five_classes(table, len(lst), lst),
            "avg_call_response_top_priority": self.single_priority_one_response(table, lst),
            "avg_dispatch": self.average_dispatch_time(table, lst),
            "hospital_response": self.average_hospital_time(table, lst),
            "arrest_rate": self.arrest_rate(table, lst),
            "resolve_time": self.resolve_time_allocations(table, lst),
            "gun_violence_calls": self.count_gun(table, lst),
            "domestic_violence_calls": self.count_domestic(table, lst),
            "burglary_calls": self.count_burglary(table, lst),
            "drug_calls": self.count_drug(table, lst),
            "disposition_frequent_calls": self.disposition_of_classes(table, lst)
        }

        # will return None for all stats that don't apply

    def single_priority_proportion(self, table, total_calls, data):

        def contains_null(lst):
            res = False
            for e in lst:
                if (e is None) or (e == 'None'):
                    res = True
                    break
            return res

        def configure(lst):
            new_dic = {'priority': lst[0],
                       'percentage': round(lst[1]*100/total_calls, 2)}
            return new_dic

        cols = ['priority']
        if cols != self.get_present(table, cols):
            return None
        df = pd.DataFrame.from_dict(data)
        if 'int' in str(df.dtypes[0]):
            check = -1
        else:
            check = "None"

        df = df[df['priority'] != check]
        df.dropna(inplace=True)
        df['priority'] = df['priority'].astype(str)
        counts = df['priority'].value_counts()
        lst = zip(counts.index, counts)
        lst = sorted(lst, key=lambda x: x[0])

        lst = [e for e in lst if not contains_null(e)]
        lst = [configure(e) for e in lst]
        return lst

    def single_source_proportion(self, table, total_calls, data):

        def contains_null(lst):
            res = False
            for e in lst:
                if (e is None) or (e == 'None'):
                    res = True
                    break
            return res

        def configure(lst):
            new_dic = {'source': lst[0],
                       'percentage': round(lst[1]*100/total_calls, 2)}
            return new_dic

        cols = ['source']
        if cols != self.get_present(table, cols):
            return None
        df = pd.DataFrame.from_dict(data)
        check = "None"
        df = df[df['source'] != check]
        df.dropna(inplace=True)
        counts = df['source'].value_counts()
        lst = zip(counts.index, counts)
        lst = sorted(lst, key=lambda x: x[1], reverse=True)

        lst = [e for e in lst if not contains_null(e)]
        lst = [configure(e) for e in lst]
        return lst

    def single_top_five_classes(self, table, total_calls, data):

        def contains_null(lst):
            res = False
            for e in lst:
                if (e is None) or (e == 'None'):
                    res = True
                    break
            return res

        def configure(lst):
            new_dic = {'classification': lst[0],
                       'percentage': round(lst[1]*100/total_calls, 2)}
            return new_dic

        cols = ['classification']
        if cols != self.get_present(table, cols):
            return None
        df = pd.DataFrame.from_dict(data)
        check = "None"
        df = df[df['classification'] != check]
        df.dropna(inplace=True)
        counts = df['classification'].value_counts()
        lst = zip(counts.index, counts)
        lst = sorted(lst, key=lambda x: x[1], reverse=True)

        lst = [e for e in lst if not contains_null(e)]
        lst = [configure(e) for e in lst][:5]
        return lst

    def avg_overlap_count(self, table, data):

        def clean_data():
            if isinstance(data, pd.DataFrame):
                df = data
            else:
                df = pd.DataFrame.from_dict(data)
            df = df[col]
            df = df.dropna()
            df = df.query(f"{col[0]}!='None' and {col[1]}!='None'")
            for e in col:
                df[e] = df[e].astype(int)
            outlier_checks = [f"{col[0]} > 0", f"{col[1]} > 0", f"{col[0]} - {col[1]} > 0"]
            df = df.query(' and '.join(outlier_checks))
            return df

        col = ['timestamp_closed', 'timestamp']
        if col != self.get_present(table, col):
            return None

        df = clean_data()
        if df.empty:
            return 0

        start = [(e, True) for e in df['timestamp']]
        end = [(e, False) for e in df['timestamp_closed']]
        timestamps = (start+end)
        timestamps.sort(key=lambda r: r[0])
        curr_count, overlaps = 0, []
        for e in timestamps:
            if e[1]:
                curr_count += 1
            else:
                curr_count -= 1
            overlaps.append(curr_count)
        return round(sum(overlaps)/len(overlaps), 2)

    def single_priority_one_response(self, table, data, ret_df=False):
        # returns the average response time (enroute time) for calls for service classified as having the highest priority
        def clean_data():
            if isinstance(data, pd.DataFrame):
                df = data
            else:
                df = pd.DataFrame.from_dict(data)
            df = df.dropna()
            df = df.query(f"{col[0]}!='None' and {col[1]}!='None'")
            for e in col[:2]:
                df[e] = df[e].astype(int)
            null_checks = [f"{col[0]} > 0", f"{col[1]} > 0", f"{col[0]} - {col[1]} > 0"]
            df = df.query(' and '.join(null_checks))
            return df

        col = ['timestamp_arrival', 'timestamp_dispatch', 'priority']
        highest = configs.highest_priority_config.get(table)
        if col != self.get_present(table, col) or highest is None:
            if ['response'] == self.get_present(table, ['response']):
                return self.alt_priority_one_response(table, data, ret_df)
            return None

        df = clean_data()
        if df.empty:
            return None

        df[col[2]] = df[col[2]].astype(str)
        qry = " or ".join([f"{col[2]} == '{e}'" for e in highest])
        df = df.query(qry)
        if df.empty:
            return None
        res_col = 'response'
        df[res_col] = df[col[0]] - df[col[1]]
        if ret_df:
            return df
        mean, median, std, minimum, maximum = df[res_col].mean(), df[res_col].median(
        ), df[res_col].std(), float(df[res_col].min()), float(df[res_col].max())
        within_four = sum(df[res_col] <= 240) / df.count()[res_col] * 100
        # return {"mean": round(mean, 2), "median": median, "standard deviation": round(std, 2), "percent_within_four_minutes": round(within_four, 2), "minimum": minimum, "maximum": maximum}
        return round(mean, 2)

    def alt_priority_one_response(self, table, data, ret_df):
        # returns the average response time (enroute time) for calls for service classified as having the highest priority

        def clean_data():
            df = pd.DataFrame.from_dict(data)
            df = df.dropna()
            df = df.query(f"{col[0]}!='None' and {col[1]}!='None'")
            df[col[0]] = df[col[0]].astype(int)
            null_checks = [f"{col[0]} > 0"]
            df = df.query(' and '.join(null_checks))
            return df

        col = ['response', 'priority']
        highest = configs.highest_priority_config.get(table)
        if col != self.get_present(table, col) or highest is None:
            return None

        df = clean_data()
        if df.empty:
            return None

        df[col[1]] = df[col[1]].astype(str)
        qry = " or ".join([f"{col[1]} == '{e}'" for e in highest])
        df = df.query(qry)
        if df.empty:
            return None
        res_col = 'response'
        if ret_df:
            return df
        mean, median, std, min, max = df[res_col].mean(), df[res_col].median(
        ), df[res_col].std(), df[res_col].min(), df[res_col].max()
        within_five = sum(df[res_col] <= 300) / df.count()[res_col] * 100
        return {"mean": round(mean, 2), "median": median, "standard deviation": round(std, 2), "percent_within_five_minutes": round(within_five, 2), 'minimum': min, 'maximum': max}

    def resolve_time_allocations(self, table, data):

        def clean_data():
            df = pd.DataFrame.from_dict(data)
            df = df[col]
            df = df.dropna()
            df = df.query(f"{col[0]}!='None' and {col[1]}!='None' and {col[2]}!='None'")
            for e in col[:2]:
                df[e] = df[e].astype(int)
            outlier_checks = [f"{col[0]} > 0", f"{col[1]} > 0", f"{col[1]} - {col[0]} >= 0"]
            df = df.query(' and '.join(outlier_checks))
            return df

        def format(sec):

            minutes = sec // 60
            hours = minutes // 60
            string = "%04d" % (hours)
            return string

        col = ['timestamp', 'timestamp_closed', 'classification']
        if col != self.get_present(table, col):
            return None
        df = clean_data()
        if df.empty:
            return None
        res_col = 'resolve'
        df[res_col] = df[col[1]] - df[col[0]]
        tot = df[res_col].sum()
        s = df.groupby(['classification']).sum()[res_col]
        num_series = df.groupby(['classification']).count()[res_col]
        if df.empty:
            return None
        s = s.sort_values(ascending=False)[:10]

        dic = {k: {"hours spent resolving": format(v), "percentage of total time": round(v*100/tot, 2), "number of calls": (int)(num_series[k])}
               for k, v in list(zip(s.index, s))}
        return dic

    def arrest_rate(self, table, data):

        def clean_data():
            df = pd.DataFrame.from_dict(data)
            df = df.dropna()
            df = df.query(f"{col[0]}!='None'")
            return df

        config = configs.arrest_config.get(table)
        if config is None:
            return None
        col = [config.get('source')]
        filters = config.get('contains')

        df = clean_data()
        if df.empty:
            return None
        total = df.count()[col[0]]

        qry = " or ".join([f"{col[0]}.str.contains('{e}', case=False)" for e in filters])
        df = df.query(qry, engine='python')
        if df.empty:
            count = 0
        else:
            count = df.count()[col[0]]
        arrest_rate = round(count/total * 100, 2)
        return arrest_rate

    def disposition_of_classes(self, table, data):

        # only have it work where stat can be calculated
        # clean the Data and take out the columns you need
        # group by class, and for each of these groups find the 3 most common dispositions and their percentage
        def clean_data():
            df = pd.DataFrame.from_dict(data)
            df = df[col]
            df = df.dropna()
            df = df.query(f"{col[0]}!='None' and {col[1]}!='None'")
            return df

        def top_five(group):
            counts = group.size()
            counts.sort_values(ascending=False, inplace=True)
            index = counts[:5].index
            return index

        config = configs.arrest_config.get(table)
        if config is None:
            return None
        col = [config.get('source'), 'classification']
        present = self.get_present(table, col)
        for e in col:
            if e not in present:
                return None

        df = clean_data()
        if df.empty:
            return None
        by_class = df.groupby(col[1], sort=False)
        index = top_five(by_class)

        lst = []
        for e in index:
            class_df, dic = by_class.get_group(e), {}
            num = class_df.shape[0]
            class_df = class_df[class_df[col[0]] != '-']
            dic.update({'classification': e})
            percents = round(class_df[col[0]].value_counts()[:3]/num * 100, 2)
            disp_lst = []
            for k, v in list(zip(percents.index, percents)):
                disp_lst.append({'disposition': k, 'percentage': v})
            dic.update({'top': disp_lst})
            lst.append(dic)
        return lst

    def highest_priority_count(self, table, data, total_calls=None, ret_df=False):

        def clean_data():
            df = pd.DataFrame.from_dict(data)
            df = df.dropna()
            df = df.query(f"{col[0]}!='None'")
            return df

        col = ['priority']
        highest = configs.highest_priority_config.get(table)
        if col != self.get_present(table, col) or highest is None:
            return None

        df = clean_data()
        if df.empty:
            return None

        df[col[0]] = df[col[0]].astype(str)
        qry = " or ".join([f"{col[0]} == '{e}'" for e in highest])
        df = df.query(qry)
        if ret_df:
            return df
        if df.empty:
            count = 0
        else:
            count = (int)(df.count()[col[0]])
        dic = {"count": count, "percentage": round(count/total_calls * 100, 2)}
        return dic

    def average_dispatch_time(self, table, data, ret_df=False):

        def clean_data():
            if isinstance(data, pd.DataFrame):
                df = data
            else:
                df = pd.DataFrame.from_dict(data)
            df = df.dropna()
            df = df.query(f"{col[0]}!='None' and {col[1]}!='None'")
            for e in col:
                df[e] = df[e].astype(int)
            null_checks = [f"{col[0]} > 0", f"{col[1]} > 0", f"{col[0]} - {col[1]} > 0"]
            df = df.query(' and '.join(null_checks))
            return df

        col = ['timestamp_dispatch', 'timestamp']
        if col != self.get_present(table, col):
            if ['dispatch'] == self.get_present(table, ['dispatch']):
                return self.alt_dispatch_time(table, data, ret_df)
            return None

        df = clean_data()
        if df.empty:
            return None

        res_col = 'dispatch_time'
        df[res_col] = (df[col[0]] - df[col[1]])//60
        if ret_df:
            return df

        mean, median, std, minimum, maximum = df[res_col].mean(), df[res_col].median(
        ), df[res_col].std(), float(df[res_col].min()), float(df[res_col].max())
        # return {"mean": round(mean, 2), "median": median, "standard deviation": round(std, 2), "minimum": minimum, "maximum": maximum}
        return round(mean, 2)

    def call_count(self, table, data):
        count = data.shape[0]
        return float(count)

    def alt_dispatch_time(self, table, data, ret_df):

        def clean_data():
            df = pd.DataFrame.from_dict(data)
            df = df.dropna()
            df = df.query(f"{col[0]}!='None'")
            df[col[0]] = df[col[0]].astype(int)
            null_checks = [f"{col[0]} > 0"]
            df = df.query(' and '.join(null_checks))
            return df

        col = ['dispatch']
        if col != self.get_present(table, col):
            return None

        df = clean_data()
        if df.empty:
            return None

        res_col = 'dispatch_time'
        df[res_col] = df[res_col]//60
        if ret_df:
            return df
        mean, median, std, minimum, maximum = df[res_col].mean(), df[res_col].median(
        ), df[res_col].std(), float(df[res_col].min()), float(df[res_col].max())
        return {"mean": round(mean, 2), "median": median, "standard deviation": round(std, 2), "minimum": minimum, "maximum": maximum}

    def avg_time_between(self, table, data):

        def clean_data():
            df = pd.DataFrame.from_dict(data)
            df = df.dropna()
            df = df.query(f"{col[0]}!='None'")
            df[col[0]] = df[col[0]].astype(int)
            null_checks = [f"{col[0]} > 0"]
            df = df.query(' and '.join(null_checks))
            df = df.sort_values(col[0], ascending=True, inplace=False)
            return df
        col = ['timestamp']
        df = clean_data()
        if df.empty:
            return None
        mean = df[col[0]].diff().dropna().mean()
        return round(mean, 2)

    def avg_daily_calls(self, table, data):

        def clean_data():
            df = pd.DataFrame.from_dict(data)
            df = df.dropna()
            df = df.query(f"{col[0]}!='None'")

            return df

        col = ['date']
        df = clean_data()
        if df.empty: return None
        mean = df.groupby('date').size().mean()
        mean = (int)(mean)
        return round(float(mean))

    def avg_dispatch_per_hour(self, table, data):

        def clean_data():
            df = pd.DataFrame.from_dict(data)
            df = df.dropna()
            df = df.query(f"{col[0]}!='None' and {col[1]}!='None'")
            return df

        col = ['date_dispatch', 'time_dispatch']
        if col != self.get_present(table, col):
            return None
        df = clean_data()
        if df.empty:
            return float(0)
        df['hour'] = df['time_dispatch'].apply(lambda x: parser.parse(str(x)).strftime('%H'))
        mean = df.groupby(["date_dispatch", "hour"]).size().mean()
        return round(float(mean), 2)

    def average_hospital_time(self, table, data):

        def clean_data():
            df = pd.DataFrame.from_dict(data)
            df = df.dropna()
            df = df.query(f"{col[0]}!='None' and {col[1]}!='None'")
            for e in col:
                df[e] = df[e].astype(int)
            null_checks = [f"{col[0]} > 0", f"{col[1]} > 0", f"{col[0]} - {col[1]} > 0"]
            df = df.query(' and '.join(null_checks))
            return df

        col = ['timestamp_hospital', 'timestamp_dispatch']
        if col != self.get_present(table, col):
            return None

        df = clean_data()
        if df.empty:
            return None

        res_col = 'hospital_time'
        df[res_col] = (df[col[0]] - df[col[1]])//60
        mean, median, std, minimum, maximum = df[res_col].mean(), df[res_col].median(
        ), df[res_col].std(), float(df[res_col].min()), float(df[res_col].max())
        return {"mean": round(mean, 2), "median": median, "standard deviation": round(std, 2),  "minimum": minimum, "maximum": maximum}

    def count_incident(self, table, data, incident):

        def clean_data():
            df = pd.DataFrame.from_dict(data)
            df = df.dropna()
            df = df.query(f"{col[0]}!='None' and {col[1]}!='None'")
            return df

        city_config = configs.specific_incident_config.get(table)
        if city_config is None:
            return None
        incident_config = city_config.get(incident)
        if incident_config is None:
            return None
        col = [incident_config.get('source'), 'time']
        if col != self.get_present(table, col):
            return None

        df = clean_data()
        if df.empty:
            return None
        qry = " or ".join(
            [f"{col[0]}.str.contains('{e}', case=False)" for e in incident_config.get('contains')])
        df = df.query(qry, engine='python')
        if df.empty:
            count = 0
            common_time = None
        else:
            count = (int)(df.count()[col[0]])
            df['hour'] = df['time'].apply(lambda x: parser.parse(str(x)).strftime('%H'))
            s = df['hour'].value_counts().sort_values(ascending=False)
            common_time = s.index[0]

        return {'count': float(count), "most_common_hour": (int)(common_time)}

    def count_gun(self, table, data):

        return self.count_incident(table, data, "shooting")

    def count_domestic(self, table, data):

        return self.count_incident(table, data, "domestic_violence")

    def count_drug(self, table, data):

        return self.count_incident(table, data, "drugs")

    def count_burglary(self, table, data):

        return self.count_incident(table, data, "burglary")

    # methods to return geojson response of statistics by district

    def district_count(self, table, start, end):

        nhood_geojson = self.get_nhood_geojson(table)
        if nhood_geojson == None:
            return None
        col = ['timestamp', 'latitude', 'longitude']
        if col != self.get_present(table, col):
            return self.build_stat_geojson(nhood_geojson, None, 'call_count', all_null=True)

        def grab_data():
            u, v = self.dates_to_timestamps(start, end)
            qry = f"SELECT timestamp, latitude, longitude FROM {table} \
                    WHERE timestamp >= {u} AND timestamp <= {v} \
                    ORDER BY timestamp DESC"

            lst = self.sql.get(qry)
            return lst

        def apply_stat(df):
            count_per_neighborhood = df['nhood'].value_counts()
            return count_per_neighborhood.astype(float)

        # get all the data you need to calculate stats
        data = grab_data()
        if not data:
            return self.build_stat_geojson(nhood_geojson, None, 'call_count', all_null=True)

        # merge the data with the geojson so every call is associated w/ a district
        df = self.map_rows_to_neighborhoods(data, table, nhood_geojson)
        if df.empty:
            return self.build_stat_geojson(nhood_geojson, None, 'call_count', all_null=True)
        # return a series indexed by neighborhood where the statistic has been applied on the calls from each neighborhood
        stat_srs = apply_stat(df)
        return self.build_stat_geojson(nhood_geojson, stat_srs, 'call_count')

    def district_mean_dispatch(self, table, start, end):

        nhood_geojson = self.get_nhood_geojson(table)
        if nhood_geojson == None:
            return None
        col = ['timestamp', 'latitude', 'longitude']
        if col != self.get_present(table, col):
            return self.build_stat_geojson(nhood_geojson, None, 'mean_dispatch_time_minutes', all_null=True)

        def grab_data():

            u, v = self.dates_to_timestamps(start, end)
            qry = f"SELECT timestamp_dispatch, timestamp, latitude, longitude FROM {table} \
                    WHERE timestamp >= {u} AND timestamp <= {v} \
                    ORDER BY timestamp DESC"

            lst = self.sql.get(qry)
            return lst

        # get all the data you need to calculate stats
        data = grab_data()
        if not data:
            return self.build_stat_geojson(nhood_geojson, None, 'mean_dispatch_time_minutes', all_null=True)

        df = self.average_dispatch_time(table, data, True)
        if type(df) == type(None) or df.empty:
            return self.build_stat_geojson(nhood_geojson, None, 'mean_dispatch_time_minutes', all_null=True)

        # merge the data with the geojson so every call is associated w/ a district
        df = self.map_rows_to_neighborhoods(df, table, nhood_geojson)
        if df.empty:
            return self.build_stat_geojson(nhood_geojson, None, 'mean_dispatch_time_minutes', all_null=True)

        # return a series indexed by neighborhood where the statistic has been applied on the calls from each neighborhood
        stat_srs = df.groupby('nhood').mean()['dispatch_time']
        return self.build_stat_geojson(nhood_geojson, stat_srs, 'mean_dispatch_time_minutes')

    def district_mean_response(self, table, start, end):

        stat_name = 'mean_response_time_emergency_seconds'
        nhood_geojson = self.get_nhood_geojson(table)
        if nhood_geojson == None:
            return None
        col = ['priority', 'latitude', 'longitude']
        if col != self.get_present(table, col):
            return self.build_stat_geojson(nhood_geojson, None, stat_name, all_null=True)

        def grab_data():

            u, v = self.dates_to_timestamps(start, end)
            qry = f"SELECT timestamp_dispatch, timestamp_arrival, priority, latitude, longitude FROM {table} \
                    WHERE timestamp >= {u} AND timestamp <= {v} \
                    ORDER BY timestamp DESC"

            lst = self.sql.get(qry)
            return lst

        # get all the data you need to calculate stats
        data = grab_data()
        if not data:
            return self.build_stat_geojson(nhood_geojson, None, stat_name, all_null=True)

        df = self.single_priority_one_response(table, data, True)
        if type(df) == type(None) or df.empty:
            return self.build_stat_geojson(nhood_geojson, None, stat_name, all_null=True)

        # merge the data with the geojson so every call is associated w/ a district
        df = self.map_rows_to_neighborhoods(df, table, nhood_geojson)
        if df.empty:
            return self.build_stat_geojson(nhood_geojson, None, stat_name, all_null=True)

        # return a series indexed by neighborhood where the statistic has been applied on the calls from each neighborhood
        stat_srs = df.groupby('nhood').mean()['response']

        return self.build_stat_geojson(nhood_geojson, stat_srs, stat_name)

    def district_emergency_count(self, table, start, end):

        stat_name = 'emergency_count'
        nhood_geojson = self.get_nhood_geojson(table)
        if nhood_geojson == None:
            return None
        col = ['priority', 'latitude', 'longitude']
        if col != self.get_present(table, col):
            return self.build_stat_geojson(nhood_geojson, None, stat_name, all_null=True)

        def grab_data():

            u, v = self.dates_to_timestamps(start, end)
            qry = f"SELECT priority, latitude, longitude FROM {table} \
                    WHERE timestamp >= {u} AND timestamp <= {v} \
                    ORDER BY timestamp DESC"

            lst = self.sql.get(qry)
            return lst

        # get all the data you need to calculate stats
        data = grab_data()
        if not data:
            return self.build_stat_geojson(nhood_geojson, None, stat_name, all_null=True)
        df = self.highest_priority_count(table, data, total_calls=None, ret_df=True)
        if type(df) == type(None) or df.empty:
            return self.build_stat_geojson(nhood_geojson, None, stat_name, all_null=True)

        # merge the data with the geojson so every call is associated w/ a district
        df = self.map_rows_to_neighborhoods(df, table, nhood_geojson)
        if df.empty:
            return self.build_stat_geojson(nhood_geojson, None, stat_name, all_null=True)

        # return a series indexed by neighborhood where the statistic has been applied on the calls from each neighborhood
        count_per_neighborhood = df['nhood'].value_counts()
        stat_srs = count_per_neighborhood.astype(float)

        return self.build_stat_geojson(nhood_geojson, stat_srs, stat_name)

    def district_hourly_dispatch(self, table, start, end):

        nhood_geojson = self.get_nhood_geojson(table)
        if nhood_geojson == None:
            return None
        col = ['date_dispatch', 'time_dispatch', 'latitude', 'longitude']
        if col != self.get_present(table, col):
            return self.build_stat_geojson(nhood_geojson, None, 'hourly_dispatch_count', all_null=True)

        def grab_data():

            u, v = self.dates_to_timestamps(start, end)
            qry = f"SELECT date_dispatch, time_dispatch, latitude, longitude FROM {table} \
                    WHERE timestamp >= {u} AND timestamp <= {v} \
                    ORDER BY timestamp DESC"

            lst = self.sql.get(qry)
            return lst

        def apply_stat(df):

            grps = df.groupby('nhood', sort=False)
            nhood_df_lst, nhood_name_lst = [group for name,
                                            group in grps], [name for name, group in grps]
            ind = {'nhood': pd.Series(nhood_name_lst)}
            stat_lst = list(map(lambda x: stat_method(table, x), nhood_df_lst))
            stat_srs = pd.Series(stat_lst).astype(float)
            stat_srs.index = nhood_name_lst
            return stat_srs

        stat_method = self.avg_dispatch_per_hour

        # get all the data you need to calculate stats
        data = grab_data()
        if not data:
            return self.build_stat_geojson(nhood_geojson, None, 'hourly_dispatch_count', all_null=True)

        # merge the data with the geojson so every call is associated w/ a district
        df = self.map_rows_to_neighborhoods(data, table, nhood_geojson)
        if df.empty:
            return self.build_stat_geojson(nhood_geojson, None, 'hourly_dispatch_count', all_null=True)

        # return a df indexed by neighborhood where the statistic has been applied on the calls from each neighborhood
        stat_srs = apply_stat(df)

        return self.build_stat_geojson(nhood_geojson, stat_srs, 'hourly_dispatch_count')

    def district_mean_overlap(self, table, start, end):

        nhood_geojson = self.get_nhood_geojson(table)
        if nhood_geojson == None:
            return None
        col = ['timestamp', 'timestamp_closed', 'latitude', 'longitude']
        if col != self.get_present(table, col):
            return self.build_stat_geojson(nhood_geojson, None, 'mean_overlap_count', all_null=True)

        def grab_data():
            u, v = self.dates_to_timestamps(start, end)
            qry = f"SELECT timestamp, timestamp_closed, latitude, longitude FROM {table} \
                    WHERE timestamp >= {u} AND timestamp <= {v} \
                    ORDER BY timestamp DESC"

            lst = self.sql.get(qry)
            return lst

        def apply_stat(df):

            grps = df.groupby('nhood', sort=False)
            nhood_df_lst, nhood_name_lst = [group for name,
                                            group in grps], [name for name, group in grps]
            ind = {'nhood': pd.Series(nhood_name_lst)}

            stat_lst = list(map(lambda x: stat_method(table, x), nhood_df_lst))
            stat_srs = pd.Series(stat_lst).astype(float)
            stat_srs.index = nhood_name_lst

            return stat_srs

        stat_method = self.avg_overlap_count

        # get all the data you need to calculate stats
        data = grab_data()
        if not data:
            return self.build_stat_geojson(nhood_geojson, None, 'mean_overlap_count', all_null=True)

        # merge the data with the geojson so every call is associated w/ a district
        df = self.map_rows_to_neighborhoods(data, table, nhood_geojson)

        # return a df indexed by neighborhood where the statistic has been applied on the calls from each neighborhood
        stat_srs = apply_stat(df)

        return self.build_stat_geojson(nhood_geojson, stat_srs, 'mean_overlap_count')

    def get_nhood_geojson(self, table):

        qry = f"SELECT nhood_geojson FROM CityCoordinates WHERE table_name LIKE '{table}'"
        res = self.sql.get(qry)[0].get('nhood_geojson')
        if res == None or res == 'None':
            return None
        geojson = json.loads(res)
        return geojson

    def map_rows_to_neighborhoods(self, data, table, nhood_geojson):

        # take out null longitude and latitude rows
        if type(data) == type([]):
            df = pd.DataFrame.from_dict(data)
        else:
            df = data
        df = df[(df['latitude'].notna()) & (df['longitude'].notna()) &
                (df['latitude'] != 'None') & (df['longitude'] != 'None')]

        # merging the two dataframes in order to map row's coordinates to corresponding neighborhoods
        df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['longitude'], df['latitude']))
        nhood_map = gpd.GeoDataFrame.from_features(nhood_geojson.get('features'))
        df.crs = nhood_map.crs
        df = gpd.sjoin(nhood_map, df)
        return df
