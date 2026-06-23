from dataclasses import asdict, dataclass
from typing import Any

from examples.rocket_drone_lqr.sim.dynamics import RocketForces, RocketState
from examples.rocket_drone_lqr.sim.trajectory import TrajectoryPoint


@dataclass(frozen=True)
class ControlRequest:
    time: float
    state: RocketState
    reference: TrajectoryPoint

    def to_dict(self) -> dict[str, Any]:
        return {
            "time": self.time,
            "state": asdict(self.state),
            "reference": asdict(self.reference),
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "ControlRequest":
        return ControlRequest(
            time=float(data["time"]),
            state=RocketState(**data["state"]),
            reference=TrajectoryPoint(**data["reference"]),
        )


@dataclass(frozen=True)
class ControlResponse:
    forces: RocketForces

    def to_dict(self) -> dict[str, Any]:
        return {"forces": asdict(self.forces)}

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "ControlResponse":
        return ControlResponse(
            forces=RocketForces(**data["forces"]),
        )