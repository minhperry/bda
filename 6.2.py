points = {
    "A": (5, 4),
    "B": (2, 5),
    "C": (1, 7),
    "D": (3, 8),
    "E": (5, 7),
    "F": (9, 4),
    "G": (9, 1),
    "H": (7, 2),
}

medoids = ["A", "E"]

non_medoids = [point for point in points if point not in medoids]


def mdist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def select_medoids(points, medoids):
    clusters = {}
    for medoid in medoids:
        clusters[medoid] = {}
    for point in points:
        min_dist = float("inf")
        min_medoid = None
        for medoid in medoids:
            dist = mdist(points[point], points[medoid])
            if dist < min_dist:
                min_dist = dist
                min_medoid = medoid
        clusters[min_medoid][point] = min_dist
    for medoid in medoids:
        clusters[medoid].pop(medoid)
    return clusters


def compute_cost(clusters, points):
    cost = 0
    for medoid in clusters:
        for point in clusters[medoid]:
            cost += mdist(points[point], points[medoid])
    return cost


def swap_point(point_set, p1, p2):
    pointcpy = point_set.copy()
    pointcpy[p1], pointcpy[p2] = pointcpy[p2], pointcpy[p1]
    return pointcpy


def swap_permanently(point_set, p1, p2):
    point_set[p1], point_set[p2] = point_set[p2], point_set[p1]
    return point_set


def costs_on_swap(points, medoids, non_medoids):
    swap_cost_dict = {}
    for medoid in medoids:
        for non_medoid in non_medoids:
            swapped = swap_point(points, medoid, non_medoid)
            swap_cost_dict[(medoid, non_medoid)] = compute_cost(
                select_medoids(swapped, medoids), swapped
            )
    return swap_cost_dict


if __name__ == "__main__":
    # Step 1: For each pair (medoid M, non-medoid N), swap M and N and compute the cost.
    clusters = select_medoids(points, medoids)
    swap_cost_dict = costs_on_swap(points, medoids, non_medoids)
    print(
        "Step 1: for each pair (medoid M, non-medoid N), swap M and N and compute the cost:"
    )
    print(swap_cost_dict)
    for swap in swap_cost_dict:
        print(f"Swapping {swap[0]} and {swap[1]} gives cost {swap_cost_dict[swap]}")

    # Step 2: Select the pair (M, N) with the lowest cost.
    min_cost = float("inf")
    min_swap = None
    for swap in swap_cost_dict:
        if swap_cost_dict[swap] < min_cost:
            min_cost = swap_cost_dict[swap]
            min_swap = swap
    print("\nStep 2: Select the pair (M, N) with the lowest cost:")
    print(min_swap, "=", min_cost, "\n")

    # Step 3: If TD_curr < TD_swap, then swap M and N permanently.
    td_curr = compute_cost(clusters, points)
    td_swap = min_cost
    print("Step 3: If TD_curr < TD_swap, then swap M and N permanently:")
    print("TD_curr =", td_curr)
    print("TD_swap =", td_swap)
    if td_curr < td_swap:
        print("TD_curr < TD_swap, so swap M and N permanently.")
        points = swap_permanently(points, min_swap[0], min_swap[1])
        td_curr = td_swap
    else:
        print("TD_curr >= TD_swap, so do not swap M and N permanently.")

    # In case of using set N as medoid instead:
    medoids, non_medoids = non_medoids, medoids
    hypo_swap_cost = costs_on_swap(points, medoids, non_medoids)
    print("\nIn case of using set N as medoid instead:")
    print(hypo_swap_cost)
