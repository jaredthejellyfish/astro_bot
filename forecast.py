class Forecast:
    def generate_link(self, lat, lon):
        #Generate link with formatted coordinates for clearoutside.
        link = 'https://clearoutside.com/forecast_image_large/{}/{}/forecast.png'.format(round(lat,2), round(lon,2))
        return link
   