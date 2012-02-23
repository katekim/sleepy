import glob, os
from distutils.core import *

VERSION = "0.1"

setup (name = "sleepy",
       version = VERSION,
       packages = ['sleepy',
                   'sleepy.dpat',
                   'sleepy.collection',
                   'sleepy.functional',
                   'sleepy.aassert',
                   ],

       package_dir = {'sleepy' : 'src/sleepy',
                      'sleepy.dpat' : 'src/sleepy/dpat',
                      'sleepy.collection' : 'src/sleepy/collection',
                      'sleepy.functional' : 'src/sleepy/functional',
                      'sleepy.aassert' : 'src/sleepy/aassert',
                      },

       package_data = {'sleepy.aassert' : ["messages.yaml"]},
       )
