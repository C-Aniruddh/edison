import pytest
import edisoncar as ec
from edisoncar.parts.transform import Lambda

@pytest.fixture()
def vehicle():
    v = ec.Vehicle()
    def f(): return 1
    l = Lambda(f)
    v.add(l, outputs=['test_out'])
    return v

def test_create_vehicle():
    v = ec.Vehicle()
    assert v.parts == []


def test_add_part():
    v = ec.Vehicle()
    def f():
        return 1
    l = Lambda(f)
    v.add(l, outputs=['test_out'])
    assert len(v.parts) == 1


def test_vehicle_run(vehicle):
    vehicle.start(rate_hz=20, max_loop_count=2)
    assert vehicle is not None