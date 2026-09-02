import streamlit as st
import html
import streamlit.components.v1 as components

st.set_page_config(page_title="IEEE MATLAB Ray Tracing Workshop", layout="wide", page_icon="📡")

# Custom CSS for styling
st.markdown("""
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #006699;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #555555;
            margin-bottom: 1.5rem;
        }
        .badge {
            background-color: #006699;
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 10px;
        }
        .challenge-box {
            background-color: #f8f9fa;
            border-left: 4px solid #ff9900;
            padding: 12px 16px;
            border-radius: 4px;
            margin: 15px 0;
        }
        .explanation-box {
            background-color: #eef7fc;
            border-left: 4px solid #006699;
            padding: 12px 16px;
            border-radius: 4px;
            margin: 15px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Dictionary of Workshop Parts
PARTS = {
    "Part 1 (no code)": {
        "title": "PART 1 — Getting Started with the Urban Environment",
        "badge": "Mini Task 1",
        "description": "Understand Line-of-Sight (LOS), Reflection, Diffraction, and Non-Line-of-Sight (NLOS) wireless propagation in 5G urban environments.",
        "explanation": """In urban 5G wireless communications, signals travel from a Base Station (TX) to User Equipment (RX) via multiple mechanisms:
- **Line-of-Sight (LOS)**: Direct path between TX and RX.
- **Reflection**: Signal bounces off building facades.
- **Diffraction**: Signal bends over rooftop edges or building corners.
- **NLOS**: When direct path is obstructed, relying entirely on reflections and diffractions.""",
        "challenge": "What happens to received power when a building blocks the direct LOS path?\n\n*Expected Answer*: Received power decreases as the signal relies on weaker, attenuated reflected/diffracted paths.",
        "code": r"""% PART 1 — Conceptual Understanding of Ray Tracing & Urban Propagation
% No MATLAB code required for setup in Part 1.
% Proceed to Part 2 to load 3D Chicago city environment.
"""
    },
    "Part 2": {
        "title": "PART 2 — Load a Real City",
        "badge": "Mini Task 2",
        "description": "Import 3D Chicago OpenStreetMap building geometries into MATLAB Site Viewer.",
        "explanation": """### Students run:
```matlab
clc;
clear;
close all;

viewer = siteviewer(...
    Buildings="chicago.osm", ...
    Basemap="topographic");
```

`siteviewer` initializes the 3D geographical simulation canvas using real OpenStreetMap (OSM) building data.""",
        "challenge": "Change the basemap from 'topographic' to another basemap (e.g. 'streets', 'satellite') and observe the visual difference.",
        "code": r"""clc;
clear;
close all;

viewer = siteviewer(...
    Buildings="chicago.osm", ...
    Basemap="topographic");
"""
    },
    "Part 3": {
        "title": "PART 3 — Create the 5G Base Station",
        "badge": "Mini Task 3",
        "description": "Define the 5G Base Station transmitter (txsite) parameters.",
        "explanation": """### Students create:
```matlab
tx = txsite( ...
    Name="5G Base Station", ...
    Latitude=41.8800,...
    Longitude=-87.6295,...
    AntennaHeight=25, ...
    TransmitterPower=10, ...
    TransmitterFrequency=2.5e9);

show(tx);
```

| Parameter | Value | Meaning |
| --- | --- | --- |
| Latitude | 41.8800 | Geographic Latitude |
| Longitude | -87.6295 | Geographic Longitude |
| AntennaHeight | 25 m | Height of tower antenna |
| TransmitterPower | 10 W | Transmit power level |
| TransmitterFrequency | 2.5 GHz | Carrier frequency |""",
        "challenge": "Change frequency from 2.5 GHz to 3.5 GHz. Will coverage increase or decrease?\n\n*Answer*: High carrier frequencies experience higher free-space path loss, decreasing overall coverage.",
        "code": r"""tx = txsite( ...
    Name="5G Base Station", ...
    Latitude=41.8800,...
    Longitude=-87.6295,...
    AntennaHeight=25, ...
    TransmitterPower=10, ...
    TransmitterFrequency=2.5e9);

show(tx);
"""
    },
    "Part 4": {
        "title": "PART 4 — Create First User Equipment (UE1)",
        "badge": "Mini Task 4",
        "description": "Place receiver User Equipment 1 (rxsite) in proximity to the base station.",
        "explanation": """### Students create:
```matlab
rx1 = rxsite( ...
    Name="User Equipment 1", ...
    Latitude=41.881352, ...
    Longitude=-87.629771, ...
    AntennaHeight=30);

show(rx1);
```

Receiver sites must be positioned accurately within the 3D map environment.""",
        "challenge": "Verify coordinates carefully in 3D Site Viewer.",
        "code": r"""rx1 = rxsite( ...
    Name="User Equipment 1", ...
    Latitude=41.881352, ...
    Longitude=-87.629771, ...
    AntennaHeight=30);

show(rx1);
"""
    },
    "Part 5 (no code)": {
        "title": "PART 5 — Check Line of Sight",
        "badge": "Mini Task 5",
        "description": "Determine if there is a clear direct LOS line between Base Station and UE1.",
        "explanation": """### Students run:
```matlab
los(tx,rx1);
```

LOS asks: Is there a clear direct path between transmitter and receiver?
- Clear path = Line of Sight (LOS)
- Blocked path = Non Line of Sight (NLOS)""",
        "challenge": "Move UE1 across different streets to observe transitions between LOS and NLOS states.",
        "code": r"""los(tx,rx1);
"""
    },
    "Part 6": {
        "title": "PART 6 — Create Ray-Tracing Model",
        "badge": "Mini Task 6",
        "description": "Initialize Shooting and Bouncing Rays (SBR) model for LOS propagation.",
        "explanation": """### Students create:
```matlab
rtpm = propagationModel("raytracing", ...
    Method="sbr", ...
    MaxNumReflections=0, ...
    MaxNumDiffractions=0);
```

SBR launches discrete electromagnetic rays from the transmitter to map spatial propagation paths.""",
        "challenge": "Set MaxNumReflections=0 and MaxNumDiffractions=0 for pure direct LOS analysis.",
        "code": r"""rtpm = propagationModel("raytracing", ...
    Method="sbr", ...
    MaxNumReflections=0, ...
    MaxNumDiffractions=0);
"""
    },
    "Part 7": {
        "title": "PART 7 — Generate Coverage Map (LOS)",
        "badge": "Mini Task 7",
        "description": "Plot signal power distribution map over 250m radius.",
        "explanation": """### Students run:
```matlab
coverage(tx, rtpm, ...
    SignalStrengths=-120:-5, ...
    MaxRange=250, ...
    Resolution=5, ...
    Transparency=0.6);
```

| Parameter | Value | Description |
| --- | --- | --- |
| SignalStrengths | -120:-5 dBm | Displayed power range |
| MaxRange | 250 m | Simulation radius |
| Resolution | 5 m | Grid cell spatial resolution |""",
        "challenge": "Observe building shadows where signal is completely blocked under LOS assumptions.",
        "code": r"""coverage(tx, rtpm, ...
    SignalStrengths=-120:-5, ...
    MaxRange=250, ...
    Resolution=5, ...
    Transparency=0.6);
"""
    },
    "Part 8": {
        "title": "PART 8 — Introduce NLOS Propagation",
        "badge": "Mini Task 8",
        "description": "Enable 1-order building reflections in SBR model.",
        "explanation": """### Task Steps:

**Change:**
```matlab
rtpm.MaxNumReflections = 1;
```

**Then:**
```matlab
raytrace(tx,rx1,rtpm,Type="pathloss");
```

Now MATLAB can find paths where the signal reaches the receiver after reflecting from a building.""",
        "challenge": "Run raytrace to see the reflected multipath ray.",
        "code": r"""rtpm.MaxNumReflections = 1;
raytrace(tx,rx1,rtpm,Type="pathloss");
"""
    },
    "Part 9": {
        "title": "PART 9 — Calculate Received Signal Strength",
        "badge": "Mini Task 9",
        "description": "Compute absolute power level in dBm at UE1.",
        "explanation": """### Students run:
```matlab
ss1 = sigstrength(rx1,tx,rtpm);
fprintf("UE1 received power = %.4f dBm\n", ss1);
```

`sigstrength` calculates the accumulated signal strength at the receiver.""",
        "challenge": "Move UE1 farther away and re-calculate power.",
        "code": r"""ss1 = sigstrength(rx1,tx,rtpm);
fprintf("UE1 received power = %.4f dBm\n", ss1);
"""
    },
    "Part 10": {
        "title": "PART 10 — Building Material Losses",
        "badge": "Mini Task 10",
        "description": "Replace ideal perfect reflectors with realistic concrete permittivity parameters.",
        "explanation": """### Students run:
```matlab
rtpm.BuildingsMaterial = "concrete";
rtpm.TerrainMaterial = "concrete";
```

**Then:**
```matlab
raytrace(tx,rx1,rtpm,Type="pathloss");
ss1_concrete = sigstrength(rx1,tx,rtpm);
```

Concrete absorbs and scatters energy, reducing reflected ray power compared to ideal reflectors.""",
        "challenge": "Calculate material loss: `materialLoss = ss1 - ss1_concrete`",
        "code": r"""rtpm.BuildingsMaterial = "concrete";
rtpm.TerrainMaterial = "concrete";

raytrace(tx,rx1,rtpm,Type="pathloss");
ss1_concrete = sigstrength(rx1,tx,rtpm);
fprintf("UE1 concrete received power = %.4f dBm\n", ss1_concrete);
"""
    },
    "Part 11": {
        "title": "PART 11 — Add Weather & Gas Attenuation",
        "badge": "Mini Task 11",
        "description": "Combine ray tracing with ITU atmospheric gas and rain loss models.",
        "explanation": """### Students create:
```matlab
rtPlusWeather = rtpm + propagationModel("gas") + propagationModel("rain");
```

**Then calculate:**
```matlab
ss1_weather = sigstrength(rx1, tx, rtPlusWeather);
```

Atmospheric gas absorption and rain attenuation introduce additional link losses.""",
        "challenge": "Compare `ss1_weather` with `ss1_concrete` to observe weather degradation.",
        "code": r"""rtPlusWeather = rtpm + propagationModel("gas") + propagationModel("rain");
ss1_weather = sigstrength(rx1, tx, rtPlusWeather);
fprintf("UE1 weather received power = %.4f dBm\n", ss1_weather);
"""
    },
    "Part 12": {
        "title": "PART 12 — Multi-Hop Reflections (Order 2)",
        "badge": "Mini Task 12",
        "description": "Allow double-bounce reflection paths (TX -> Building 1 -> Building 2 -> RX).",
        "explanation": """### Students modify:
```matlab
rtPlusWeather.PropagationModels(1).MaxNumReflections = 2;
rtPlusWeather.PropagationModels(1).AngularSeparation = "low";
```

**Then:**
```matlab
ss1_two_reflections = sigstrength(rx1,tx,rtPlusWeather);
```""",
        "challenge": "Set `MaxNumReflections = 2` and `AngularSeparation = 'low'`. ",
        "code": r"""rtPlusWeather.PropagationModels(1).MaxNumReflections = 2;
rtPlusWeather.PropagationModels(1).AngularSeparation = "low";

ss1_two_reflections = sigstrength(rx1,tx,rtPlusWeather);
fprintf("UE1 2 reflections power = %.4f dBm\n", ss1_two_reflections);
"""
    },
    "Part 13": {
        "title": "PART 13 — Add Edge Diffraction",
        "badge": "Mini Task 13",
        "description": "Incorporate knife-edge and building corner diffraction.",
        "explanation": """### Students set:
```matlab
rtPlusWeather.PropagationModels(1).MaxNumReflections = 2;
rtPlusWeather.PropagationModels(1).MaxNumDiffractions = 1;
```

**Then:**
```matlab
ss1_two_ref_one_diff = sigstrength(rx1,tx,rtPlusWeather);
```""",
        "challenge": "Observe how diffraction fills dead zones in non-line-of-sight street corners.",
        "code": r"""rtPlusWeather.PropagationModels(1).MaxNumReflections = 2;
rtPlusWeather.PropagationModels(1).MaxNumDiffractions = 1;

ss1_two_ref_one_diff = sigstrength(rx1,tx,rtPlusWeather);
fprintf("UE1 2 ref + 1 diff power = %.4f dBm\n", ss1_two_ref_one_diff);
"""
    },
    "Part 14": {
        "title": "PART 14 — Scenario Comparison Table",
        "badge": "Mini Task 14",
        "description": "Compare received power across all propagation configurations for UE1.",
        "explanation": """### Scenario Comparison Table:

| Scenario | Received Power |
| --- | --- |
| One reflection | ___ dBm |
| Concrete | ___ dBm |
| Concrete + weather | ___ dBm |
| Two reflections | ___ dBm |
| Two reflections + diffraction | ___ dBm |""",
        "challenge": "Which scenario produces the highest power? Which is lowest?",
        "code": r"""% Scenario Comparison Logging Script
fprintf("=== UE1 Propagation Comparison ===\n");
fprintf("1 Reflection          : %.4f dBm\n", ss1);
fprintf("Concrete Material     : %.4f dBm\n", ss1_concrete);
fprintf("Concrete + Weather    : %.4f dBm\n", ss1_weather);
fprintf("2 Reflections         : %.4f dBm\n", ss1_two_reflections);
fprintf("2 Ref + 1 Diffraction : %.4f dBm\n", ss1_two_ref_one_diff);
"""
    },
    "Part 15": {
        "title": "PART 15 — Reflection-Aware Coverage Map",
        "badge": "Mini Task 15",
        "description": "Generate coverage map including 1-order reflections.",
        "explanation": """### Set:
```matlab
rtPlusWeather.PropagationModels(1).MaxNumReflections = 1;
rtPlusWeather.PropagationModels(1).MaxNumDiffractions = 0;
```

**Then:**
```matlab
coverage(tx,rtPlusWeather, ...
    SignalStrengths=-120:-5, ...
    MaxRange=250, ...
    Resolution=5, ...
    Transparency=0.6);
```""",
        "challenge": "Compare LOS vs Reflection coverage visually in Site Viewer.",
        "code": r"""rtPlusWeather.PropagationModels(1).MaxNumReflections = 1;
rtPlusWeather.PropagationModels(1).MaxNumDiffractions = 0;

coverage(tx,rtPlusWeather, ...
    SignalStrengths=-120:-5, ...
    MaxRange=250, ...
    Resolution=5, ...
    Transparency=0.6);
"""
    },
    "Part 16": {
        "title": "PART 16 — Advanced Urban Coverage Map",
        "badge": "Mini Task 16",
        "description": "Generate full coverage map with 2 reflections and 1 diffraction.",
        "explanation": """### Configure:
```matlab
rtPlusWeather.PropagationModels(1).MaxNumReflections = 2;
rtPlusWeather.PropagationModels(1).MaxNumDiffractions = 1;
rtPlusWeather.PropagationModels(1).AngularSeparation = "high";
```

**Then calculate:**
```matlab
coverage(tx,rtPlusWeather, ...
    SignalStrengths=-120:-5, ...
    MaxRange=250, ...
    Resolution=5, ...
    Transparency=0.6);
```""",
        "challenge": "Observe detailed power contours inside urban building blocks.",
        "code": r"""rtPlusWeather.PropagationModels(1).MaxNumReflections = 2;
rtPlusWeather.PropagationModels(1).MaxNumDiffractions = 1;
rtPlusWeather.PropagationModels(1).AngularSeparation = "high";

coverage(tx,rtPlusWeather, ...
    SignalStrengths=-120:-5, ...
    MaxRange=250, ...
    Resolution=5, ...
    Transparency=0.6);
"""
    },
    "Part 17": {
        "title": "PART 17 — Introduce User Equipment 2 (UE2)",
        "badge": "Mini Task 17",
        "description": "Add a second user device to transition to multi-user simulation.",
        "explanation": """### Students create:
```matlab
rx2 = rxsite( ...
    Name="User Equipment 2", ...
    Latitude=41.880600, ...
    Longitude=-87.628800, ...
    AntennaHeight=30);

show(rx2);
```""",
        "challenge": "Place UE2 at Latitude 41.880600, Longitude -87.628800.",
        "code": r"""rx2 = rxsite( ...
    Name="User Equipment 2", ...
    Latitude=41.880600, ...
    Longitude=-87.628800, ...
    AntennaHeight=30);

show(rx2);

los(tx,rx2);
raytrace(tx,rx2,rtpm);
ss2 = sigstrength(rx2,tx,rtpm);
fprintf("UE2 received power = %.4f dBm\n", ss2);
"""
    },
    "Part 18": {
        "title": "PART 18 — Multi-User Link Comparison",
        "badge": "Mini Task 18",
        "description": "Compare link budget metrics between UE1 and UE2.",
        "explanation": """### Multi-User Comparison:

| Parameter | UE1 | UE2 |
| --- | --- | --- |
| LOS/NLOS | ___ | ___ |
| One reflection | ___ dBm | ___ dBm |
| Concrete | ___ dBm | ___ dBm |
| Weather | ___ dBm | ___ dBm |
| Two reflections | ___ dBm | ___ dBm |
| Reflection + diffraction | ___ dBm | ___ dBm |""",
        "challenge": "Why are received powers different for users on the same cell tower?\n\n*Answer*: Path length, building shadowing, number of reflections, and local diffraction angles differ for each user coordinate.",
        "code": r"""% Compare UE1 and UE2
fprintf("UE1 Received Power: %.4f dBm\n", ss1_two_ref_one_diff);
fprintf("UE2 Received Power: %.4f dBm\n", ss2);
"""
    },
    "Part 19 (no code)": {
        "title": "PART 19 — Why Directional Antennas?",
        "badge": "Mini Task 19",
        "description": "Understand isotropic/omnidirectional vs directional array beamforming.",
        "explanation": "Omnidirectional antennas radiate power in 360 degrees, wasting energy. Directional phased arrays focus energy into sharp narrow beams targeted directly at users.",
        "challenge": "How much gain can an 8x8 phased array provide over an isotropic antenna?",
        "code": r"""% Conceptual overview: Replacing isotropic antenna with 8x8 Uniform Rectangular Array (URA)
"""
    },
    "Part 20": {
        "title": "PART 20 — Create 8x8 Phased Antenna Array",
        "badge": "Mini Task 20",
        "description": "Design an 8x8 (64-element) Uniform Rectangular Array (URA) with half-wavelength spacing.",
        "explanation": """### Students create custom antenna element pattern & array:
```matlab
azvec = -180:180;
elvec = -90:90;
SLA = 30;
tilt = 0;
az3dB = 65;
el3dB = 65;

lambda = physconst("lightspeed") / tx.TransmitterFrequency;
[az,el] = meshgrid(azvec,elvec);

azMagPattern = -min(12*(az/az3dB).^2,SLA);
elMagPattern = -min(12*((el-tilt)/el3dB).^2,SLA);
combinedMagPattern = -min(-(azMagPattern + elMagPattern),SLA);

antennaElement = phased.CustomAntennaElement(MagnitudePattern=combinedMagPattern);

tx.Antenna = phased.URA( ...
    Size=[8 8], ...
    Element=antennaElement, ...
    ElementSpacing=[lambda/2 lambda/2]);
```""",
        "challenge": "Calculate wavelength `lambda = c / f` and verify `lambda/2` element spacing.",
        "code": r"""azvec = -180:180;
elvec = -90:90;
SLA = 30;
tilt = 0;
az3dB = 65;
el3dB = 65;

lambda = physconst("lightspeed") / tx.TransmitterFrequency;
[az,el] = meshgrid(azvec,elvec);

azMagPattern = -min(12*(az/az3dB).^2,SLA);
elMagPattern = -min(12*((el-tilt)/el3dB).^2,SLA);
combinedMagPattern = -min(-(azMagPattern + elMagPattern),SLA);

antennaElement = phased.CustomAntennaElement(MagnitudePattern=combinedMagPattern);

tx.Antenna = phased.URA( ...
    Size=[8 8], ...
    Element=antennaElement, ...
    ElementSpacing=[lambda/2 lambda/2]);
"""
    },
    "Part 21": {
        "title": "PART 21 — Calculate Antenna Directivity",
        "badge": "Mini Task 21",
        "description": "Compute peak directivity in dBi of the 64-element antenna array.",
        "explanation": """### Students run:
```matlab
antennaDirectivity = pattern(tx.Antenna,tx.TransmitterFrequency);
antennaDirectivityMax = max(antennaDirectivity(:));
fprintf("Peak antenna directivity = %.4f dBi\n", antennaDirectivityMax);
```""",
        "challenge": "Peak directivity increases proportionally with the logarithm of total array elements.",
        "code": r"""antennaDirectivity = pattern(tx.Antenna,tx.TransmitterFrequency);
antennaDirectivityMax = max(antennaDirectivity(:));
fprintf("Peak antenna directivity = %.4f dBi\n", antennaDirectivityMax);
"""
    },
    "Part 22": {
        "title": "PART 22 — Visualize 3D Radiation Pattern",
        "badge": "Mini Task 22",
        "description": "Overlay 3D radiation lobes onto the base station in Site Viewer.",
        "explanation": """### Set:
```matlab
tx.AntennaAngle = -90;
```

**Then:**
```matlab
pattern(tx,Transparency=0.6);
```""",
        "challenge": "Set `tx.AntennaAngle = -90` and view main lobe alignment.",
        "code": r"""tx.AntennaAngle = -90;
pattern(tx,Transparency=0.6);
"""
    },
    "Part 23": {
        "title": "PART 23 — Extract Dominant Propagation Path",
        "badge": "Mini Task 23",
        "description": "Extract path parameters from ray trace objects.",
        "explanation": """### Students use:
```matlab
ray = raytrace(tx,rx1,rtPlusWeather);
disp(ray{1});
```""",
        "challenge": "Inspect `ray{1}` parameters to identify strongest ray component.",
        "code": r"""ray = raytrace(tx,rx1,rtPlusWeather);
disp(ray{1});
"""
    },
    "Part 24": {
        "title": "PART 24 — Extract Angle of Departure",
        "badge": "Mini Task 24",
        "description": "Extract Azimuth and Elevation departure angles of dominant ray.",
        "explanation": """### Students run:
```matlab
aod = ray{1}.AngleOfDeparture;
fprintf("Azimuth = %.4f degrees\n",aod(1));
fprintf("Elevation = %.4f degrees\n",aod(2));
```""",
        "challenge": "Print azimuth and elevation angles for UE1 path.",
        "code": r"""aod = ray{1}.AngleOfDeparture;
fprintf("Azimuth = %.4f degrees\n",aod(1));
fprintf("Elevation = %.4f degrees\n",aod(2));
"""
    },
    "Part 25": {
        "title": "PART 25 — Apply Phased Array Beam Steering",
        "badge": "Mini Task 25",
        "description": "Compute complex steering vector and apply array taper weights.",
        "explanation": """### Task Steps:

**Calculate:**
```matlab
steeringaz = wrapTo180(aod(1)-tx.AntennaAngle(1));
```

**Create the steering vector:**
```matlab
steeringVector = phased.SteeringVector(SensorArray=tx.Antenna);
```

**Then:**
```matlab
sv = steeringVector(tx.TransmitterFrequency, [steeringaz;aod(2)]);
```

**Apply it:**
```matlab
tx.Antenna.Taper = conj(sv);
```""",
        "challenge": "Verify `tx.Antenna.Taper = conj(sv)` applies maximum gain towards target path.",
        "code": r"""steeringaz = wrapTo180(aod(1)-tx.AntennaAngle(1));
steeringVector = phased.SteeringVector(SensorArray=tx.Antenna);
sv = steeringVector(tx.TransmitterFrequency, [steeringaz;aod(2)]);

tx.Antenna.Taper = conj(sv);
"""
    },
    "Part 26": {
        "title": "PART 26 — Measure Beam Steering Gain Improvement",
        "badge": "Mini Task 26",
        "description": "Quantify SNR/power enhancement after beam steering on NLOS link.",
        "explanation": """### Calculate:
```matlab
ss1_beam_steering = sigstrength(rx1,tx,rtPlusWeather);
beamGainImprovement1 = ss1_beam_steering - ss1_weather;
```""",
        "challenge": "Calculate `gainImprovement = ss1_beam_steering - ss1_weather`",
        "code": r"""ss1_beam_steering = sigstrength(rx1,tx,rtPlusWeather);
beamGainImprovement1 = ss1_beam_steering - ss1_weather;

fprintf("Before beam steering: %.4f dBm\n", ss1_weather);
fprintf("After beam steering : %.4f dBm\n", ss1_beam_steering);
fprintf("Improvement          : %.4f dB\n", beamGainImprovement1);
"""
    },
    "Part 27": {
        "title": "PART 27 — Challenge: Beam Steering for UE2",
        "badge": "Mini Challenge 8",
        "description": "Perform full ray extraction, AoD calculation, steering vector weight synthesis, and beam steering for UE2 independently.",
        "explanation": """### Students repeat beam-steering for UE2:
1. Calculate UE2 ray.
2. Extract UE2 angle of departure.
3. Calculate UE2 steering angle.
4. Generate UE2 steering vector.
5. Apply antenna taper `tx.Antenna.Taper = conj(sv2);`
6. Calculate beam-steering improvement.""",
        "challenge": "Complete table for UE2 before vs after beam steering.",
        "code": r"""%% PART 27 — Challenge Solution: Beam Steering for UE2
ray2 = raytrace(tx,rx2,rtPlusWeather);
aod2 = ray2{1}.AngleOfDeparture;

steeringaz2 = wrapTo180(aod2(1)-tx.AntennaAngle(1));
sv2 = steeringVector(tx.TransmitterFrequency, [steeringaz2;aod2(2)]);

tx.Antenna.Taper = conj(sv2);

ss2_beam_steering = sigstrength(rx2,tx,rtPlusWeather);
beamGainImprovement2 = ss2_beam_steering - ss2;

fprintf("UE2 Power Before Steering: %.4f dBm\n", ss2);
fprintf("UE2 Power After Steering : %.4f dBm\n", ss2_beam_steering);
fprintf("UE2 Beam Gain Improvement : %.4f dB\n", beamGainImprovement2);
"""
    },
    "Final Challenge": {
        "title": "Final Workshop Challenge 🏆 — Add UE3 & Complete Analysis",
        "badge": "Final Hands-On Challenge",
        "description": "Add User Equipment 3 (UE3), execute complete propagation analysis (LOS, reflections, concrete, weather, diffraction), and apply beam steering.",
        "explanation": """Students work independently (15-20 mins) to implement multi-user 3D Ray Tracing for UE3:
1. Place UE3 at a new urban coordinate.
2. Calculate LOS / 1-Reflection / Concrete / Weather / 2-Reflections + 1-Diffraction.
3. Extract dominant ray & AoD.
4. Synthesize beam steering vector & apply array taper.
5. Measure power improvement and build comparative matrix.""",
        "challenge": "Fill comparative matrix for UE1, UE2, and UE3.",
        "code": r"""%% Final Workshop Challenge — Complete Analysis for UE3
rx3 = rxsite( ...
    Name="User Equipment 3", ...
    Latitude=41.879500, ...
    Longitude=-87.630500, ...
    AntennaHeight=25);

show(rx3);

% 1. Check LOS
los(tx,rx3);

% 2. Full Ray Tracing with Weather & Diffraction
ray3 = raytrace(tx,rx3,rtPlusWeather);
ss3_initial = sigstrength(rx3,tx,rtPlusWeather);

% 3. Extract AoD
aod3 = ray3{1}.AngleOfDeparture;

% 4. Beam Steering
steeringaz3 = wrapTo180(aod3(1)-tx.AntennaAngle(1));
sv3 = steeringVector(tx.TransmitterFrequency, [steeringaz3;aod3(2)]);
tx.Antenna.Taper = conj(sv3);

% 5. Measured Power Post Steering
ss3_steered = sigstrength(rx3,tx,rtPlusWeather);
improvement3 = ss3_steered - ss3_initial;

fprintf("=== UE3 Final Results ===\n");
fprintf("Initial Power : %.4f dBm\n", ss3_initial);
fprintf("Steered Power : %.4f dBm\n", ss3_steered);
fprintf("Gain Improvement: %.4f dB\n", improvement3);
"""
    }
}

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/satellite-tower.png", width=70)
st.sidebar.title("IEEE MATLAB Workshop")
st.sidebar.markdown("**Urban Ray Tracing & 5G Beam Steering**")

# Sidebar navigation options cleanly listed as requested by user
sidebar_options = list(PARTS.keys()) + ["6-Hour Schedule"]
selected_option = st.sidebar.radio("Select Module / Option", sidebar_options)

if selected_option in PARTS:
    part_key = selected_option
    part_data = PARTS[part_key]

    st.markdown(f'<div class="badge">{part_data["badge"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="main-header">{part_data["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{part_data["description"]}</div>', unsafe_allow_html=True)

    # 1. CODE AND COPY OPTION FIRST
    st.markdown("### 💻 MATLAB Code & Copy Option")
    code = part_data["code"]
    js_safe = code.replace('\\','\\\\').replace('`','\\`')

    with st.sidebar:
        st.markdown("---")
        st.markdown("### Quick Copy & Download")
        components.html(f"""
        <div style='padding:4px;display:flex;justify-content:center;'>
            <button style='width:100%;padding:10px;border-radius:6px;border:none;background:#006699;color:#fff;cursor:pointer;font-weight:700;' onclick="navigator.clipboard.writeText(`{js_safe}`)">📋 Copy {part_key} Code</button>
        </div>
        """, height=65)
        st.download_button(f"📥 Download {part_key} (.m)", code, file_name=f"{part_key.replace(' ', '_')}.m", mime="text/plain")

    pre_id = f"code_{abs(hash(part_key))}"
    esc = html.escape(code)
    num_lines = len(code.strip().split('\n'))
    box_height = min(max(num_lines * 22 + 65, 110), 450)
    components.html(f"""
    <div style='background:#1e1e1e;color:#d4d4d4;padding:14px;border-radius:8px;position:relative;font-family:Consolas, Monaco, "Andale Mono", monospace;'>
        <button style='position:absolute;top:10px;right:10px;padding:6px 14px;border-radius:4px;border:none;background:#007bff;color:#fff;cursor:pointer;z-index:2;font-weight:600;display:inline-flex;align-items:center;gap:4px;' 
            onclick="(() => {{
                const btn = event.target;
                const text = document.getElementById('{pre_id}').innerText;
                navigator.clipboard.writeText(text)
                    .then(() => {{
                        btn.innerHTML = '✓ Copied';
                        setTimeout(() => btn.innerHTML = 'Copy Code', 1200);
                    }})
                    .catch(err => alert('Copy error: ' + err));
            }})()">Copy Code</button>
        <pre id='{pre_id}' style='white-space:pre-wrap;font-size:14px;margin-top:28px;max-height:400px;overflow-y:auto;color:#d4d4d4;'>{esc}</pre>
    </div>
    """, height=box_height)

    st.markdown("---")

    # 2. REST OF INFO SECOND
    st.markdown("### 📖 Detailed Explanation & Workshop Info")
    with st.expander("📌 Theoretical Overview & Parameter Reference", expanded=True):
        st.markdown(part_data["explanation"])

    if "challenge" in part_data and part_data["challenge"]:
        with st.expander("💡 Mini Challenge & Expected Outcome", expanded=True):
            st.markdown(part_data["challenge"])

elif selected_option == "6-Hour Schedule":
    st.markdown('<div class="main-header">Recommended 6-Hour Workshop Structure</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Time breakdown for hosting the IEEE 5G Urban Propagation & Ray Tracing Workshop.</div>', unsafe_allow_html=True)

    schedule_data = [
        ("0:00 – 0:20", "Introduction to wireless propagation and ray tracing fundamentals"),
        ("0:20 – 0:45", "MATLAB environment setup & Chicago 3D OpenStreetMap import"),
        ("0:45 – 1:15", "5G Base Station (TX) & User Equipment (UE1) site creation"),
        ("0:15 – 1:45", "LOS / NLOS check & initial SBR ray tracing execution"),
        ("1:45 – 2:15", "Received signal strength calculation & 2D/3D coverage maps"),
        ("2:15 – 2:30", "☕ Coffee & Networking Break"),
        ("2:30 – 3:00", "Building material losses (Concrete) & ITU weather/rain attenuation"),
        ("3:00 – 3:30", "Multi-hop reflections (Order 2) & edge diffraction models"),
        ("3:30 – 4:00", "⭐ Challenge 1: Add UE2 & perform complete propagation analysis"),
        ("4:00 – 4:30", "8x8 (64-element) phased antenna array & radiation pattern visualization"),
        ("4:30 – 5:00", "Dominant ray extraction & complex beam steering vector synthesis"),
        ("5:00 – 5:30", "⭐ Challenge 2: Beam steering for UE2 & power gain evaluation"),
        ("5:30 – 6:00", "🏆 Final Challenge: Add UE3 + comparative matrix + closing Q&A")
    ]

    for time_slot, activity in schedule_data:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"**`{time_slot}`**")
        with col2:
            st.markdown(activity)
        st.markdown("---")
