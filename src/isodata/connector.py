from loguru import logger


class Connector:
    token = None
    required = []

    def authorize(self, **kwargs):
        """Set all dynamic attributes."""

        if len(self.required) == 0:
            logger.warning("No requirments for connector?")

        for r in self.required:
            try:
                setattr(self, r, kwargs[r])
            except IndexError:
                logger.error(f"Authorize: Missing '[{r}]' credential" % r)
            except KeyError:
                logger.error(f"Authorize: Required attribute not set: '{r}'")

        self.token = self.get_token()

        if self.token is None:
            logger.error('No token retrieved')
        else:
            logger.debug('Received a token of length %s characters.' % len(self.token))
