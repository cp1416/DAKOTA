# CMakeLists.txt for DAKOTA tests

set(aux_files)
set(aux_files "cantilever cantilever.template driver.sh"
  )

set(extra_files)
set(extra_files " ")

add_training_test(dakota_opt_cons_cantilever.in ${aux_files} ${extra_files} TRUE)
