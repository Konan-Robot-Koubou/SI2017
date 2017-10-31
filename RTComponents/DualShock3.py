#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file DualShock3.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import pygame


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>

pygame.init()
pygame.joystick.init()
JoyN=pygame.joystick.get_count()
if JoyN==0:
        exit(1)
JoyNS=""
JoyND={}
DefN=None
for i in range(JoyN):
        Name=pygame.joystick.Joystick(i).get_name().strip()
        JoyND[Name]=i
        JoyNS+=Name+","
        if DefN is None:
                DefN=Name
JoyNS=JoyNS[:-1]

# This module's spesification
# <rtc-template block="module_spec">
dualshock3_spec = ["implementation_id", "DualShock3", 
		 "type_name",         "DualShock3", 
		 "description",       "ModuleDescription", 
		 "version",           "0.1.0", 
		 "vendor",            "Konan_University", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "4", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "lang_type",         "SCRIPT",
		 "conf.default.JoyStick", DefN,
		 "conf.__widget__.JoyStick", "radio",
		 "conf.__constraints__.JoyStick", "("+JoyNS+")",
		 ""]
# </rtc-template>

##
# @class DualShock3
# @brief ModuleDescription
# 
# 
class DualShock3(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_LAnalogStick = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._LAnalogStickOut = OpenRTM_aist.OutPort("LAnalogStick", self._d_LAnalogStick)

		self._d_RAnalogStick = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._RAnalogStickOut = OpenRTM_aist.OutPort("RAnalogStick", self._d_RAnalogStick)

		self._d_CrossKey = RTC.TimedBooleanSeq(RTC.Time(0,0),[])
		"""
		"""
		self._CrossKeyOut = OpenRTM_aist.OutPort("CrossKey", self._d_CrossKey)

		self._d_Button= RTC.TimedBooleanSeq(RTC.Time(0,0),[])
		"""
		"""
		self._ButtonOut = OpenRTM_aist.OutPort("Button", self._d_Button)

		self._d_SideButton= RTC.TimedBooleanSeq(RTC.Time(0,0),[])
		"""
		"""
		self._SideButtonOut = OpenRTM_aist.OutPort("SideButton", self._d_SideButton)


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>
		"""

		 - Name:  JoyStick
		 - DefaultValue: N
		"""
		self._JoyStick = [DefN]

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
		self.bindParameter("JoyStick", self._JoyStick, "N")
		
		# Set InPort buffers
		
		# Set OutPort buffers
		self.addOutPort("LAnalogStick",self._LAnalogStickOut)
		self.addOutPort("RAnalogStick",self._RAnalogStickOut)
		self.addOutPort("CrossKey",self._CrossKeyOut)
		self.addOutPort("Button",self._ButtonOut)
		self.addOutPort("SideButton",self._SideButtonOut)
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
		JoyName=self._JoyStick[0]
		self.JS=pygame.joystick.Joystick(JoyND[JoyName])
		self.JS.init()
		self.AN=self.JS.get_numaxes()
		self.BN=self.JS.get_numbuttons()
		print JoyName
		print "Axis     ",self.AN
		print "Button   ",self.BN
		
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
	def onDeactivated(self, ec_id):
                self.JS.quit()
		return RTC.RTC_OK
	
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
		pygame.event.pump()
		Ax=[]
		Bn=[]
		LA=[]
		RA=[]
		CrossKey=[]
		Button=[]
		SideButton=[]
		for i in xrange(self.AN):
			x=self.JS.get_axis(i)
			Ax.append(x)
		LA.append(Ax[0])
		LA.append(Ax[1])
		RA.append(Ax[2])
		RA.append(Ax[3])
		for i in xrange(self.BN):
			x=self.JS.get_button(i)==1
			Bn.append(x)
		
		for i in range(4,8):
			CrossKey.append(Bn[i])
			Button.append(Bn[i+8])
			SideButton.append(Bn[i+4])
		self._d_LAnalogStick.data = LA
		self._d_RAnalogStick.data = RA
		self._d_CrossKey.data = CrossKey
		self._d_Button.data = Button
		self._d_SideButton.data = SideButton
		OpenRTM_aist.setTimestamp(self._d_LAnalogStick)
		OpenRTM_aist.setTimestamp(self._d_RAnalogStick)
		OpenRTM_aist.setTimestamp(self._d_CrossKey)
		OpenRTM_aist.setTimestamp(self._d_Button)
		OpenRTM_aist.setTimestamp(self._d_SideButton)
		self._LAnalogStickOut.write()
		self._RAnalogStickOut.write()
		self._CrossKeyOut.write()
		self._ButtonOut.write()
		self._SideButtonOut.write()

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
	



def DualShock3Init(manager):
    profile = OpenRTM_aist.Properties(defaults_str=dualshock3_spec)
    manager.registerFactory(profile,
                            DualShock3,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    DualShock3Init(manager)

    # Create a component
    comp = manager.createComponent("DualShock3")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

