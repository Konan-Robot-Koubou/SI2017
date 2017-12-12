#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file pi2goRTC.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
import pi2go 
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

 #転輪幅(メートル)
# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
pi2gortc_spec = ["implementation_id", "pi2goRTC", 
		 "type_name",         "pi2goRTC", 
		 "description",       "ModuleDescription", 
		 "version",           "o.1.0", 
		 "vendor",            "Konan_University", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.Speed", "60",
		"conf.__widget__.Speed", "text",
		 ""]
# </rtc-template>

##
# @class KurobakoRTC
# @brief ModuleDescription
# 
# 
class pi2goRTC(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_SpeedIn = RTC.TimedVelocity2D(RTC.Time(0,0),[])
		"""
		"""
		self._SpeedInIn = OpenRTM_aist.InPort("SpeedIn", self._d_SpeedIn)
		
		self._d_Switch = RTC.TimedBooleanSeq(RTC.Time(0,0),[])
		"""
		"""
		self._SwitchOut = OpenRTM_aist.OutPort("Switch", self._d_Switch)
		
		self._d_IRLineSensor = RTC.TimedBooleanSeq(RTC.Time(0,0),[])
		"""
		"""
		self._IRLineSensorOut = OpenRTM_aist.OutPort("IRLineSensor", self._d_IRLineSensor)

		self._d_LightReception = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._LightReceptionOut = OpenRTM_aist.OutPort("LightReception", self._d_LightReception)

		self._d_Sonar = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._SonarOut = OpenRTM_aist.OutPort("Sonar", self._d_Sonar)

		self._d_IRSensor = RTC.TimedBooleanSeq(RTC.Time(0,0),[])
		"""
		"""
		self._IRSensorOut = OpenRTM_aist.OutPort("IRSensor", self._d_IRSensor)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  Speed
		 - DefaultValue: 60
		"""
		self._Speed = [60]

		# </rtc-template>
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("SpeedIn",self._SpeedInIn)
		
		# Set OutPort buffers
		self.addOutPort("Switch",self._SwitchOut)
		self.addOutPort("IRSensor",self._IRSensorOut)
		self.addOutPort("IRLineSensor",self._IRLineSensorOut)
		self.addOutPort("Sonar",self._SonarOut)
		self.addOutPort("LightReception",self._LightReceptionOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The activated action (Active state entry action)
	#	# former rtc_active_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	# 
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onActivated(self, ec_id):
		#pi2go library setup
		pi2go.init()
	
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The deactivated action (Active state exit action)
	#	# former rtc_active_exit()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onDeactivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The execution action that is invoked periodically
	#	# former rtc_active_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onExecute(self, ec_id):
		if self._SpeedInIn.isNew():
			# 速度入力
			d=self._VelocityInIn.read().data
			VX=d.vx
			VA=d.va/3
			VL=(VX-VA)*self._Speed[0]
			VR=(VX+VA)*self._Speed[0]
			pi2go.go(int(VL),int(VR))#go(LeftSpeed,RightSpeed)

		#Write IRSensor value
		self._d_IRSensor.data = [pi2go.irLeft(),pi2go.irCentre(),pi2go.irRight()]
		OpenRTM_aist.setTimestamp(self._d_IRSensor)
		self._IRSensorOut.write()

		#Write IRLineSensor value
		self._d_IRLineSensor.data = [pi2go.irLeftLine(),pi2go.irRightLine()]
		OpenRTM_aist.setTimestamp(self._d_IRLineSensor)
		self._IRLineSensorOut.write()

		#Write Sonar value
		self._d_Sonar.data = pi2go.getDistance()
		OpenRTM_aist.setTimestamp(self._d_Sonar)
		self._SonarOut.write()

		#Write switch value
		self._d_Switch.data = pi2go.getSwitch()
		OpenRTM_aist.setTimestamp(self._d_Switch)
		self._SwitchOut.write()


		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def pi2goRTCInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=pi2gortc_spec)
    manager.registerFactory(profile,
                            pi2goRTC,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    pi2goRTCInit(manager)

    # Create a component
    comp = manager.createComponent("pi2goRTC")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

