import secrets


class SkyScannerEndpoints:
    '''returns formatted api endpoint strings for making api calls'''

    def __init__(self):
        self.apiKey = secrets.SKYSCANNER_KEY
        self.baseUrl = 'http://partners.api.skyscanner.net/apiservices/'
        self.country = "US"
        self.currency = "USD"
        self.locale = 'en-US'

    def get_all_geo(self):
        return '{0}geo/v1.0?apiKey={1}'.format(self.baseUrl, self.apiKey)

    def browse_quotes(self, originPlace, destinationPlace, outboundPartialDate, inboundPartialDate):
        # inbound partial date can be empty if one way trip
        if inboundPartialDate is None:
            inboundPartialDate = ''

        return '{0}/browsequotes/v1.0/{1}{2}{3}{4}{5}{6}{7}?apiKey={8}'.format(
            self.baseUrl,
            self.country,
            self.currency,
            self.locale,
            originPlace,
            destinationPlace,
            outboundPartialDate,
            inboundPartialDate,
            self.apiKey)