#SOVEREIGN
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here
from ghidra.app.decompiler import DecompInterface
from ghidra.app.util.exporter import BinaryExporter
from ghidra.program.model.lang import Register
from ghidra.util.task import ConsoleTaskMonitor
from java.io import File
import json
import base64
import os
from binascii import hexlify

# Initialize decompiler
decompInterface = DecompInterface()
decompInterface.openProgram(currentProgram)

# Function to get decompiled code
def getDecompiledFunction(function):
    results = decompInterface.decompileFunction(function, 0, ConsoleTaskMonitor())
    if results.decompileCompleted():
        return results.getDecompiledFunction(), results.getHighFunction()
    return ""

#def b64e(s):
#    return base64.b64encode(s.encode('ascii')).decode('ascii')

# Get all functions
function_details = []
fm = currentProgram.getFunctionManager()
functions = fm.getFunctions(True)

for f in functions:
    try:
        func_detail = {}
        func_detail["name"] = f.getName()
        func_detail["raw"] = [hexlify(instr.getBytes()) for instr in currentProgram.getListing().getInstructions(f.getBody(), True)]
        func_detail["p_code"] = [str(instr.getPcode()) for instr in currentProgram.getListing().getInstructions(f.getBody(), True)]
        decompiled_func, high_func = getDecompiledFunction(f)
        func_detail["p_code_refined"] = [op.toString() for op in high_func.getPcodeOps()]
        func_detail["c_code"] = decompiled_func.getC() if decompiled_func else ""
        func_detail["assembly"] = [instr.toString() for instr in currentProgram.getListing().getInstructions(f.getBody(), True)]  # Add assembly code
        function_details.append(func_detail)
    except:
        continue

# Convert to JSON and write to file
folder_path = "/mnt/ssd1/authorship-attribution/GCJ/malcode_casestudy/" + getState().getProject().getProjectData().getProjectLocator().getName()
# create folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
file_path = folder_path + "/function_details_" + currentProgram.getName() + ".json"
with open(file_path, "w") as f:
    json.dump(function_details, f, indent=4)
