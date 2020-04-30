from satellite import Satellite
from forecast import Forecast
lat, lon = (41.28610, 1.98241)

sat = Satellite()
fc = Forecast()

#fc.get_forecast(lat, lon)
print(sat.get_sat(lat, lon))