class ReservationError(Exception):
    pass


class ReservationOverlap(ReservationError):
    pass


class ReservationNotFound(ReservationError):
    pass


class InvalidTimeRange(ReservationError):
    pass


# Parking lots
#
class ParkingLotError(Exception):
    pass


class ParkingLotNotFound(ParkingLotError):
    pass
