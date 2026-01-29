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
file_pattern = "*.asc"

sigma_smooth = 5
r_ignore = 200     # centrum uitsluiten (PSF)
window = 80        # lokale randbreedte

# ==========================
# Hulpfuncties
# ==========================
def extract_time(filename):
    """
    Haalt tijdindex uit bestandsnaam (bv __100_)
    """
    match = re.search(r'__([0-9]+)_', filename)
    if match:
        return int(match.group(1))
    else:
        return None


def compute_ring_radius(data):
    """
    Bepaalt ringradius via gradiëntmethode
    """

    # --- centrum bepalen ---
    y, x = np.indices(data.shape)
    total_I = np.sum(data)
    x0 = np.sum(x * data) / total_I
    y0 = np.sum(y * data) / total_I

    # --- radiale coördinaat ---
    r = np.sqrt((x - x0)**2 + (y - y0)**2).astype(int)

    sum_I = np.bincount(r.ravel(), data.ravel())
    count = np.bincount(r.ravel())
    radial_profile = sum_I / count

    # --- achtergrond corrigeren ---
    bg = np.median(radial_profile[int(0.8 * len(radial_profile)):])
    profile = radial_profile - bg
    profile[profile < 0] = 0

    # --- smoothing ---
    profile_smooth = gaussian_filter1d(profile, sigma=sigma_smooth)

    # --- ringradius via gradiënt ---
    gradient = np.gradient(profile_smooth)
    search_region = gradient[r_ignore:]
    ring_radius = r_ignore + np.argmin(search_region)

    return ring_radius


# ==========================
# Bestanden verwerken
# ==========================
files = sorted(glob.glob(os.path.join(data_folder, file_pattern)))

times = []
radii = []

for file in files:
    try:
        data = np.loadtxt(file, delimiter=",")
        radius = compute_ring_radius(data)

        t = extract_time(file)
        if t is None:
            t = len(times)   # fallback: index

        times.append(t)
        radii.append(radius)

        # print(f"{os.path.basename(file)} → radius = {radius:.1f} px")

    except Exception as e:
        print(f"FOUT in {file}: {e}")

# ==========================
# Resultaten plotten
# ==========================
times = np.array(times)
radii = np.array(radii)

# sorteren op tijd
idx = np.argsort(times)
times = times[idx]
radii = radii[idx]
print(times, radii)
# plt.figure(figsize=(8,5))
times = [0, 10,20,30,40,50,60,70,80,90,100,110,120]
radii= [1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226, 1226]
plt.plot(times, radii, 'o-', lw=2)
plt.xlabel("Tijd [s]")
plt.ylabel("Ringradius [pixels]")
plt.title("Verandering van ringradius in de tijd ")
plt.grid(True)
plt.tight_layout()
plt.ylim(1220,1240)
plt.xlim(0,131,)


plt.show()

# ==========================
# Opslaan
# ==========================
# np.savetxt(
#     "ringradius_vs_time.txt",
#     np.column_stack([times, radii]),
#     header="time radius_px"
# )

print("Klaar ")
