from src.classifier import geoparse


def test_geoparse():
    test_string = "Eiffel Tower is located in Paris"
    location = geoparse(test_string)
    assert location == [{'word': 'Eiffel Tower',
  'spans': [{'start': 0, 'end': 12}],
  'country_predicted': 'FRA',
  'country_conf': 0.611725,
  'geo': {'admin1': 'Île-de-France',
   'lat': '48.85832',
   'lon': '2.29452',
   'country_code3': 'FRA',
   'geonameid': '6254976',
   'place_name': 'Tour Eiffel',
   'feature_class': 'S',
   'feature_code': 'MNMT'}},
 {'word': 'Paris',
  'spans': [{'start': 27, 'end': 32}],
  'country_predicted': 'FRA',
  'country_conf': 0.9881995,
  'geo': {'admin1': 'Île-de-France',
   'lat': '48.85339',
   'lon': '2.34864',
   'country_code3': 'FRA',
   'geonameid': '2988506',
   'place_name': 'Paris',
   'feature_class': 'A',
   'feature_code': 'ADM3'}}]
