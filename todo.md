# FlytBase Robotics Assignment - TODO

## Phase 1: Core Logic Implementation (Beginner Level)

- [ ] **1.1: Define Data Structures**
    - [ ] Define how to represent the primary drone's mission (waypoints `(x, y)`, overall time window `(T_start, T_end)`).
    - [ ] Define how to represent simulated drone flight paths (waypoints `(x, y)`, associated timings for each segment).
- [ ] **1.2: Implement Spatial Check**
    - [ ] Function to calculate distance between two points.
    - [ ] Function to check if two line segments (drone path segments) intersect or come within a safety buffer.
    - [ ] Iterate through primary drone's path segments and compare against all simulated drone path segments.
- [ ] **1.3: Implement Temporal Check**
    - [ ] Function to determine if two time intervals overlap.
    - [ ] For spatially conflicting segments, check if their time intervals also overlap.
- [ ] **1.4: Implement Conflict Explanation**
    - [ ] If a conflict is detected, store information: location (approximate), time of conflict, and which simulated drone(s) are involved.
- [ ] **1.5: Create Query Interface**
    - [ ] A simple Python function `check_mission_safety(primary_mission, simulated_flights, safety_buffer)`.
    - [ ] Function should return `{"status": "clear"}` or `{"status": "conflict detected", "details": [...]}`.

## Phase 2: Simulation and Visualization (Basic)

- [ ] **2.1: Generate Basic Plots**
    - [ ] Use `matplotlib` for 2D plotting.
    - [ ] Plot primary drone's path.
    - [ ] Plot simulated drones' paths.
    - [ ] Highlight conflict points/segments if any.
- [ ] **2.2: Create Scenarios**
    - [ ] Define a conflict-free scenario (data for primary mission and simulated flights).
    - [ ] Define a scenario with clear spatial and temporal conflicts.
    - [ ] Generate plots for both scenarios.

## Phase 3: Documentation

- [ ] **3.1: Write README.md**
    - [ ] Project overview.
    - [ ] How to set up (dependencies, e.g., `matplotlib`).
    - [ ] How to run the main script/function with example usage.
- [ ] **3.2: Write REFLECTION.md (Reflection & Justification Document)**
    - [ ] **Design Decisions & Architecture:** Explain the simple, modular approach chosen (e.g., separate functions for spatial, temporal checks, visualization).
    - [ ] **Spatial & Temporal Check Implementation:** Briefly describe the logic (e.g., line segment intersection, time interval overlap).
    - [ ] **AI Integration (Simulated):** Document how AI tools *could have been* used by a beginner (e.g., "Used an AI assistant to help debug a tricky part of the line intersection logic" or "Asked an AI tool for suggestions on how to structure the Python functions"). Keep it plausible for a beginner.
    - [ ] **Testing Strategy & Edge Cases:** Describe simple test cases (e.g., no drones, one drone far away, direct collision course). Mention basic edge cases (e.g., drones starting/ending at the same point but different times).
    - [ ] **Scalability Discussion:** Briefly touch on limitations of the current simple approach for many drones (e.g., N*M comparisons) and suggest high-level ideas for scaling (e.g., spatial indexing like quadtrees, more efficient algorithms – but keep it high-level and beginner-friendly).

## Phase 4: Code Structure and Finalization

- [ ] **4.1: Create Main Python Script**
    - [ ] `deconfliction_system.py` (or similar).
    - [ ] Include all functions (data structures, checks, plotting, query interface).
    - [ ] Add example usage in `if __name__ == "__main__":` block to demonstrate scenarios.
- [ ] **4.2: Ensure Beginner-Level Code**
    - [ ] Simple logic, clear variable names.
    - [ ] Adequate comments explaining each step.
    - [ ] Avoid advanced Python features unless very common.
- [ ] **4.3: Prepare for Demonstration Video (Script/Outline)**
    - [ ] Outline the key points to cover in a 3-5 minute video.
    - [ ] Introduction to the problem.
    - [ ] Showcasing the code structure briefly.
    - [ ] Running the conflict-free scenario and showing the plot.
    - [ ] Running the conflict scenario, showing the plot, and explaining the conflict details from the system.
    - [ ] (Optional, if time/complexity allows for beginner: Briefly mention 3D/4D extra credit idea).
    - [ ] Conclude with a summary.

## Phase 5: Review and Submission Package

- [ ] **5.1: Review all deliverables against assignment requirements.**
- [ ] **5.2: Create a zip file with the code repository (Python script, README.md, REFLECTION.md, and any generated plot images).**

