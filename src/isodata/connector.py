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

        self.token = self.get_token()

        if self.token is None:
            logger.error('No token retrieved')
        else:
            logger.debug('Received a token of length %s characters.' % len(self.token))
