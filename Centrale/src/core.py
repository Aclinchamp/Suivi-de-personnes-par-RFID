#coding: utf-8
from command import Command, CommandTypes
from collections import OrderedDict
import sys
import parser
from interfaceMqtt import InterfaceMqtt as intfMqtt
from logger import Logger, LogLevel
import time
from bddManager import BddManager

from queue import Queue

sys.path.append("../res")
import setting

def main():

    fifo_mqtt2core = Queue()
    fifo_core2mqtt = Queue()
   
    print("[Core] Create logger")
    logger = Logger()

    Logger.log(LogLevel.DEBUG, "CORE", "Create interface thread")
    mqtt = intfMqtt(fifo_mqtt2core, fifo_core2mqtt)
    mqtt.start()

    while(mqtt.connected== False):
        time.sleep(0.25)
	
    Logger.log(LogLevel.DEBUG, "CORE", "Create bdd manager")
    #manager = BddManager("localhost", "BDD_HospitalTracking", "boitier", "hospital")

    while(True):

        Logger.log(LogLevel.DEBUG, "CORE", "Waiting for msg from mqtt")
        cmd = fifo_mqtt2core.get()
        cmd.printCmd()

    Logger.log(LogLevel.DEBUG, "CORE", "Stopping threads")
    mqtt.stop()
    mqtt.join()
   
    Logger.log(LogLevel.INFO, "CORE", "Core is down")
    
if __name__ == "__main__":
    main()