class BroadPhaseDetector:
    def find_candidate_pairs(self, bodies):
        candidate_pairs = []

        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                body_a = bodies[i]
                body_b = bodies[j]

                if body_a.is_static and body_b.is_static:
                    continue

                candidate_pairs.append((body_a, body_b))

        return candidate_pairs
