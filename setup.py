from setuptools import setup, find_packages
import os
from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

VERSION = "version.txt"
REQUIREMENTS = "requirements.pkg.txt"
PATH = "cxs.pth"


def get_path(fi):
    return os.path.join(os.path.dirname(__file__), fi)


with open(get_path(REQUIREMENTS)) as f:
    reqs = [line.strip() for line in f if "==" in line and not line.strip().startswith("#")]


with open(get_path(VERSION)) as f:
    version = [x.strip() for x in f][0]


exclude = [
    "cxs.tests",
    "cxs.tools"
]

setup(
    name="cxs338",
    version=version,
    description="CXS338",
    author="AJ",
    author_email="ajvazquez.teleco@gmail.com",
    #url
    data_files=[(site_packages_path, [PATH])],
    install_requires=reqs,
    packages=[x for x in find_packages(exclude=exclude) if x.startswith("cxs")],
    entry_points={
        "console_scripts": [
            # Spark
            "cxs = cxs.parallel.spark.spark_cx:main",
            
            # Tools
            "cx-vis-compare = cxs.iocx.visibilities.tools.vis_compare:main",
            "cx-vdif-gen = cxs.iocx.readers.vdif.tools.vdif_generator:main",
            "cx-vdif-info = cxs.iocx.readers.vdif.tools.vdif_info:main",
            
            # Hadoop
            "cxh = cxs.parallel.hadoop.mapred_cx:main",
            
            # Conversion tools
            "cx2d-pcal = cxs.conversion.difx.convert_cx2d:main",
            "cx2d = cxs.conversion.difx.convert_cx_dx:main",
            "im2cx = cxs.conversion.difx.convert_im_cx:main",
            "cx-zoom = cxs.conversion.difx.process_zoom:main",
        ]
    }
)