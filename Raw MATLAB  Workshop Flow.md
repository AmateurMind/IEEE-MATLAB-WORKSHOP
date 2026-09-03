## **Urban Link and Coverage Analysis Using Ray Tracing in MATLAB**

### **Overall objective**

By the end of the workshop, students should be able to take a real urban map, place a 5G base station and multiple user equipment on it, simulate propagation using ray tracing, analyse received power, study the effects of buildings/materials/weather, generate coverage maps, and finally use beam steering to improve a non-line-of-sight link.

---

# **PART 1 — Getting Started with the Urban Environment**

## **Mini Task 1: Understand the Problem**

### **What are we trying to simulate?**

Imagine a 5G base station installed somewhere in a city.

A mobile user is somewhere nearby.

The signal from the base station can travel:

**Directly to the user**  
→ Line-of-Sight (LOS)

or it can interact with buildings:

**Base Station → Building → User**  
→ Reflection

or:

**Base Station → Building Edge → User**  
→ Diffraction

There can also be multiple reflections:

**Base Station → Building 1 → Building 2 → User**

This is what ray tracing allows us to study.

### **Student objective**

Understand the difference between:

- LOS propagation
- Reflected propagation
- Diffracted propagation
- NLOS communication

# **PART 2 — Load a Real City**

## **Mini Task 2: Import Chicago 3-D Buildings**

Students run:

**clc;**  
**clear;**  
**close all;**

**viewer \= siteviewer(...**  
**Buildings="chicago.osm", ...**  
**Basemap="topographic");**

### **Explain**

`siteviewer` creates the MATLAB environment where we can visualise:

- Buildings
- Transmitter
- Receivers
- Propagation paths
- Coverage maps

The file:

Chicago, OSM

contains OpenStreetMap building information.

### **What students should observe**

They should see a 3-D representation of Chicago in Site Viewer.

### **Mini Challenge 1**

Ask students to:

> Change the basemap from `"topographic"` to another available basemap and observe the difference.

The important learning outcome is understanding that the propagation simulation uses a **real geographical environment**, rather than an idealized empty space.

---

# **PART 3 — Create the 5G Base Station**

## **Mini Task 3: Define the Transmitter**

Students create:

**tx \= txsite( ...**  
**Name="5G Base Station", ...**  
**Latitude=41.8800,...**  
**Longitude=-87.6295,...**  
**AntennaHeight=25, ...**  
**TransmitterPower=10, ...**  
**TransmitterFrequency=2.5e9);**

Then:

show(tx);

### **Explain every parameter.**

| Parameter               | Meaning                         |
| ----------------------- | ------------------------------- |
| `Latitude`              | Geographic latitude             |
| `Longitude`             | Geographic longitude            |
| `AntennaHeight`         | Height of base-station antenna  |
| `Transmitter Power`     | Transmitted power               |
| `Transmitter Frequency` | Carrier frequency               |
| `Name`                  | Identifier shown in Site Viewer |

Here:

Frequency \= 2.5 GHz  
Power \= 10 W  
Height \= 25 m

---

# **PART 4 — Create the First User Equipment**

## **Mini Task 4: Place UE1**

Students create:

**rx1 \= rxsite( ...**  
**Name="User Equipment 1", ...**  
**Latitude=41.881352, ...**  
**Longitude=-87.629771, ...**  
**AntennaHeight=30);**

Then:

**show(rx1);**

### **Explain**

An `RX site` represents a receiving device.

For example:

5G Base Station  
↓  
Signal  
↓  
UE1

The receiver has a location and antenna height.

### **Important concept**

The coordinates must be geographically close to the transmitter for ray tracing.

Students should understand that a longitude mistake such as

Longitude=-0.629771

instead of:

Longitude=-87.629771

can place the receiver thousands of kilometres away.

---

# **PART 5 — Check Line of Sight**

## **Mini Task 5: Determine Whether UE1 Has LOS**

Students run:

los(tx,rx1);

### **Explain**

LOS asks:

> Is there a clear direct path between transmitter and receiver?

Conceptually:

TX \---------------------- RX  
Clear path  
\= LOS

or:

TX \-------- Building \-------- RX  
↑  
Blocked path  
\= NLOS

### **What students should observe**

The visualisation indicates whether buildings obstruct the direct path.

### **Mini Challenge 3**

Ask students:

> Move UE1 to another location on the map.

Then run:

los(tx,rx1);

Students should find a location where the link changes from LOS to NLOS.

This teaches an important idea:

**Location strongly affects wireless communication.**

---

# **PART 6 — Create the Ray-Tracing Model**

## **Mini Task 6: Start with LOS Ray Tracing**

Students create:

**rtpm \= propagationModel("raytracing", ...**  
**Method="sbr", ...**  
**MaxNumReflections=0, ...**  
**MaxNumDiffractions=0);**

### **Explain SBR**

SBR means:

**Shooting and Bouncing Rays**

MATLAB launches rays from the transmitter and determines how they interact with the environment.

At this stage:

Reflections \= 0  
Diffractions \= 0

So we are considering the direct LOS case.

---

# **PART 7 — Generate the First Coverage Map**

## **Mini Task 7: Visualize LOS Coverage**

Students run:

**coverage (tx, rtpm, ...**  
**SignalStrengths=-120:-5, ...**  
**MaxRange=250, ...**  
**Resolution=5, ...**  
**Transparency=0.6);**

### **Explain the parameters.**

`Signal Strengths:`

\-120:-5

defines the received-power levels displayed.

`MaxRange`:

250

means the simulation considers a maximum range of 250 m.

`Resolution`:

5

controls the spatial sampling of the coverage calculation.

### **What students learn**

The coverage map answers:

> "Where can a user receive a sufficiently strong signal from this base station?"

---

# **PART 8 — Introduce NLOS Propagation**

## **Mini Task 8: Add Reflection**

Change:

**rtpm. MaxNumReflections \= 1;**

Then:

**raytrace(tx,rx1,rtpm,Type="pathloss");**

### **Explain**

Now MATLAB can find paths such as

              Building
              /

TX \----------/  
\\  
\\------ RX

The signal reaches the receiver after reflecting from a building.

This is especially important in dense urban environments.

---

# **PART 9 — Calculate Received Signal Strength**

## **Mini Task 9: Calculate Received Power**

Run:

**ss1 \= sigstrength(rx1,tx,rtpm);**

**fprintf("UE1 received power \= %.4f dBm\\n",ss1);**

### **Explain**

`sigstrength` calculates the signal strength at the receiver.

Students should understand:

Higher received power  
↓  
Better link condition

Lower received power  
↓  
Potentially poorer link condition

### **Mini Challenge 4**

Ask students:

> Move UE1 farther away from the transmitter and calculate the received power again.

Then ask:

> "Did the received power increase or decrease?"

---

# **PART 10 — Study Building Materials**

## **Mini Task 10: Replace Ideal Materials with Concrete**

Students run:

**rtpm.BuildingsMaterial \= "concrete";**  
**rtpm.TerrainMaterial \= "concrete";**

Then:

**raytrace(tx,rx1,rtpm,Type="pathloss");**

**ss1_concrete \= sigstrength(rx1,tx,rtpm);**

### **Explain**

The first simulation uses idealised propagation assumptions.

Real buildings are not perfect reflectors.

Concrete causes additional propagation loss.

Students compare:

Before concrete  
↓  
Received power

After concrete  
↓  
Received power

### **Mini Challenge 5**

Ask:

> Calculate the difference.

materialLoss \= ss1 \- ss1_concrete;

Then ask students:

> Why is the second value different?

---

# **PART 11 — Add Weather Effects**

## **Mini Task 11: Include Gas and Rain Loss**

Students create:

**rtPlusWeather \= ...**  
**rtpm \+ propagationModel("gas") ...**  
**\+ propagationModel("rain");**

Then calculate:

**ss1_weather \= sigstrength(rx1, tx, rtPlusWeather);**

### **Explain**

Wireless propagation can also experience atmospheric losses.

The model now includes:

- Building effects
- Terrain effects
- Atmospheric gas attenuation
- Rain attenuation;

---

# **PART 12 — Increase the Number of Reflections**

## **Mini Task 12: Two Reflections**

Students modify:

**rtPlusWeather.PropagationModels(1).MaxNumReflections \= 2;**

and:

**rtPlusWeather.PropagationModels(1).AngularSeparation \= "low";**

Then:

**ss1_two_reflections \= ...**  
**sigstrength(rx1,tx,rtPlusWeather);**

### **Explain**

Now MATLAB looks for paths involving up to two reflections.

For example:

TX → Building 1 → RX

versus:

TX → Building 1 → Building 2 → RX

The second case requires more computational effort.

### **Important concept**

More rays and interactions can reveal additional propagation paths, but computation becomes more expensive.

---

# **PART 13 — Add Diffraction**

## **Mini Task 13: Reflection \+ Diffraction**

Students set:

**rtPlusWeather.PropagationModels(1).MaxNumReflections \= 2;**  
**rtPlusWeather.PropagationModels(1).MaxNumDiffractions \= 1;**

Then:

**ss1_two_ref_one_diff \= ...**  
**sigstrength(rx1,tx,rtPlusWeather);**

### **Explain diffraction**

Diffraction allows energy to bend around edges.

Conceptually:

       Building
       ┌─────────┐

TX ────┘ └──── RX  
↑  
Edge diffraction

This is important when the direct path is blocked.

---

# **PART 14 — Compare All Propagation Conditions**

## **Mini Task 14: Build a Comparison**

Students should record:

|            Scenario            | Received Power |
| :----------------------------: | :------------: |
|         One reflection         |   \_\_\_ dBm   |
|            Concrete            |   \_\_\_ dBm   |
|      Concrete \+ weather       |   \_\_\_ dBm   |
|        Two reflections         |   \_\_\_ dBm   |
| Two reflections \+ diffraction |   \_\_\_ dBm   |

### **Mini Challenge 7**

Ask students:

> Which propagation condition gives the strongest received power?

Then:

> Which condition gives the weakest?

The purpose is not simply to get the "right number," but to understand **why the number changes**.

---

# **PART 15 — Create a Detailed Coverage Map**

## **Mini Task 15: Single-Reflection Coverage**

Set:

**rtPlusWeather.PropagationModels(1).MaxNumReflections \= 1;**  
**rtPlusWeather.PropagationModels(1).MaxNumDiffractions \= 0;**

Then:

**coverage(tx,rtPlusWeather, ...**  
**SignalStrengths=-120:-5, ...**  
**MaxRange=250, ...**  
**Resolution=5, ...**  
**Transparency=0.6);**

### **Students compare**

**LOS coverage**

versus

**Reflection-aware coverage**

They should observe that the coverage pattern becomes affected by buildings and multipath.

---

# **PART 16 — Advanced Coverage**

## **Mini Task 16: Two Reflections \+ One Diffraction**

Configure:

**rtPlusWeather.PropagationModels(1).MaxNumReflections \= 2;**  
**rtPlusWeather.PropagationModels(1).MaxNumDiffractions \= 1;**  
**rtPlusWeather.PropagationModels(1).AngularSeparation \= "high";**

Then calculate:

**coverage(tx,rtPlusWeather, ...**  
**SignalStrengths=-120:-5, ...**  
**MaxRange=250, ...**  
**Resolution=5, ...**  
**Transparency=0.6);**

### **Explain**

`AngularSeparation="high"` means fewer rays are launched.

Therefore:

High angular separation  
↓  
Fewer rays  
↓  
Faster computation  
↓  
Less detailed result

While:

Low angular separation  
↓  
More rays  
↓  
Longer computation  
↓  
More detailed propagation analysis

---

# **PART 17 — Introduce a Second User Equipment**

## **Mini Task 17: Add UE2**

This is where the students begin modifying the original project themselves.

**Give them:**

**rx2 \= rxsite( ...**  
**Name="User Equipment 2", ...**  
**Latitude=41.880600, ...**  
**Longitude=-87.628800, ...**  
**AntennaHeight=30);**

Then:

**show(rx2);**

Now the network becomes:

                ┌── UE1
                 │
          TX ────┤
                 │
                 └── UE2

### **Explain**

A real 5G base station does not normally communicate with only one device.

Now students are moving toward a **multi-user wireless scenario**.

---

# **MINI CHALLENGE 8**

## **Students Repeat the Entire Analysis for UE2**

This should be an important hands-on challenge.

Tell students:

> "You have already completed the analysis for UE1. Now do the complete analysis for UE2 without copying the final results."

Students must perform:

### **Step A**

Check LOS:

**los(tx,rx2);**

### **Step B**

Calculate reflected paths:

**raytrace(tx,rx2,rtpm);**

### **Step C**

Calculate received power:

**ss2 \= sigstrength(rx2,tx,rtpm);**

### **Step D**

Add concrete materials.

### **Step E**

Calculate concrete received power.

### **Step F**

Add weather.

### **Step G**

Calculate weather-affected received power.

### **Step H**

Increase reflections to 2\.

### **Step I**

Add one diffraction.

### **Step J**

Generate the propagation paths.

### **Step K**

Generate the coverage map.

Now students have independently repeated the complete process.

---

# **PART 18 — Compare UE1 and UE2**

## **Mini Task 18: Multi-User Comparison**

Students create a table:

|         Parameter         |    UE1     |    UE2     |
| :-----------------------: | :--------: | :--------: |
|         LOS/NLOS          |   \_\_\_   |   \_\_\_   |
|      One reflection       | \_\_\_ dBm | \_\_\_ dBm |
|         Concrete          | \_\_\_ dBm | \_\_\_ dBm |
|          Weather          | \_\_\_ dBm | \_\_\_ dBm |
|      Two reflections      | \_\_\_ dBm | \_\_\_ dBm |
| Reflection \+ diffraction | \_\_\_ dBm | \_\_\_ dBm |

### **Mini Challenge 9 ⭐**

Ask:

> Both users are connected to the same base station. Why are their received powers different?

Expected discussion:

- Different distances
- Different building obstructions
- Different propagation paths
- Different reflection points
- Different diffraction conditions

This is an excellent point to explain that **wireless performance depends heavily on location**.

---

# **PART 19—Introduce Antenna Directivity**

## **Mini Task 19: Why Do We Need Directional Antennas?**

So far, the transmitter uses an approximately omnidirectional/isotropic antenna.

Ask students:

> "What if we could concentrate the transmitted energy toward the receiver?"

Explain:

Omnidirectional antenna

       ↑

↗ ↑ ↖  
← TX →  
↘ ↓ ↙

versus:

Directional antenna

          \>\>\>\>\>\>
        \>\>\>\>\>\>\>\>\>\>
       \>\>\> TX \>\>\>\>
        \>\>\>\>\>\>\>\>\>\>
          \>\>\>\>\>\>

A directional antenna can provide higher gain in a desired direction.

---

# **PART 20 — Create an 8×8 Antenna Array**

## **Mini Task 20: Create the Antenna**

Students create the custom antenna pattern:

**azvec \= \-180:180;**  
**elvec \= \-90:90;**

**SLA \= 30;**  
**tilt \= 0;**  
**az3dB \= 65;**  
**el3dB \= 65;**

**lambda \= ...**  
**physconst("lightspeed") / ...**  
**tx.TransmitterFrequency;**

**\[az,el\] \= meshgrid(azvec,elvec);**

**azMagPattern \= ...**  
**\-min(12\*(az/az3dB).^2,SLA);**

**elMagPattern \= ...**  
**\-min(12\*((el-tilt)/el3dB).^2,SLA);**

**combinedMagPattern \= ...**  
**\-min(-(azMagPattern \+ elMagPattern),SLA);**

Then:

**antennaElement \= phased.CustomAntennaElement( ...**  
**MagnitudePattern=combinedMagPattern);**

**And:**

**tx.Antenna \= phased.URA( ...**  
**Size=\[8 8\], ...**  
**Element=antennaElement, ...**  
**ElementSpacing=\[lambda/2 lambda/2\]);**

### **Explain**

The transmitter now uses:

**8 × 8 \= 64 antenna elements**

This introduces the idea of a phased antenna array used in modern cellular systems.

---

# **PART 21 — Calculate Antenna Directivity**

## **Mini Task 21**

Students run:

**antennaDirectivity \= ...**  
**pattern(tx.Antenna,tx.TransmitterFrequency);**

**antennaDirectivityMax \= ...**  
**max(antennaDirectivity(:));**

Then:

**fprintf("Peak antenna directivity \= %.4f dBi\\n", ...**  
**antennaDirectivityMax);**

### **Explain**

Directivity indicates how strongly the antenna concentrates energy in a particular direction compared with an isotropic radiator.

---

# **PART 22—Visualize the Radiation Pattern**

## **Mini Task 22**

Set:

**tx.AntennaAngle \= \-90;**

Then:

**pattern(tx,Transparency=0.6);**

### **Students observe**

The 3-D radiation pattern shows where the antenna is directing energy.

This connects:

**Antenna design → propagation → received power**

---

# **PART 23 — Find the Dominant Propagation Path**

## **Mini Task 23**

Students use:

**ray \= raytrace(tx,rx1,rtPlusWeather);**

Then:

**disp(ray{1});**

### **Explain**

The ray object contains information such as:

- Propagation distance
- Path loss
- Phase shift
- Angle of departure
- Angle of arrival
- Number of interactions
- LOS/NLOS condition

This moves the students from simply **looking at the simulation** to actually **extracting propagation data**.

---

# **PART 24—Extract Angle of Departure**

## **Mini Task 24**

**aod \= ray{1}.AngleOfDeparture;**

Then:

**fprintf("Azimuth \= %.4f degrees\\n",aod(1));**  
**fprintf("Elevation \= %.4f degrees\\n",aod(2));**

### **Explain**

The transmitter needs to know:

> In which direction should the antenna beam point?

The ray-tracing result tells us the direction of the dominant path.

---

#

# **PART 25 — Beam Steering**

## **Mini Task 25**

Calculate:

**steeringaz \= ...**  
**wrapTo180(aod(1)-tx.AntennaAngle(1));**

**Create the steering vector:**

**steeringVector \= phased.SteeringVector( ...**  
**SensorArray=tx.Antenna);**

**Then:**

**sv \= steeringVector( ...**  
**tx.TransmitterFrequency, ...**  
**\[steeringaz;aod(2)\]);**

Apply it:

**tx.Antenna.Taper \= conj(sv);**

### **Explain**

Before steering:

TX antenna  
↓  
Beam not optimally aligned  
↓  
Lower received power

After steering:

TX antenna  
\>\>\>\>\>\>\>\>\>\>\> UE  
Beam aligned  
\>\>\>\>\>\>\>\>\>\>\> UE  
↓  
Higher received power

---

# **PART 26 — Measure Beam-Steering Improvement**

## **Mini Task 26**

Calculate:

**ss1_beam_steering \= ...**  
**sigstrength(rx1,tx,rtPlusWeather);**

Then:

**beamGainImprovement1 \= ...**  
**ss1_beam_steering \- ss1_weather;**

Students report:

Before beam steering: \_\_\_ dBm  
After beam steering : \_\_\_ dBm

Improvement : \_\_\_ dB

### **Important conclusion**

Students should discover that antenna beam steering can significantly improve a NLOS link by directing energy toward a useful propagation path.

---

# **PART 27—MINI CHALLENGE: Beam Steering for UE2**

This should be your **final major challenge**.

Students must repeat the beam-steering procedure for UE2.

They should:

1. Calculate UE2's ray.
2. Extract UE2's angle of departure.
3. Calculate UE2's steering angle.
4. Generate UE2's steering vector.
5. Apply the new antenna taper.
6. Plot the radiation pattern.
7. Calculate UE2 received power.
8. Calculate beam-steering improvement.

They should ultimately produce:

|                      | UE1        | UE2        |
| -------------------- | ---------- | ---------- |
| Before beam steering | \_\_\_ dBm | \_\_\_ dBm |
| After beam steering  | \_\_\_ dBm | \_\_\_ dBm |
| Improvement          | \_\_\_ dB  | \_\_\_ dB  |

---

# **Final Workshop Challenge 🏆**

Give students **15–20 minutes** for this without giving them the solution.

### **Challenge**

> Add a third user equipment at a new location and perform the complete propagation analysis independently.

Students should implement:

                   ┌── UE1
                    │
                    ├── UE2

5G Base Station ────┤  
│  
└── UE3

They must perform:

**Environment**

→ Add UE3

**Propagation**

→ LOS  
→ 1 reflection  
→ Concrete  
→ Weather  
→ 2 reflections  
→ 1 diffraction

**Analysis**

→ Received power  
→ Path loss  
→ Dominant ray  
→ Propagation distance  
→ Angle of departure

**Antenna**

→ Steering vector  
→ Beam steering  
→ New received power

**Final result**

They create their own table:

| Parameter          | UE1 | UE2 | UE3 |
| ------------------ | --- | --- | --- |
| LOS/NLOS           |     |     |     |
| Received power     |     |     |     |
| Concrete           |     |     |     |
| Weather            |     |     |     |
| 2 reflections      |     |     |     |
| 2R \+ 1D           |     |     |     |
| Beam-steered power |     |     |     |
| Beam improvement   |     |     |     |

---

# **Recommended 6-Hour Workshop Structure**

| Time          | Activity                                                        |
| ------------- | --------------------------------------------------------------- |
| **0:00–0:20** | Introduction to wireless propagation and ray tracing            |
| **0:20–0:45** | MATLAB \+ Chicago 3-D environment                               |
| **0:45–1:15** | Transmitter and UE creation                                     |
| **1:15–1:45** | LOS/NLOS and first ray tracing                                  |
| **1:45–2:15** | Received power and coverage map                                 |
| **2:15–2:30** | ☕ Break                                                        |
| **2:30–3:00** | Building materials \+ weather                                   |
| **3:00–3:30** | Reflections \+ diffraction                                      |
| **3:30–4:00** | **Challenge 1: Add UE2 and repeat analysis**                    |
| **4:00–4:30** | Antenna array \+ radiation pattern                              |
| **4:30–5:00** | Beam steering                                                   |
| **5:00–5:30** | **Challenge 2: Beam steering for UE2**                          |
| **5:30–6:00** | **Final Challenge: Add UE3 \+ complete analysis \+ discussion** |

## **What students should have at the end**

Each student/team should have a MATLAB project containing:

Chicago 3-D urban environment  
↓  
5G Base Station  
↓  
UE1 \+ UE2 (+ UE3 challenge)  
↓  
LOS/NLOS analysis  
↓  
Ray tracing  
↓  
Reflection analysis  
↓  
Diffraction analysis  
↓  
Material effects  
↓  
Weather effects  
↓  
Coverage map  
↓  
8×8 antenna array  
↓  
Radiation pattern  
↓  
Dominant ray extraction  
↓  
Beam steering  
↓  
Received-power comparison

Expected final output:  
![][image1]

[image1]: data:image/png;base64,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
