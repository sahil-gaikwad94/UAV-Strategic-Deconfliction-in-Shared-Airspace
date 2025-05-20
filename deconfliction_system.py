# A simple system to check for drone mission conflicts in shared airspace.

import math
import matplotlib.pyplot as plt

# Configuration
HARDCODED_SAFETY_BUFFER = 5.0 # Minimum safety distance in units (e.g., meters)

# Helper Functions
def calculate_distance(point1, point2):
    """Calculates the Euclidean distance between two 2D points."""
    # point1 and point2 are tuples like (x, y)
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Data Structures
# I'm representing missions and flight paths using dictionaries and lists of tuples.

# Example Primary Drone Mission:
# primary_mission_example = {
#     "waypoints": [(0, 0), (10, 10), (10, 20), (20, 20)], # List of (x, y) tuples
#     "time_window": (0, 100) # (start_time, end_time) in seconds
# }

# Example Simulated Flight Schedules (a list of individual drone flight plans):
# simulated_flights_example = [
#     {
#         "id": "drone_A",
#         "path_segments": [
#             # Each segment is ((start_x, start_y), (end_x, end_y), (segment_start_time, segment_end_time))
#             ((5, 0), (5, 15), (10, 40)),
#             ((5, 15), (15, 15), (40, 60))
#         ]
#     },
#     {
#         "id": "drone_B",
#         "path_segments": [
#             ((0, 10), (20, 10), (0, 50))
#         ]
#     }
# ]

# --- Core Logic: Spatial and Temporal Checks ---
def is_spatial_conflict(segment1_start, segment1_end, segment2_start, segment2_end, buffer):
    """ 
    Checks if two line segments are closer than the safety buffer.
    This is a simplified check. A more robust check would involve:
    1. Distance between line segments.
    2. Checking if endpoints of one segment are close to the other segment.
    For a beginner, we can start with checking distances between endpoints and midpoints.
    """
    # Simplified check: distance between midpoints (very basic, for demonstration)
    mid1 = ((segment1_start[0] + segment1_end[0]) / 2, (segment1_start[1] + segment1_end[1]) / 2)
    mid2 = ((segment2_start[0] + segment2_end[0]) / 2, (segment2_start[1] + segment2_end[1]) / 2)
    if calculate_distance(mid1, mid2) < buffer:
        # print(f"Conflict: Midpoint dist {calculate_distance(mid1, mid2)} < {buffer}")
        return True

    # Also check distance between all endpoints
    if calculate_distance(segment1_start, segment2_start) < buffer: 
        # print(f"Conflict: Endpoint dist {calculate_distance(segment1_start, segment2_start)} < {buffer}")
        return True
    if calculate_distance(segment1_start, segment2_end) < buffer: 
        # print(f"Conflict: Endpoint dist {calculate_distance(segment1_start, segment2_end)} < {buffer}")
        return True
    if calculate_distance(segment1_end, segment2_start) < buffer: 
        # print(f"Conflict: Endpoint dist {calculate_distance(segment1_end, segment2_start)} < {buffer}")
        return True
    if calculate_distance(segment1_end, segment2_end) < buffer: 
        # print(f"Conflict: Endpoint dist {calculate_distance(segment1_end, segment2_end)} < {buffer}")
        return True
    
    # A more accurate check would involve point-to-line-segment distance
    # or line-segment to line-segment distance, which is more complex.
    # This simplified version is a starting point for a beginner.
    return False

def is_temporal_overlap(time_interval1_start, time_interval1_end, time_interval2_start, time_interval2_end):
    """Checks if two time intervals overlap."""
    # (StartA <= EndB) and (EndA >= StartB)
    return time_interval1_start <= time_interval2_end and time_interval1_end >= time_interval2_start

# --- Query Interface ---
def check_mission_safety(primary_mission, simulated_flights, safety_buffer):
    """
    Checks the primary drone mission against simulated flights for conflicts.
    Returns a status and details of any conflicts.
    """
    conflicts = []
    primary_waypoints = primary_mission["waypoints"]
    mission_start_time, mission_end_time = primary_mission["time_window"]

    if len(primary_waypoints) < 2:
        return {"status": "clear", "reason": "Primary mission has less than 2 waypoints."}
    
    num_primary_segments = len(primary_waypoints) - 1
    if num_primary_segments == 0: # Should not happen if len < 2 is checked, but as a safeguard
        return {"status": "clear", "reason": "Primary mission has no segments."}
    time_per_primary_segment = (mission_end_time - mission_start_time) / num_primary_segments

    for i in range(num_primary_segments):
        p_seg_start_wp = primary_waypoints[i]
        p_seg_end_wp = primary_waypoints[i+1]
        p_seg_start_time = mission_start_time + (i * time_per_primary_segment)
        p_seg_end_time = p_seg_start_time + time_per_primary_segment

        for sim_flight in simulated_flights:
            for sim_seg_idx, (sim_seg_start_wp, sim_seg_end_wp, (sim_seg_start_time_val, sim_seg_end_time_val)) in enumerate(sim_flight["path_segments"]):
                # 1. Spatial Check
                if is_spatial_conflict(p_seg_start_wp, p_seg_end_wp, sim_seg_start_wp, sim_seg_end_wp, safety_buffer):
                    # 2. Temporal Check
                    if is_temporal_overlap(p_seg_start_time, p_seg_end_time, sim_seg_start_time_val, sim_seg_end_time_val):
                        conflict_info = {
                            "type": "Spatio-Temporal Conflict",
                            "primary_segment_index": i,
                            "primary_segment_waypoints": (p_seg_start_wp, p_seg_end_wp),
                            "primary_segment_time": (p_seg_start_time, p_seg_end_time),
                            "conflicting_drone_id": sim_flight["id"],
                            "conflicting_drone_segment_index": sim_seg_idx,
                            "conflicting_drone_segment_waypoints": (sim_seg_start_wp, sim_seg_end_wp),
                            "conflicting_drone_segment_time": (sim_seg_start_time_val, sim_seg_end_time_val),
                            "approx_conflict_location": "Near primary segment from {} to {}".format(p_seg_start_wp, p_seg_end_wp),
                            "approx_conflict_time_primary": "Between {:.2f}s and {:.2f}s".format(p_seg_start_time, p_seg_end_time)
                        }
                        conflicts.append(conflict_info)
    
    if conflicts:
        return {"status": "conflict detected", "details": conflicts}
    else:
        return {"status": "clear"}

# --- Simulation & Visualization ---
def plot_scenario(primary_mission, simulated_flights, conflicts=None, title="Drone Mission Scenario"):
    """Plots the drone paths and highlights conflicts."""
    plt.figure(figsize=(10, 8))
    
    # Plot primary mission path
    px_coords = [wp[0] for wp in primary_mission["waypoints"]]
    py_coords = [wp[1] for wp in primary_mission["waypoints"]]
    plt.plot(px_coords, py_coords, marker=".", linestyle="-", color="blue", label="Primary Drone Mission")
    plt.scatter(px_coords, py_coords, color="blue", s=50) # Mark waypoints

    # Plot simulated drone paths
    # Keep track of labels to avoid duplicates in legend
    sim_labels_added = set()
    for i, flight in enumerate(simulated_flights):
        flight_color = plt.get_cmap("viridis")(i / len(simulated_flights)) # Get different colors
        for seg_idx, (start_wp, end_wp, _) in enumerate(flight["path_segments"]):
            label = f"Simulated Drone {flight["id"]}"
            if flight["id"] not in sim_labels_added:
                plt.plot([start_wp[0], end_wp[0]], [start_wp[1], end_wp[1]], 
                         marker="o", linestyle="--", color=flight_color, label=label)
                sim_labels_added.add(flight["id"])
            else:
                 plt.plot([start_wp[0], end_wp[0]], [start_wp[1], end_wp[1]], 
                         marker="o", linestyle="--", color=flight_color)
            plt.scatter([start_wp[0], end_wp[0]], [start_wp[1], end_wp[1]], color=flight_color, s=30)

    # Highlight conflicts
    conflict_label_added = False
    if conflicts:
        for conflict in conflicts:
            p_start, p_end = conflict["primary_segment_waypoints"]
            if not conflict_label_added:
                plt.plot([p_start[0], p_end[0]], [p_start[1], p_end[1]], color="red", linewidth=3, label="Conflict Area")
                conflict_label_added = True
            else:
                plt.plot([p_start[0], p_end[0]], [p_start[1], p_end[1]], color="red", linewidth=3)

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.axis("equal") # Ensure aspect ratio is equal for better spatial representation
    filename = title.lower().replace(" ", "_").replace(":", "") + ".png"
    plt.savefig(filename)
    print(f"Plot saved as {filename}")
    plt.close() # Close the plot to free memory
    return filename

# --- Main Execution / Example Scenarios ---
if __name__ == "__main__":
    print("Running Deconfliction System Examples...")

    # Scenario 1: Conflict-Free Mission
    primary_mission_safe = {
        "waypoints": [(0, 0), (10, 0), (10, 10)],
        "time_window": (0, 60) # Total time for mission
    }
    simulated_flights_safe = [
        {
            "id": "drone_A_safe",
            "path_segments": [
                ((20, 20), (20, 30), (0, 30)), # Far away
                ((20, 30), (30, 30), (30, 60))
            ]
        }
    ]

    print("\n--- Scenario 1: Conflict-Free Mission ---")
    result_safe = check_mission_safety(primary_mission_safe, simulated_flights_safe, HARDCODED_SAFETY_BUFFER)
    print(f"Mission Status: {result_safe["status"]}")
    if result_safe["status"] == "conflict detected":
        for detail in result_safe["details"]:
            print(f"  - {detail}")
    plot_filename_safe = plot_scenario(primary_mission_safe, simulated_flights_safe, 
                                       result_safe.get("details"), 
                                       title="Conflict-Free Mission Example")
    print(f"Visualization for safe scenario: {plot_filename_safe}")

    # Scenario 2: Mission with Conflicts
    primary_mission_conflict = {
        "waypoints": [(0, 5), (20, 5), (20, 15)], # Primary path: (0,5)->(20,5) then (20,5)->(20,15)
        "time_window": (0, 100) # Total time. Segment 1: 0-50s, Segment 2: 50-100s
    }
    simulated_flights_conflict = [
        {
            "id": "drone_B_conflict",
            "path_segments": [
                # This drone flies along part of the primary drone's first segment during overlapping time
                ((5, 5), (15, 5), (20, 70)) 
            ]
        },
        {
            "id": "drone_C_spatial_ok_temporal_miss",
            "path_segments": [
                 ((10, 0), (10, 3), (25, 45)) # Spatially close to (10,5) (mid of primary seg1) but buffer might save it
            ]
        },
        {
            "id": "drone_D_spatial_conflict_temporal_ok",
            "path_segments": [
                ((0, 5), (5, 5), (110, 120)) # Spatially on primary start, but different time window
            ]
        }
    ]

    print("\n--- Scenario 2: Mission with Conflicts ---")
    result_conflict = check_mission_safety(primary_mission_conflict, simulated_flights_conflict, HARDCODED_SAFETY_BUFFER)
    print(f"Mission Status: {result_conflict["status"]}")
    if result_conflict["status"] == "conflict detected":
        print("Conflict Details:")
        for detail in result_conflict["details"]:
            print(f"  - Drone ID: {detail["conflicting_drone_id"]}")
            print(f"    Primary Segment Index: {detail["primary_segment_index"]}")
            print(f"    Primary Segment: {detail["primary_segment_waypoints"]} ({detail["primary_segment_time"][0]:.1f}s - {detail["primary_segment_time"][1]:.1f}s)")
            print(f"    Simulated Segment Index: {detail["conflicting_drone_segment_index"]}")
            print(f"    Simulated Segment: {detail["conflicting_drone_segment_waypoints"]} ({detail["conflicting_drone_segment_time"][0]:.1f}s - {detail["conflicting_drone_segment_time"][1]:.1f}s)")

    plot_filename_conflict = plot_scenario(primary_mission_conflict, simulated_flights_conflict, 
                                           result_conflict.get("details"), 
                                           title="Conflict Mission Example")
    print(f"Visualization for conflict scenario: {plot_filename_conflict}")

    print("\nDeconfliction System Examples Complete.")

