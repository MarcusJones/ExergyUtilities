# ExergyUtilities
# Copyright (c) 2010, B. Marcus Jones <>
# All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The :mod:`xx` module 
"""

#===============================================================================
# Set up
#===============================================================================
from __future__ import division
from __future__ import print_function

import logging.config
import subprocess
from datetime import datetime
import time
from config import *

import warnings

# psutil is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network)in Python.
try:
    import psutil
    FLG_PSUTIL = True
except ImportError, e:
    FLG_PSUTIL = False
    warnings.warn(
   "'psutil' module not imported. Without psutil, current CPU load is not detected.",
    ImportWarning
    )
    pass 


# max_cpu_percent = 80
# max_processes = 4
# update_delay = 2

#===============================================================================
# Code
#===============================================================================
class DOSCommand(object):
    """A class holding a running DOS command
    Keyword arguments:
    runID                 - An arbitrary ID for tracking
    execution_command     - the fully formed DOS command string
    
    Internal:
    status           - Pending -> Running -> Finished
    process          - The actual subprocess Popen object
    PID              - Process ID in Windows
    run_start_time   - Time started
    run_end_time     - Time ended
    """
    
    def __init__(self, runID, execution_command): 
        self.runID = runID
        self.execution_command = execution_command
        
        self.status = "Pending"
        self.process = None
        self.PID = None
        self.run_start_time = None
        self.run_end_time = None
        
    def execute(self):
        """Call subprocess with command
        """
        logging.info("Executing ID {}; {}".format(self.runID,self.execution_command))
        
        self.process = subprocess.Popen(self.execution_command, shell=True)
        self.PID = self.process.pid
        self.run_start_time = datetime.now()
        
    def update(self):
        """Check on the status of the process, update if necessary
        """
        if self.process:
            retcode = self.process.poll()
            # Windows exit code
            if retcode is None:
                self.status = "Running"
            else:
                # Add more handling for irregular retcodes
                # See i.e. http://www.symantec.com/connect/articles/windows-system-error-codes-exit-codes-description
                self.status = "Finished"
                self.run_end_time  = datetime.now()
        else:
            # This process has not been started
            pass

def execute_parallel(commands, update_delay, max_cpu_percent, max_processes):
    """This function will execute a list of DOS commands
    DOS commands are passed as a list of strings 
    Strings have all flags and paths (commands assembled externally)
    System parameters CONSTANTS:
    update_delay - Time in seconds to update the run loop
    max_cpu_percent - How close to run the processor to maximum (Say 80%, leaving 20% for other tasks)
    max_processes - How many processes in parallel maximum
    """

    logging.debug("Received {} commands".format(len(commands)))
    
    # The three queues 
    pending_queue = list()
    live_queue = list()
    finished_queue = list()
    
    id_num = 0
    # Instantiate DOSCommand objects from strings
    for cmd in commands:
        pending_queue.append(DOSCommand(id_num,cmd))
        id_num += 1
        logging.debug("Added to queue: {} {}".format(id_num,cmd))
    
    while live_queue or pending_queue:
        # The system loop delay
        time.sleep(update_delay)
        
        # Check CPU load
        if FLG_PSUTIL:
            currentCPU = psutil.cpu_percent()
        else:
            currentCPU = -1

        # Try to move 1 process from pending -> live
        if (pending_queue and
            currentCPU <= max_cpu_percent and 
            len(live_queue) < max_processes):
            # Shift a run to the live_queue
            live_queue.append(pending_queue.pop(0))
            # Execute this run (the last one in live_queue)
            live_queue[-1].execute()

        # Check the live queue
        for run in live_queue:
            run.update()
            # Move off the live queue if finished
            if run.status == "Finished":
                finished_queue.append(run)
                live_queue.remove(run)
                
        print("CPU: {}, pending: {}, live: {}, finished: {}".format(currentCPU,
                                                                  len(pending_queue),
                                                                  len(live_queue),
                                                                  len(finished_queue),
                                                                  ))
     
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    execute_parallel(["echo Testing 1","echo Testing 2"], update_delay = 2, max_cpu_percent = 80, max_processes = 4)

    logging.debug("Finished _main".format())

    