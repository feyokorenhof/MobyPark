# Reservations


class ReservationError(Exception):
    pass


class ReservationOverlap(ReservationError):
    pass


class ReservationNotFound(ReservationError):
    pass


class InvalidTimeRange(ReservationError):
    pass


# Parking lots
class ParkingLotError(Exception):
    pass


class ParkingLotNotFound(ParkingLotError):
    pass


# Auth
class AuthError(Exception):
    pass


class AccountAlreadyExists(AuthError):
    pass


class InvalidCredentials(AuthError):
    pass


# Users
class UserError(Exception):
    pass


class UserNotFound(UserError):
    pass


# Sessions
class ParkingSessionError(Exception):
    pass


class ParkingSessionNotFound(ParkingSessionError):
    pass
