#Helderheid van een pixel bekijken die op de fotonen ring zit
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import glob
import re
import os

# ==========================
# Instellingen
# ==========================
data_folder = r"C:\Users\lbloe\OneDrive\Bureaublad\UNI\NATUURKUNDE JAAR 2\Project 4\Fits_files"
files = glob.glob(os.path.join(data_folder, "*.asc"))


sigma_smooth = 5
r_ignore = 200
delta_r = 2   # halve ringbreedte (pixels)

# ==========================
# Hulpfuncties
# ==========================
def extract_time(filename):
    base = os.path.basename(filename)

    # voorbeeld: Expt1pp01_gtb2_c4__1003_f_1.asc
    parts = base.split("__")[1]        # "1003_f_1.asc"
    time_part, frame_part = parts.split("_f_")

    time = int(time_part)
    frame = int(frame_part.replace(".asc", ""))

    return time, frame

files_sorted = sorted(files, key=extract_time)
for f in files_sorted[:11]:
    print(os.path.basename(f))
print("Laatste bestand:", os.path.basename(files_sorted[-1]))


def compute_ring_radius_and_intensity(data):
    # --- centrum ---
    y, x = np.indices(data.shape)
    total_I = np.sum(data)
    x0 = np.sum(x * data) / total_I
    y0 = np.sum(y * data) / total_I

    # --- radius ---
    r = np.sqrt((x - x0)**2 + (y - y0)**2)
    r_int = r.astype(int)

    # --- radiaal profiel ---
    sum_I = np.bincount(r_int.ravel(), data.ravel())
    count = np.bincount(r_int.ravel())
    radial_profile = sum_I / count

    # --- achtergrond ---
    bg = np.median(radial_profile[int(0.8 * len(radial_profile)):])
    profile = radial_profile - bg
    profile[profile < 0] = 0

    # --- smoothing ---
    profile_smooth = gaussian_filter1d(profile, sigma=sigma_smooth)

    # --- ringradius ---
    gradient = np.gradient(profile_smooth)
    ring_radius = r_ignore + np.argmin(gradient[r_ignore:])

    # --- intensiteit op ring ---
    mask = (r > ring_radius - delta_r) & (r < ring_radius + delta_r)
    ring_intensity = np.mean(data[mask])

    return ring_radius, ring_intensity


# ==========================
# Bestanden verwerken
# ==========================

times = []
radii = []
intensities = []

for file in files_sorted:
    try:
        data = np.loadtxt(file, delimiter=",")
        R, I = compute_ring_radius_and_intensity(data)

        t,frame = extract_time(file)
        if t is None:
            t = len(times)

        times.append(t+ 0.1*frame)
        radii.append(R)
        intensities.append(I)

        print(f"{os.path.basename(file)} → R={R:.1f} px, I={I:.2f}")

    except Exception as e:
        print(f"FOUT in {file}: {e}")

# ==========================
# Plotten
# ==========================
times = np.array(times)
intensities = np.array(intensities)

idx = np.argsort(times)
times = times[idx]
intensities = intensities[idx]

plt.figure(figsize=(8,5))
plt.plot(times, intensities, 'o-', lw=2)
plt.xlabel("Tijd / frame")
plt.ylabel("Gemiddelde intensiteit op ring")
plt.title("Helderheid van fotonenring vs tijd")
plt.grid(True)
plt.tight_layout()
plt.show()
