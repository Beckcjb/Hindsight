import matlab.engine

print("Starting Matlab engine")
matlab_engine = matlab.engine.start_matlab()
matlab_engine.addpath(r'./Source_Code/colorSegMatlab')
matlab_engine.addpath(r'./Source_Code/findAbrasion')
print("Engine finished")
