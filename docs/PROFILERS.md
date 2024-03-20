# [BACK TO MAIN README](../README.md)

## Profilers
Before refactoring it's usually a ***great*** idea to profile the code.
The following methods describe the profilers that are available in the 
pyproject_microservices environment, and how to use them.


### SNAKEVIZ Execution
To test an entire script just enter the following from the project root
directory.

#### Profile Script
```bash
make snakeviz PROFILE_PY=script.py
```

### Memory Profiler
1. Open Jupyter Notebook
1. Load Extension
    - `%load_ext memory_profiler`
1. Run profiler
    - `%memit enter_code_here`

# [BACK TO MAIN README](../README.md)
