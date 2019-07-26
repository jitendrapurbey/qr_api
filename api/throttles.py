from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class NormalQRRateThrottle(AnonRateThrottle):
    scope = 'normal'


class UserQRRateThrottle(UserRateThrottle):
    scope = 'user'
