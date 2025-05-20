# FlytBase Robotics Assignment: UAV Strategic Deconfliction

This project is a simple implementation of a strategic deconfliction system for Unmanned Aerial Vehicles (UAVs) or drones. It checks if a primary drone's planned waypoint mission is safe to execute by looking for potential conflicts in space and time with other simulated drones operating in the same airspace.

This was completed as an assignment, aiming for a beginner-friendly approach to the problem.

## Features

*   **2D Waypoint Missions:** Defines drone missions as a series of (x, y) waypoints.
*   **Time Windows:** Considers an overall time window for the primary mission and specific time segments for simulated drone paths.
*   **Spatial Conflict Check:** A simplified check to see if drone paths come too close to each other (based on a safety buffer and distance between path segment endpoints/midpoints).
*   **Temporal Conflict Check:** Checks if potentially spatially conflicting drones are in the same area during overlapping time periods.
*   **Conflict Reporting:** If a conflict is detected, the system provides basic details about which drones are involved and where/when the conflict might occur.
*   **Query Interface:** A Python function `check_mission_safety()` that takes the primary mission and simulated flight data to return a status.
*   **Basic Visualization:** Uses `matplotlib` to plot the drone paths and highlight potential conflict areas in 2D.

## Setup and Dependencies

To run this project, you need Python 3 and the `matplotlib` library.

1.  **Ensure Python 3 is installed.**
    You can check by typing `python --version` or `python3 --version` in your terminal.

2.  **Install `matplotlib`:**
    If you don't have it, you can install it using pip:
    ```bash
    pip install matplotlib
    ```

## How to Run

1.  Save the `deconfliction_system.py` file to your computer.
2.  Open a terminal or command prompt.
3.  Navigate to the directory where you saved the file.
4.  Run the script using Python:
    ```bash
    python deconfliction_system.py
    ```

The script will execute two example scenarios:
*   A conflict-free mission.
*   A mission where a conflict is detected.

For each scenario, it will print the status to the console and save a plot as a PNG image in the same directory (e.g., `conflict-free_mission_example.png` and `conflict_mission_example.png`).

## Code Structure

The `deconfliction_system.py` file contains:

*   **Configuration:** Basic settings like `HARDCODED_SAFETY_BUFFER`.
*   **Helper Functions:** e.g., `calculate_distance()`.
*   **Data Structure Examples:** Comments showing how mission data is structured.
*   **Core Logic:** Functions like `is_spatial_conflict()` and `is_temporal_overlap()`.
*   **Query Interface:** The main `check_mission_safety()` function.
*   **Simulation & Visualization:** The `plot_scenario()` function.
*   **Main Execution Block:** (`if __name__ == "__main__":`) which runs the example scenarios.

## Future Improvements (Beyond Beginner Scope)

*   More accurate spatial conflict detection (e.g., line segment intersection, distance between line segments).
*   Handling drone speeds and variable timing for primary mission segments.
*   3D (x, y, z) and 4D (x, y, z, time) deconfliction.
*   More sophisticated visualization and animation.
*   A user interface instead of just script execution.

