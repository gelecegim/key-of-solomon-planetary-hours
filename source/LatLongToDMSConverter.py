class LatLongToDMSConverter:
    
    def convert_to_dms(self, latitude, longitude):
        latitude_dms = self.decimal_to_dms(latitude)
        longitude_dms = self.decimal_to_dms(longitude)
        return latitude_dms, longitude_dms

    def decimal_to_dms(self, value):
        degrees = int(value)
        minutes_float = (value - degrees) * 60
        minutes = int(minutes_float)
        seconds = round((minutes_float - minutes) * 60)
        return (degrees, minutes, seconds)