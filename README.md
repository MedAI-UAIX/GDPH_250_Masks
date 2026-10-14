# GDPH-250: Lesion Segmentation Masks for 250 Breast Ultrasound Images

Expert-annotated breast lesion masks for 250 breast ultrasound (BUS) images, sampled 1:1 from benign and malignant cases of the public GDPH dataset released with the HoVer-Trans study (IEEE TMI, 2023). Annotations were produced by three physicians under a two-reader-plus-arbitration protocol.

## Dataset Overview

- **250 images**: 125 benign (`_B`) + 125 malignant (`_M`), sampled 1:1 from 846 source images.
- **Mask format**: single-channel PNG, binary — `0` = background, `255` = lesion. Mask size is identical to the source image (no resizing; do not convert to lossy formats).
- **Sampling**: 250 cases (benign : malignant = 1 : 1) randomly drawn from the 846-image source pool, with near-duplicate rejection and a serial-number gap rule to avoid repeated frames of the same lesion; details see `sample.py`.
- **Naming and sampling rules**: mask filenames follow `GDPH_XXXX_B/M.png`; image-mask correspondence is given in `index.csv`.

## Folder Structure

```
GDPH_250_mask/
├── final/       # 250 consensus masks (the recommended labels)
├── doctor1/     # Reader 1 independent annotations (250)
├── doctor2/     # Reader 2 independent annotations (250)
├── doctor3/     # Reader 3 arbitration annotations (38)
├── index.csv    # Index: mask_id, original_id, dice(1&2), final_mask
└── sample.py    # Script reproducing the renaming and sampling pipeline
```

## Annotation Protocol

1. Two physicians with more than 10 years of experience independently delineated the lesion boundary in all 250 images (`doctor1/`, `doctor2/`), without knowing the image label in advance. Delineation criteria: each lesion was outlined along its outermost margin, only the lesion itself was included (surrounding normal tissue excluded), and when multiple lesions were present in one image, all of them were delineated. Pairwise Dice similarity scores are reported in `index.csv` (mean 0.87).
2. A senior physician with 15 years of experience reviewed the annotations and selected the final mask for each case. The 38 cases with reader Dice < 0.8 were re-annotated by this third physician (`doctor3/`); the final mask for these cases is the third reader's annotation.
3. For the remaining 212 cases, the final mask follows the consistent reader's annotation, recorded in the `final_mask` column of `index.csv` (`doctor1` ×112, `doctor2` ×100, `doctor3` ×38).

## Source Data and Terms of Use

- **This release contains segmentation masks only, not the source images.** The images derive from the public GDPH dataset released with: *Mo et al., "HoVer-Trans: Anatomy-aware HoVer-Transformer for ROI-free Breast Cancer Diagnosis in Ultrasound Images," IEEE Transactions on Medical Imaging, 2023, doi: 10.1109/TMI.2023.3236011*. Please obtain the image collection from the original authors via the official project page: <https://github.com/yuhaomo/HoVerTrans>.
- Match images to masks by filename via `index.csv`.
- **License for these annotations: CC BY-NC 4.0** (applying to the masks only, not the source images). 

## Citation

If you use this dataset, please cite both the source dataset paper and this dataset:

```bibtex
@article{mo2023hovertrans,
  author={Mo, Yuhao and Han, Chu and Liu, Yu and Liu, Min and Shi, Zhenwei and Lin, Jiatai and Zhao, Bingchao and Huang, Chunwang and Qiu, Bingjiang and Cui, Yanfen and Wu, Lei and Pan, Xipeng and Xu, Zeyan and Huang, Xiaomei and Li, Zhenhui and Liu, Zaiyi and Wang, Ying and Liang, Changhong},
  journal={IEEE Transactions on Medical Imaging},
  title={HoVer-Trans: Anatomy-Aware HoVer-Transformer for ROI-Free Breast Cancer Diagnosis in Ultrasound Images},
  year={2023},
  volume={42},
  number={6},
  pages={1696-1706},
  doi={10.1109/TMI.2023.3236011}
}
```

```
GDPH-250 Breast Ultrasound Lesion Masks, v1.0, 2026.
```

**Note:** a paper describing this dataset is currently under review. If you use these masks, please cite that paper once it is published; until then, acknowledging this dataset (GDPH-250 Breast Ultrasound Lesion Masks) is sufficient. We will add the full citation here as soon as the paper is accepted.

## Changelog

- **v1.0** — Initial release: 250 consensus masks, individual reader annotations, index CSV, and the reproducible sampling pipeline.
