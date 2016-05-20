file format:
--line 1 indicates the number of variables N
--line 2 to N+1 indicate the parent for each variable
  -- the first number on each line is the id for the variable 1 to N-1
  -- the second number is the number of parents for this variable
  -- the ids for the parents follow
--line N+2 to 2N+1 are the CPTs for each variable
  -- the first number on each line is the id of the variable
  -- the rest are the entries in the CPT
  -- all the variables are binary, so the CPT only contains values for when the variable takes on the value TRUE
  -- please refer to the corresponding png file to understand the order of the CPT

For each network, there's a png file showing an image for the network structure