from abc import ABC, abstractmethod
from datetime import datetime


# ─────────────────────────────────────────────
#  Base class  —  abstract, never instantiated
# ─────────────────────────────────────────────
class Vehicle(ABC):
    def __init__(self, vehicle_id: str, driver: str) -> None:
        self.vehicle_id = vehicle_id
        self.driver     = driver

    @abstractmethod
    def fare(self, distance: float) -> float:
        """Every child MUST implement its own fare formula."""
        ...

    def trip_summary(self, distance: float) -> None:
        """Defined once here — calls self.fare() which resolves to the child's version."""
        total        = self.fare(distance)
        vehicle_type = self.__class__.__name__
        print(f"\n  {'─' * 46}")
        print(f"  🚗  {vehicle_type}  Trip Summary")
        print(f"  {'─' * 46}")
        print(f"  Driver     : {self.driver}")
        print(f"  Vehicle ID : {self.vehicle_id}")
        print(f"  Distance   : {distance} km")
        print(f"  Fare       : ₹{total:.2f}")
        print(f"  {'─' * 46}")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.vehicle_id}, driver={self.driver})"


# ─────────────────────────────────────────────
#  Child class: Car
# ─────────────────────────────────────────────
class Car(Vehicle):
    BASE_FARE = 50
    PER_KM    = 15

    def __init__(self, vehicle_id: str, driver: str) -> None:
        super().__init__(vehicle_id, driver)   # pass args up to Vehicle.__init__

    def fare(self, distance: float) -> float:
        return self.BASE_FARE + self.PER_KM * distance


# ─────────────────────────────────────────────
#  Child class: Bike
# ─────────────────────────────────────────────
class Bike(Vehicle):
    BASE_FARE = 20
    PER_KM    = 8

    def __init__(self, vehicle_id: str, driver: str) -> None:
        super().__init__(vehicle_id, driver)

    def fare(self, distance: float) -> float:
        return self.BASE_FARE + self.PER_KM * distance


# ─────────────────────────────────────────────
#  Child class: Auto
# ─────────────────────────────────────────────
class Auto(Vehicle):
    BASE_FARE = 30
    PER_KM    = 10

    def __init__(self, vehicle_id: str, driver: str) -> None:
        super().__init__(vehicle_id, driver)

    def fare(self, distance: float) -> float:
        return self.BASE_FARE + self.PER_KM * distance


# ─────────────────────────────────────────────
#  Bonus: SurgePricedCar  —  grandchild class
# ─────────────────────────────────────────────
class SurgePricedCar(Car):
    SURGE_MULTIPLIER = 1.5
    PEAK_HOURS       = {8, 9, 17, 18, 19, 20}   # 8-9 AM and 5-8 PM

    def __init__(self, vehicle_id: str, driver: str) -> None:
        super().__init__(vehicle_id, driver)     # → Car.__init__ → Vehicle.__init__

    def fare(self, distance: float) -> float:
        base = super().fare(distance)            # reuse Car's formula
        if datetime.now().hour in self.PEAK_HOURS:
            return base * self.SURGE_MULTIPLIER
        return base

    def trip_summary(self, distance: float) -> None:
        super().trip_summary(distance)           # print Car/Vehicle summary first
        hour       = datetime.now().hour
        is_peak    = hour in self.PEAK_HOURS
        base_total = Car.fare(self, distance)    # plain Car fare without surge
        if is_peak:
            print(
                f"  Surge Active ({self.SURGE_MULTIPLIER}) — "
                f"Peak hour {hour}:00  |  Base was ₹{base_total:.2f}"
            )
        else:
            print(f"  No surge — off-peak hour {hour}:00")
        print(f"  {'─' * 46}")


# ─────────────────────────────────────────────
#  Fare table helper
# ─────────────────────────────────────────────
def print_fare_table(distance: float = 10) -> None:
    vehicles = [Car("X", "—"), Bike("X", "—"), Auto("X", "—")]
    print(f"\n  Fare Comparison at {distance} km")
    print("  " + "─" * 42)
    print(f"  {'Vehicle':<18} {'Base':>6}  {'/km':>5}  {'Total':>8}")
    print("  " + "─" * 42)
    rates = {
        "Car":  (Car.BASE_FARE,  Car.PER_KM),
        "Bike": (Bike.BASE_FARE, Bike.PER_KM),
        "Auto": (Auto.BASE_FARE, Auto.PER_KM),
    }
    for v in vehicles:
        name = v.__class__.__name__
        base, per_km = rates[name]
        total = v.fare(distance)
        print(f"  {name:<18} ₹{base:>4}   ₹{per_km:>3}   ₹{total:>6.2f}")
    print("  " + "─" * 42)


if __name__ == "__main__":
    print("Ola / Uber / Rapido Fleet System")

    print_fare_table(distance=10)

    fleet: list[Vehicle] = [
        Car("KA-01-AB-1234", "Ramesh"),
        Bike("TN-09-XY-5678", "Murugan"),
        Auto("MH-12-CD-9012", "Suresh"),
        SurgePricedCar("DL-03-EF-3456", "Vikram"),
    ]

    distance = 10
    for vehicle in fleet:
        vehicle.trip_summary(distance)

    print("\n  ── Polymorphism : same call, different fare() ──")
    for v in fleet:
        print(f"  {str(v):<50}  →  ₹{v.fare(distance):.2f}")

    print("\n  ── ABC prevents direct instantiation ──")
    try:
        v = Vehicle("X", "Y")
    except TypeError as e:
        print(f"  {e}")