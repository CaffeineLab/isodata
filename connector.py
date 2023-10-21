from loguru import logger

class Connector:
    token = None
    required = []

    def authorize(self, **kwargs):
        """Set all dynamic attributes."""

        for r in self.required:
            try:
                setattr(self, r, kwargs[r])
            except IndexError:
                logger.error("Cannot authorize: Missing '[%s]' credential" % r)

        try:
            self.token = self.get_token()
            logger.debug('Received a token of length %s characters.' % len(self.token))
        except AttributeError:
            self.token = None
