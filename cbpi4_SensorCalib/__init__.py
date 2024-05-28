
# -*- coding: utf-8 -*-
#import os
#from aiohttp import web
import logging
#from unittest.mock import MagicMock, patch
import asyncio
from time import sleep
#import random
from cbpi.api import *
from cbpi.api.base import CBPiBase
# from statistics import fmean

logger = logging.getLogger(__name__)


@parameters([Property.Sensor(label="Sensor01", description="Select a sensor for this group."),
            Property.Number(label="a", description="as a in y= a*x^2 + b*x + c"),
            Property.Number(label="b", description="as b in y= a*x^2 + b*x + c"),
            Property.Number(label="c", description="as c in y= a*x^2 + b*x + c")])

class CalibSensor(CBPiSensor):


    def __init__(self, cbpi, id, props):
        super(CalibSensor, self).__init__(cbpi, id, props)
        self.value = 0      
        self.sensors = 0
        self.a = self.props.get("a", 0)
        self.b = self.props.get("b", 0)
        self.c = self.props.get("c", 0)

        logging.info("CalibSensor")
        if self.props.get("Sensor01", None) is not None:
            self.sensors = self.props.get("Sensor01")
        
        pass

    def get_state(self):
        return self.value
   
    async def run(self):
        while self.running == True:
            values = None
            try:
                
                sensor_value = self.cbpi.sensor.get_sensor_value(self.sensors).get("value")
                if sensor_value is not None:
                    values = float(sensor_value)
                
                if values is not None:
                    self.value = self.a * values**2 + self.b * values + self.c
                else:
                    logging.info("No values fetched from the selected child sensors, check connections and setup")

            except Exception as e:
                logging.info(e)
                pass 

            self.log_data(self.value)
            self.push_update(self.value)
            await asyncio.sleep(5)

        pass


def setup(cbpi):
    cbpi.plugin.register("Calibrated Sensor", CalibSensor)
    pass
