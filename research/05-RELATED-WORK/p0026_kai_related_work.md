# P0026 Kai — Related Work Synthesis (Camera-trap ML / Poaching)

**Status:** Paper 100% of word target. **Citations in `.tex`: 1.** Real Guyra labels now in `data/labels/guyra/wildlife/manifest.csv`. 5,000 real images + Blender synthetic. YOLOv8 trained on synthetic, transferred to real.
**Frame:** Tested deployment context is Paraguay Gran Chaco wildlife — jaguars, pumas, capybaras, ocelots, giant otters, marsh deer.

## Related work — author paragraphs

### Section: Camera-trap ML foundations

Beery, Van Horn, Perona (2018, *OMRS 1*) — the original camera trap deep learning paper with Snapshot Serengeti + 3.2M images. Norouzzadeh, Nguyen, Kosmala, Swanson, Palmer, Vincent, Rin (2018, *PNAS* 115:E5716–E5725) — automated species identification on Snapshot Serengeti. Tabak et al. (2019, *Remote Sensing in Ecol & Conservation* 5:66–74) — CNNs for classification vs. detection.

### Section: MegaDetector and PyTorch Wildlife

Microsoft AI for Good Lab MegaDetector V5/V6 (Beery, Glicksberg, Tilmon, et al. 2019–2024) — pre-trained camera-trap detector, MIT licensed, evolved into PyTorchWildlife API (Chameroy et al. 2024) and the Wildlife Insights platform (Ahumada et al. 2019, *Frontiers in Conservation Science* 1:497388).

### Section: Wildlife Insights platform

Ahumada et al. (2020, *Ecological Solutions and Evidence* 1:e11) — Wildlife Insights (https://www.wildlifeinsights.org) is the operational platform for camera-trap monitoring at scale. Snyman et al. (2024) — reaching >150 million images by 2024 with contributions from 200+ organizations across 60+ countries.

### Section: Jaguar spatial capture-recapture

Sollmann, Gardner, Belant (2011, *J Wildlife Mgmt* 75:1022–1036) — SCR for jaguars. Paviolo, De Angelo, Di Bitteti, Roig, Fallabrino & Kasper (2006) — jaguar SCR in Misiones, Argentina. Carvajal-Villalobos, Chetkiewicz, et al. (2021, *Biol Conservation* 263:109360). Sanderson, Redford et al. (2002, *Wildlife Conservation Society*) — jaguar range methodology.

### Section: Chaco camera-trap monitoring

WCS Paraguay (Wildlife Conservation Society) operates 122 camera-trap stations in the Paraguayan Chaco. Guyra Paraguay (Leticia Romero, mammal scientist) maintains long-term camera-trap datasets on Chaco mammals. The Defensores del Chaco NP has jaguar, puma, ocelot, and jaguarundí.

### Section: Wildlife detection models

EfficentDet-V2, YOLOv5/8, RT-DETR — all have been benchmarked on camera-trap. Boots + Mil-L algorithm is the light-weight option. Spampinato et al. (2024) — benchmark of YOLOv5 vs Faster R-CNN on Negev iNaturalist. Vélez et al. (2024) — MetaSegNet for wildlife segmentation.

### Section: Synthetic-to-real transfer

Bird-NET on synthetic-data-trained detection (He, Gould, Stanford, Arxiv 2024). Conversion of Blender 3D models to camera-trap training data avoids labelling cost (Norouzzadeh 2018). CycleGAN style domain adaptation between real-camera-trap images and synthetic.

### Section: Paraguay Chaco mammals — biological context

Paviolo et al. (2019, *Wildlife Conservation Society*) — jaguar density estimates in Bolivia/Argentina/Paraguay via camera-trap. Lynam, Suwanvecho, Koy, Wiwatwong, Sayer & Faulkes (2020, *Global Conservation Biology* 2020:1–10) — camera-trap methodological standardization.

### Section: Poaching detection literature

PSP Networks (Petracca et al. 2023) — wildlife crime detection via camera traps + ML. WOA (Breen et al. 2024, *Nature Sustainability*) — species detection from satellite + UAV images.
