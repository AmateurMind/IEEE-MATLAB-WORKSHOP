import { useMemo, useState } from 'react';
import { Check, Copy, Download, Search, Clock3 } from 'lucide-react';

const modules = [
  [
    'Getting Started with the Urban Environment',
    'Understand LOS, reflection, diffraction, and NLOS wireless propagation in a 5G city.',
    'LOS is direct; reflection bounces; diffraction bends around corners. When LOS is blocked, the link becomes NLOS.',
  ],
  [
    'Load a Real City',
    'Import Chicago OpenStreetMap building geometries into MATLAB Site Viewer.',
    'siteviewer initializes a 3D geographical simulation canvas using real building data.',
  ],
  [
    'Create the 5G Base Station',
    'Define the transmitter position, height, power, and frequency.',
    'Place a 2.5 GHz, 10 W base station at the center of the study area.',
  ],
  [
    'Create First User Equipment (UE1)',
    'Place a receiver near the base station.',
    'Receiver coordinates and antenna height define the first user scenario.',
  ],
  [
    'Check Line of Sight',
    'Determine whether a clear direct LOS line exists between TX and UE1.',
    'Use los(tx,rx1) to see whether buildings obstruct the direct path.',
  ],
  [
    'Create Ray-Tracing Model',
    'Initialize a Shooting and Bouncing Rays model.',
    'Begin with zero reflections and zero diffractions to establish a baseline.',
  ],
  [
    'Generate Coverage Map (LOS)',
    'Plot signal power distribution over a 250 m radius.',
    'Coverage maps show where a user can receive a sufficiently strong signal.',
  ],
  [
    'Introduce NLOS Propagation',
    'Enable first-order building reflections.',
    'Reflected paths let energy reach receivers behind facades.',
  ],
  [
    'Calculate Received Signal Strength',
    'Compute absolute power at UE1 in dBm.',
    'sigstrength accumulates propagation losses at the receiver.',
  ],
  [
    'Building Material Losses',
    'Replace ideal reflectors with realistic concrete.',
    'Concrete absorbs and scatters energy, reducing reflected ray power.',
  ],
  [
    'Add Weather & Gas Attenuation',
    'Combine ray tracing with atmospheric gas and rain loss models.',
    'Weather introduces additional link loss.',
  ],
  [
    'Multi-Hop Reflections (Order 2)',
    'Allow double-bounce reflection paths.',
    'Model TX to building 1 to building 2 to RX.',
  ],
  [
    'Add Edge Diffraction',
    'Incorporate knife-edge and building-corner diffraction.',
    'Diffraction can extend useful signal into NLOS corners.',
  ],
  [
    'Scenario Comparison Table',
    'Compare received power across propagation configurations.',
    'Log reflection, concrete, weather, and diffraction results together.',
  ],
  [
    'Reflection-Aware Coverage Map',
    'Generate a map including first-order reflections.',
    'Visualize how reflections reshape the signal field.',
  ],
  [
    'Advanced Urban Coverage Map',
    'Generate a full map with two reflections and one diffraction.',
    'Higher-order paths reveal detailed power contours inside building blocks.',
  ],
  [
    'Introduce User Equipment 2 (UE2)',
    'Add a second user device to the simulation.',
    'A second coordinate makes spatial variation tangible.',
  ],
  [
    'Multi-User Link Comparison',
    'Compare link metrics between UE1 and UE2.',
    'Path length, shadowing, reflection count, and diffraction angles differ.',
  ],
  [
    'Why Directional Antennas?',
    'Understand omnidirectional versus directional array beamforming.',
    'Phased arrays steer energy toward users instead of radiating equally everywhere.',
  ],
  [
    'Create 8x8 Phased Antenna Array',
    'Design a 64-element URA with half-wavelength spacing.',
    'A custom element pattern and rectangular array create a directional antenna.',
  ],
  [
    'Calculate Antenna Directivity',
    'Compute peak directivity in dBi for the array.',
    'Peak directivity grows with the number of array elements.',
  ],
  [
    'Visualize 3D Radiation Pattern',
    'Overlay radiation lobes on the base station.',
    'The 3D pattern makes main-lobe alignment visible.',
  ],
  [
    'Extract Dominant Propagation Path',
    'Extract path parameters from ray-trace objects.',
    'The dominant ray gives the geometry needed for steering.',
  ],
  [
    'Extract Angle of Departure',
    'Read azimuth and elevation departure angles.',
    'Angles of departure describe where useful energy leaves the array.',
  ],
  [
    'Apply Phased Array Beam Steering',
    'Compute a steering vector and apply array taper weights.',
    'Conjugate steering weights align array phase toward the target path.',
  ],
  [
    'Measure Beam Steering Gain Improvement',
    'Quantify power enhancement after steering on an NLOS link.',
    'Compare received power before and after steering in dBm.',
  ],
  [
    'Beam Steering for UE2',
    'Repeat path extraction, steering, and gain measurement for UE2.',
    'Each target needs its own steering solution.',
  ],
  [
    'Workshop Synthesis',
    'Review the full urban propagation pipeline.',
    'Connect city geometry, link budget, antenna pattern, and steering.',
  ],
  [
    'Analysis Notes',
    'Record observations from the two-user comparison.',
    'Capture LOS state, received power, and steering gain for each receiver.',
  ],
  [
    'Closing Q&A',
    'Revisit the questions raised by the ray-tracing lab.',
    'Leave with a testable explanation of what the city did to the signal.',
  ],
];
const snippets = {
  1: '% No MATLAB code required yet.\n% Continue to Part 2 to load the city.',
  2: 'clc;\nclear;\nviewer = siteviewer( ...\n    Buildings="chicago.osm", ...\n    Basemap="topographic");',
  3: 'tx = txsite( ...\n    Name="5G Base Station", ...\n    Latitude=41.8800, ...\n    Longitude=-87.6295, ...\n    AntennaHeight=25, ...\n    TransmitterPower=10, ...\n    TransmitterFrequency=2.5e9);',
  5: 'los(tx,rx1);',
  6: 'rtpm = propagationModel("raytracing", ...\n    Method="sbr", ...\n    MaxNumReflections=0, ...\n    MaxNumDiffractions=0);',
  7: 'coverage(tx,rtpm, ...\n    SignalStrengths=-120:-5, ...\n    MaxRange=250, Resolution=5);',
  4: 'rx1 = rxsite( ...\n    Name="User Equipment 1", ...\n    Latitude=41.881352, ...\n    Longitude=-87.629771, ...\n    AntennaHeight=30);\n\nshow(rx1);',
  8: 'rtpm.MaxNumReflections = 1;\nraytrace(tx,rx1,rtpm,Type="pathloss");',
  9: 'ss1 = sigstrength(rx1,tx,rtpm);\nfprintf("UE1 received power = %.4f dBm\\n",ss1);',
  10: 'rtpm.BuildingsMaterial = "concrete";\nrtpm.TerrainMaterial = "concrete";\n\nraytrace(tx,rx1,rtpm,Type="pathloss");\nss1_concrete = sigstrength(rx1,tx,rtpm);',
  11: 'rtPlusWeather = rtpm + propagationModel("gas") ...\n    + propagationModel("rain");\nss1_weather = sigstrength(rx1,tx,rtPlusWeather);',
  12: 'rtPlusWeather.PropagationModels(1).MaxNumReflections = 2;\nrtPlusWeather.PropagationModels(1).AngularSeparation = "low";\nss1_two_reflections = sigstrength(rx1,tx,rtPlusWeather);',
  13: 'rtPlusWeather.PropagationModels(1).MaxNumReflections = 2;\nrtPlusWeather.PropagationModels(1).MaxNumDiffractions = 1;\nss1_two_ref_one_diff = sigstrength(rx1,tx,rtPlusWeather);',
  14: 'fprintf("One reflection: %.4f dBm\\n",ss1);\nfprintf("Concrete: %.4f dBm\\n",ss1_concrete);\nfprintf("Concrete + weather: %.4f dBm\\n",ss1_weather);\nfprintf("Two reflections: %.4f dBm\\n",ss1_two_reflections);\nfprintf("Two reflections + diffraction: %.4f dBm\\n",ss1_two_ref_one_diff);',
  15: 'rtPlusWeather.PropagationModels(1).MaxNumReflections = 1;\nrtPlusWeather.PropagationModels(1).MaxNumDiffractions = 0;\ncoverage(tx,rtPlusWeather, ...\n    SignalStrengths=-120:-5, ...\n    MaxRange=250, Resolution=5, Transparency=0.6);',
  16: 'rtPlusWeather.PropagationModels(1).MaxNumReflections = 2;\nrtPlusWeather.PropagationModels(1).MaxNumDiffractions = 1;\nrtPlusWeather.PropagationModels(1).AngularSeparation = "high";\ncoverage(tx,rtPlusWeather,MaxRange=250,Resolution=5);',
  17: 'rx2 = rxsite( ...\n    Name="User Equipment 2", ...\n    Latitude=41.880600, ...\n    Longitude=-87.628800, ...\n    AntennaHeight=30);\nshow(rx2);\nlos(tx,rx2);\nraytrace(tx,rx2,rtpm);\nss2 = sigstrength(rx2,tx,rtpm);',
  18: 'fprintf("UE1 received power: %.4f dBm\\n",ss1_two_ref_one_diff);\nfprintf("UE2 received power: %.4f dBm\\n",ss2);',
  19: '% Directional antennas focus energy toward a receiver.\n% The next step creates an 8x8 phased array.',
  20: 'lambda = physconst("lightspeed") / tx.TransmitterFrequency;\ntx.Antenna = phased.URA(Size=[8 8], ...\n    ElementSpacing=[lambda/2 lambda/2]);',
  21: 'antennaDirectivity = pattern(tx.Antenna,tx.TransmitterFrequency);\nantennaDirectivityMax = max(antennaDirectivity(:));\nfprintf("Peak directivity = %.4f dBi\\n",antennaDirectivityMax);',
  22: 'tx.AntennaAngle = -90;\npattern(tx,Transparency=0.6);',
  23: 'ray = raytrace(tx,rx1,rtPlusWeather);\naod = ray{1}.AngleOfDeparture;',
  24: 'aod = ray{1}.AngleOfDeparture;\nfprintf("Azimuth = %.4f degrees\\n",aod(1));\nfprintf("Elevation = %.4f degrees\\n",aod(2));',
  25: 'steeringVector = phased.SteeringVector(SensorArray=tx.Antenna);\nsv = steeringVector(tx.TransmitterFrequency,[steeringaz;aod(2)]);\ntx.Antenna.Taper = conj(sv);',
  26: 'gain = ss1_beam_steering - ss1_weather;\nfprintf("Improvement: %.4f dB\\n",gain);',
  27: 'ray2 = raytrace(tx,rx2,rtPlusWeather);\naod2 = ray2{1}.AngleOfDeparture;\nsteeringaz2 = wrapTo180(aod2(1)-tx.AntennaAngle(1));\nsv2 = steeringVector(tx.TransmitterFrequency,[steeringaz2;aod2(2)]);\ntx.Antenna.Taper = conj(sv2);\nss2_beam_steering = sigstrength(rx2,tx,rtPlusWeather);',
  28: '% Review LOS, reflection, material, weather, diffraction,\n% and beam-steering results for UE1 and UE2.',
  29: '% Record LOS/NLOS state, received power, and steering gain\n% for each receiver in your comparison table.',
  30: '% Closing analysis: compare the city geometry, propagation\n% paths, antenna pattern, and final received power.',
};
const schedule = [
  ['00:00–00:45', 'Propagation fundamentals and Chicago 3D map'],
  ['00:45–02:30', 'TX, UE1, LOS / NLOS, ray tracing, and coverage'],
  ['02:30–03:30', 'Concrete, weather, reflections, and diffraction'],
  ['03:30–04:30', 'UE2 comparison and 8×8 phased antenna array'],
  ['04:30–05:30', 'Radiation patterns, dominant rays, and steering vectors'],
  ['05:30–06:00', 'UE2 beam steering, gain evaluation, and Q&A'],
];
function App() {
  const initialBook = new URLSearchParams(window.location.search).get('range') === '16-30' ? 1 : 0;
  const [book, setBook] = useState(initialBook);
  const [selected, setSelected] = useState(initialBook * 15);
  const [query, setQuery] = useState('');
  const [copied, setCopied] = useState(false);
  const visible = useMemo(
    () =>
      modules
        .map((m, i) => ({ m, i }))
        .filter(
          ({ m, i }) =>
            i >= book * 15 &&
            i < (book + 1) * 15 &&
            m.join(' ').toLowerCase().includes(query.toLowerCase()),
        ),
    [book, query],
  );
  const item = modules[selected];
  const snippet =
    snippets[selected + 1] || `% PART ${selected + 1}\n% Continue the workshop analysis here.`;
  function switchBook(next) {
    setBook(next);
    setSelected(next * 15);
    setQuery('');
    setCopied(false);
  }
  async function copySnippet() {
    await navigator.clipboard.writeText(snippet);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  }
  return (
    <div className="app">
      <header className="topbar">
        <a className="brand" href="#workshop">
          <img className="brand-logo" src="/only-ieee.jpeg" alt="PESMCOE emblem" />
          <span>
            <strong>MATLAB WORKSHOP</strong>
            <small>URBAN RAY TRACING · 5G</small>
          </span>
        </a>
        <div className="header-logos" aria-label="IEEE workshop organizations">
          {/* <img src="/only-ieee.jpeg" alt="IEEE Student Branch PESMCOE" /> */}
          <img
            className="featured-logo"
            src="/Comsoc _logo.jpg.jpeg"
            alt="IEEE ComSoc Student Chapter PESMCOE"
          />
          {/* <img className="college" src="/pesmcoe.jpg" alt="PESMCOE emblem" /> */}
        </div>
        <nav>
          <button className={book === 0 ? 'nav-active' : ''} onClick={() => switchBook(0)}>
            PARTS 01–15
          </button>
          <button className={book === 1 ? 'nav-active' : ''} onClick={() => switchBook(1)}>
            PARTS 16–30
          </button>
        </nav>
      </header>
      <main id="workshop">
        <section className="workspace">
          <aside className="sidebar">
            <p className="kicker">{book ? 'PARTS 16–30' : 'PARTS 01–15'}</p>
            <h2>
              {book ? 'Beam' : 'Core'}
              <br />
              <em>{book ? 'steering' : 'propagation'}</em>
            </h2>
            <label>
              <Search size={13} /> Find a module
            </label>
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by topic..."
            />
            <div className="module-list">
              {visible.map(({ m, i }) => (
                <button
                  key={i}
                  className={i === selected ? 'active' : ''}
                  onClick={() => setSelected(i)}
                >
                  <span>{String(i + 1).padStart(2, '0')}</span>
                  {m[0]}
                </button>
              ))}
            </div>
          </aside>
          <article className="lesson">
            <p className="tag">MODULE {String(selected + 1).padStart(2, '0')} / 30</p>
            <h2>{item[0]}</h2>
            <p className="description">{item[1]}</p>
            <div className="lesson-grid">
              <div>
                <h3>What you will do</h3>
                <p>{item[2]}</p>
                <h3>Field note</h3>
                <p>
                  {book
                    ? 'Each target needs its own propagation and steering solution.'
                    : 'Start with the geometry. Every later result depends on where the city puts the link.'}
                </p>
              </div>
              <div>
                <div className="code-heading">
                  <h3>MATLAB starting point</h3>
                  <button className="copy-button" onClick={copySnippet} type="button">
                    {copied ? <Check size={14} /> : <Copy size={14} />}
                    {copied ? 'Copied' : 'Copy'}
                  </button>
                </div>
                <pre>{snippet}</pre>
                <a
                  className="download"
                  href={`data:text/plain;charset=utf-8,${encodeURIComponent(snippet)}`}
                  download={`part-${selected + 1}.m`}
                >
                  <Download size={14} /> Download .m file
                </a>
              </div>
            </div>
          </article>
        </section>
        <section className="schedule">
          <div>
            <p className="kicker">
              <Clock3 size={13} /> WORKSHOP RHYTHM
            </p>
            <h2>{book ? 'Shape the link.' : 'Map the link.'}</h2>
          </div>
          <div>
            {schedule.map((row) => (
              <div className="schedule-row" key={row[0]}>
                <time>{row[0]}</time>
                <span>{row[1]}</span>
              </div>
            ))}
          </div>
        </section>
      </main>
      <footer>
        <span>IEEE MATLAB WORKSHOP</span>
        <span>Urban Ray Tracing · 5G Beam Steering</span>
      </footer>
    </div>
  );
}
export default App;
