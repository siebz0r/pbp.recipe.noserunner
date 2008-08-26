from distutils.core import setup, Extension

files = [
         "base/cartesian_base.c",
         "base/permutation_base.c",
         "base/combination_base.c",
         "base/pqueue_base.c",
         "python/cartesian.c",
         "python/permutation.c",
         "python/combination.c",
         "python/pqueue.c",
         "python/stats_module.c",
        ]

libraries = []
#libraries = ["efence"] # uncomment to use ElectricFence
includes = ['include', 'python']
setup(name = "probstat", version = "0.9",
      ext_modules = [Extension("probstat", files,
                               libraries = libraries,
                               include_dirs =  includes,
                              )
                    ],
     )

