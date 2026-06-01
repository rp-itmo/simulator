# Collision System Architecture

## Overview

This module implements a simple and extensible 2D collision detection architecture.

## Components

- **CollisionShape**: Base class for collision geometry.
- **CircleShape**: Circle collision representation.
- **RectangleShape**: Rectangle collision representation.
- **PolygonShape**: Polygon collision representation.
- **RigidBody**: Stores object position, velocity and shape.
- **CollisionData**: Stores contact point, collision normal and penetration depth.
- **BroadPhaseDetector**: Generates candidate collision pairs.
- **NarrowPhaseDetector**: Performs detailed collision detection.
- **CollisionSystem**: Coordinates the collision pipeline.
- **PhysicsWorld**: Manages bodies and simulation updates.

## Implemented Collision Type

- Circle vs Rectangle

## Collision Pipeline

1. Update object positions.
2. Generate candidate pairs using the broad phase.
3. Perform precise collision tests using the narrow phase.
4. Generate collision information.
5. Return detected collisions.

## Current Features

- Shape abstraction
- Broad phase collision detection
- Narrow phase collision detection
- Contact point computation
- Collision normal computation
- Penetration depth computation
- Physics world integration
