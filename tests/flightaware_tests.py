import unittest
import pytz
import re
from pprint import pprint
from datetime import datetime, timedelta
from flightaware.client import Client

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read("developer.cfg")
username = config.get("test settings", "username")
api_key = config.get("test settings", "api_key")
verbose = config.getboolean("test settings", "verbose")

print "Using username => %s" % username
print "Using api_key => %s" % api_key


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.client = Client(username=username, api_key=api_key)

    def tearDown(self):
        pass

    #
    # Combined API tests
    #

    def test_basic_calls(self):
        results = self.client.all_airlines()
        self.assertNotIn("error", results)
        results = self.client.all_airports()
        self.assertNotIn("error", results)
        results = self.client.count_airport_operations("BNA")
        self.assertNotIn("error", results)

    def test_weather_calls(self):
        results = self.client.ntaf("BNA")
        self.assertNotIn("error", results)
        results = self.client.taf("BNA")
        self.assertNotIn("error", results)

    #
    # Individual API tests
    #

    def test_aircraft_type(self):
        results = self.client.aircraft_type("GALX")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_airline_flight_info(self):
        faFlightID = self.client.get_flight_id("N415PW", 1442008560)
        if verbose: pprint(faFlightID)

        results = self.client.airline_flight_info(faFlightID)
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_airline_flight_schedules(self):
        start = datetime.now(tz=pytz.utc) + timedelta(days=2)
        end = datetime.now(tz=pytz.utc) + timedelta(days=3)
        results = self.client.airline_flight_schedules(
            start_date=start,
            end_date=end,
            origin="KSFO",
            destination="KLAX",
        )
        if verbose: pprint(results)
        self.assertNotIn("error", results)

        for result in results:
            self.assertIn("arrival_time", result)
            self.assertIn("departure_time", result)

    def test_airline_info(self):
        results = self.client.airline_info("SWA")
        self.assertNotIn("error", results)

    def test_airline_insight(self):
        results = self.client.airline_insight("BNA", "ATL")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_airport_info(self):
        results = self.client.airport_info("KasdfBNA")
        if verbose: pprint(results)
        self.assertIn("error", results)

        results = self.client.airport_info("BNA")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

        results = self.client.airport_info("KBNA")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_all_airlines(self):
        results = self.client.all_airlines()
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_all_airports(self):
        results = self.client.all_airports()
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_arrived(self):
        results = self.client.arrived("KSFO")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_block_indent_check(self):
        results = self.client.block_indent_check("N415PW")
        if verbose: pprint(results)
        self.assertTrue(isinstance(results, (int, long)))

    def test_count_airport_operations(self):
        results = self.client.count_airport_operations("KSFO")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_count_all_enroute_airline_operations(self):
        results = self.client.count_all_enroute_airline_operations()
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_decode_flight_route(self):
        faFlightID = self.client.get_flight_id("N415PW", 1442008560)
        if verbose: pprint(faFlightID)

        results = self.client.decode_flight_route(faFlightID)
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_decode_route(self):
        results = self.client.decode_route("KSQL", "SJC V334 SAC SWR", "KTRK")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_fleet_arrived(self):
        results = self.client.fleet_arrived("URF")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_fleet_scheduled(self):
        results = self.client.fleet_scheduled("URF")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_flight_info(self):
        results = self.client.flight_info("N415PW")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_flight_info_ex(self):
        results = self.client.flight_info_ex("N415PW")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_get_alerts(self):
        results = self.client.get_alerts()
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_get_flight_id(self):
        results = self.client.get_flight_id("N415PW", 1442008560)
        if verbose: pprint(results)
        self.assertNotIn("error", results)

        results = self.client.get_flight_id("N415PW", datetime.fromtimestamp(1442008560, tz=pytz.utc))
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_get_historical_track(self):
        faFlightID = self.client.get_flight_id("N415PW", 1442008560)
        if verbose: pprint(faFlightID)

        results = self.client.get_historical_track(faFlightID)
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_get_last_track(self):
        results = self.client.get_last_track("N415PW")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_inbound_flight_info(self):
        faFlightID = self.client.get_flight_id("SWA2612", 1442035080)
        if verbose: pprint(faFlightID)

        results = self.client.inbound_flight_info(faFlightID)
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_in_flight_info(self):
        results = self.client.in_flight_info("N415PW")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_lat_longs_to_distance(self):
        results = self.client.lat_longs_to_distance(37.3626667, -121.9291111, 33.9425003, -118.4080736)
        if verbose: pprint(results)
        self.assertTrue(isinstance(results, (int, long)))

    def test_lat_longs_to_heading(self):
        results = self.client.lat_longs_to_heading(37.3626667, -121.9291111, 33.9425003, -118.4080736)
        if verbose: pprint(results)
        self.assertTrue(isinstance(results, (int, long)))

    def test_map_flight(self):
        results = self.client.map_flight("N415PW", 100, 100)
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_map_flight_ex(self):

        faFlightID = self.client.get_flight_id("SKW2494", 1442040480)
        if verbose: pprint(faFlightID)

        mapHeight = 100
        mapWidth = 100 
        layer_on = ""
        layer_off = ""
        show_data_blocks = "true"
        show_airports = "true"
        airports_expand_view = "true"
        latlon_box = ""

        results = self.client.map_flight_ex(faFlightID, mapHeight, mapWidth, layer_on, layer_off, show_data_blocks, show_airports, airports_expand_view, latlon_box)
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_metar(self):
        results = self.client.metar("BNA")
        self.assertNotIn("error", results)

    def test_metar_ex(self):
        results = self.client.metar_ex("BNA")
        self.assertNotIn("error", results)

    def test_ntaf(self):
        results = self.client.ntaf("KSFO")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_register_alert_endpoint(self):
        '''
        #
        # XXX:  Need to figure out how to test this without disrupting the developer's alerts.
        # Ideally, there'd be an API to get the current alert endpoint.
        #

        results = self.client.register_alert_endpoint("http://www.example.com")
        if verbose: pprint(results)
        self.assertNotIn("error", results)
        '''

    def test_routes_between_airports(self):
        results = self.client.routes_between_airports("KSFO", "KLAX")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_routes_between_airports_ex(self):
        results = self.client.routes_between_airports_ex("KSFO", "KLAX")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_scheduled(self):
        results = self.client.scheduled("KSQL")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_search(self):
        queries = [
            { "type" : "B77*" },
            { "belowAltitude" : 100, "aboveGroundspeed" : 200 },
            { "destination" : "LAX", "prefix" : "H" },
            { "idents" : "UAL*", "type" : "B73*" },
        ]

        for parameters in queries:
            if verbose: pprint(parameters)
            results = self.client.search(parameters, 1)
            if verbose: pprint(results)
            self.assertNotIn("error", results)

    def test_search_birdseye_in_flight(self):
        queries = [
            [ "{< alt 100} {> gs 200}", "All aircraft below ten-thousand feet with a groundspeed over 200 kts" ],
            [ "{match aircraftType B77*}", "All in-air Boeing 777s" ],
            [ "{= dest KLAX} {= prefix H}", "All aircraft heading to Los Angeles International Airport (LAX) that are \"heavy\" aircraft" ],
            [ "{match ident UAL*} {match aircraftType B73*}", "All United Airlines flights in Boeing 737s" ],
            [ "{true lifeguard}", "All \"lifeguard\" rescue flights" ],
            [ "{in orig {KLAX KBUR KSNA KLGB KVNY KSMO KLGB KONT}} {in dest {KJFK KEWR KLGA KTEB KHPN}}", "All flights between Los Angeles area and New York area" ],
            [ "{range lat 36.897669 40.897669} {range lon -79.03655 -75.03655}", "All flights with a last reported position +/- 2 degrees of the Whitehouse" ],
            [ "{> lastPositionTime 1278610758} {true inAir} {!= physClass P} {> circles 3}", "All flights that have a reported position after a specified epoch time, are still in the air, are not piston class, and have made several circular flight patterns (potentially in distress)" ],
        ]

        for (query,comment) in queries:
            if verbose: print "SearchBirdseyeInFlight: ", comment, "(", query, ")"
            results = self.client.search_birdseye_in_flight(query, 1)
            if verbose: pprint(results)
            if u'error' in results and results[u'error'] != u'no results':
                self.assertNotIn("error", results)

    def test_search_birdseye_positions(self):
        queries = [
            [ "{< alt 100} {> gs 200}", "All flight positions below ten-thousand feet with a groundspeed over 200 kts" ],
            [ "{match fp ASA*}", "All Alaska Airlines flight positions" ],
            [ "{match fp ASA*} {> lat 45}", "All Alaska Airlines flight positions north of the 45th parallel" ],
            [ "{range lat 36.897669 40.897669} {range lon -79.03655 -75.03655}", "All flight positions +/- 2 degrees of the lat/lon of the Whitehouse" ],
            [ "{= fp N415PW-1442008613-adhoc-0}", "All flight positions for a specific flight identifier (faFlightID)" ],
        ]

        for (query,comment) in queries:
            if verbose: print "SearchBirdseyePositions: ", comment, "(", query, ")"
            results = self.client.search_birdseye_positions(query, True, 1)
            if verbose: pprint(results)
            if u'error' in results and results[u'error'] != u'no results':
                self.assertNotIn("error", results)

    def test_search_count(self):
        queries = [
            { "type" : "B77*" },
            { "belowAltitude" : 100, "aboveGroundspeed" : 200 },
            { "destination" : "LAX", "prefix" : "H" },
            { "idents" : "UAL*", "type" : "B73*" },
        ]

        for parameters in queries:
            if verbose: pprint(parameters)
            results = self.client.search_count(parameters)
            if verbose: pprint(results)
            self.assertTrue(isinstance(results, (int, long)))

    def test_set_alert(self):
        """
        XXX:  Need to implement this unit test.
        """

    def test_set_maximum_result_sizes(self):
        """
        XXX:  Need to implement this unit test.
        """

    def test_set_maximum_result_size(self):
        results = self.client.set_maximum_result_size(15)
        if verbose: pprint(results)
        self.assertTrue(isinstance(results, (int, long)))

    def test_taf(self):
        results = self.client.taf("KSFO")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_tail_owner(self):
        results = self.client.tail_owner("N415PW")
        if verbose: pprint(results)
        self.assertNotIn("error", results)

    def test_zipcode_info(self):
        results = self.client.zipcode_info("37221")
        self.assertNotIn("error", results)

