#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file pi2goVel.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
pi2govel_spec = ["implementation_id", "pi2goVel",
		 "type_name",         "pi2goVel",
		 "description",       "ModuleDescription",
		 "version",           "0.1.0",
		 "vendor",            "Konan_University",
		 "category",          "Category",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 "conf.default.VXGain", "-1.0",
		 "conf.default.VAGain", "1.0",
		 "conf.default.PivotButtonN", "0",
		 "conf.default.VXAxisN", "1",
		 "conf.default.VAAxisN", "0",
		 "conf.__widget__.VXGain", "text",
		 "conf.__widget__.VAGain", "text",
		 "conf.__widget__.PivotButtonN", "text",
		 "conf.__widget__.VXAxisN", "text",
		 "conf.__widget__.VAAxisN", "text",
		 ""]
# </rtc-template>

##
# @class pi2goVel
# @brief ModuleDescription
#
#
class pi2goVel(OpenRTM_aist.DataFlowComponentBase):

	##
	# @brief constructor
	# @param manager Maneger Object
	#
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_Axis = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._AxisIn = OpenRTM_aist.InPort("Axis", self._d_Axis)

		self._d_Button = RTC.TimedBooleanSeq(RTC.Time(0,0),[])
		"""
		"""
		self._ButtonIn = OpenRTM_aist.InPort("Button", self._d_Button)

		self._d_SpeedOut = RTC.TimedVelocity2D(RTC.Time(0,0),[])
		"""
		"""
		self._SpeedOutOut = OpenRTM_aist.OutPort("SpeedOut", self._d_SpeedOut)





		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  VXGain
		 - DefaultValue: 1.0
		"""
		self._VXGain = [-1.0]
		"""
		
		 - Name:  VAGain
		 - DefaultValue: 1.0
		"""
		self._VAGain = [1.0]
		"""
		
		 - Name:  PivotButtonN
		 - DefaultValue: 0
		"""
		self._PivotButtonN = [0]
		"""
		
		 - Name:  VXAxisN
		 - DefaultValue: 0
		"""
		self._VXAxisN = [1]
		"""
		
		 - Name:  VAAxisN
		 - DefaultValue: 1
		"""
		self._VAAxisN = [0]

		self.Pivot=False


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
		self.addInPort("Axis",self._AxisIn)
		self.addInPort("Button",self._ButtonIn)

		# Set OutPort buffers
		self.addOutPort("SpeedOut",self._SpeedOutOut)

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
	#def onActivated(self, ec_id):
	#
	#	return RTC.RTC_OK

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
	    vx = 0
		va = 0
		vy = 0
		if self._AxisIn.isNew():
		##Convert Input value of analogstick to pi2go speed
			d=self._AxisIn.read().data
			x=d[self._VXAxisN[0]]
            a=d[self._VAAxisN[0]]
            vx=x*self._VXGain[0]
            if self.Pivot:
				va=-a*self._VAGain[0]
            else:
				va=a*self._VAGain[0]*x
			if x==0 and a!=0:
				va=a*self._VXGain[0]

		elif self._ButtonIn.isNew():
			d = self._ButtonIn.read().data
			if d[0] == 1:
				vx = 1
			elif d[1] == 1:
				va = 1
			elif d[2] == 1:
				vx = -1
			elif d[3] == 1:
				va = -1

		self._d_Velocity.data=RTC.Velocity2D(vx,vy,va)
		OpenRTM_aist.setTimestamp(self._d_Velocity)
        self._VelocityOut.write()		

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




def pi2goVelInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=pi2govel_spec)
    manager.registerFactory(profile,
                            pi2goVel,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    pi2goVelInit(manager)

    # Create a component
    comp = manager.createComponent("pi2goVel")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()
