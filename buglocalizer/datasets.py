from collections import namedtuple
from pathlib import Path

# Dataset root directory
_DATASET_ROOT = Path('../data')

Dataset = namedtuple('Dataset', ['name', 'root', 'src', 'bug_repo'])

# Source codes and bug repositories
# aspectj = Dataset(
#     'aspectj',
#     _DATASET_ROOT / 'AspectJ',
#     _DATASET_ROOT / 'AspectJ/AspectJ-1.5',
#     _DATASET_ROOT / 'AspectJ/AspectJBugRepository.xml'
# )

# swt = Dataset(
#     'swt',
#     _DATASET_ROOT / 'SWT',
#     _DATASET_ROOT / 'SWT/SWT-3.1',
#     _DATASET_ROOT / 'SWT/SWTBugRepository.xml'
# )

zxing = Dataset(
    'zxing',
    _DATASET_ROOT / 'ZXing',
    _DATASET_ROOT / 'ZXing/ZXing-1.6',
    _DATASET_ROOT / 'ZXing/ZXingBugRepository.xml'
)

aspectj = Dataset(
    'aspectj',
    _DATASET_ROOT / 'sourceFile_aspectj',
    _DATASET_ROOT / 'sourceFile_aspectj/org.aspectj',
    _DATASET_ROOT / 'sourceFile_aspectj/AspectJ_v2.xml'
)
eclipseui = Dataset(
    'eclipseui',
    _DATASET_ROOT / 'sourceFile_eclipseUI',
    _DATASET_ROOT / 'sourceFile_eclipseUI/eclipse.platform.ui',
    _DATASET_ROOT / 'sourceFile_eclipseUI/Eclipse_Platform_UI.xml'
)
jdt = Dataset(
    'jdt',
    _DATASET_ROOT / 'sourceFile_jdt',
    _DATASET_ROOT / 'sourceFile_jdt/eclipse.jdt.ui',
    _DATASET_ROOT / 'sourceFile_jdt/JDT.xml'
)
swt = Dataset(
    'swt',
    _DATASET_ROOT / 'sourceFile_swt',
    _DATASET_ROOT / 'sourceFile_swt/eclipse.platform.swt',
    _DATASET_ROOT / 'sourceFile_swt/SWT.xml'
)
tomcat = Dataset(
    'tomcat',
    _DATASET_ROOT / 'sourceFile_tomcat',
    _DATASET_ROOT / 'sourceFile_tomcat/tomcat',
    _DATASET_ROOT / 'sourceFile_tomcat/Tomcat.xml'
)

### Current dataset in use. (change this name to change the dataset)
DATASET = aspectj

if __name__ == '__main__':
    print(DATASET.name, DATASET.root, DATASET.src, DATASET.bug_repo)
